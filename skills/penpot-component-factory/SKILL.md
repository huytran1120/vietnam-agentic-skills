---
name: penpot-component-factory
description: "Build and maintain Penpot components with COMPLETE variant matrices — sizes, hierarchies, and all interactive states (default/hover/pressed/focus/disabled) — fully tokenized and correctly named. Use to create a new component with variants, fill in missing states, or normalize an existing component. Triggers: 'create a Button component with variants', 'build component variants', 'add hover/pressed/disabled states', 'make a variant matrix', 'turn this into a component with sizes', 'normalize this component'."
disable-model-invocation: false
version: 0.3.0
audiences: [design-system, product-designer]
mode-default: review
requires:
  - shared/penpot-mcp-tool-reference.md
  - shared/plugin-api-gotchas.md
  - shared/tokens-schema.json
  - shared/naming-conventions.md
  - shared/state-management.md
  - shared/modes-and-policies.md
  - shared/visual-self-review.md
  - shared/design-quality.md
---

# penpot-component-factory — complete, tokenized variants

## 1. Title + How it works
`penpot-component-factory` builds components and their **full variant matrices**; every mutation goes
through `execute_code`; validate visually with `export_shape`; read structure with
`penpotUtils.shapeStructure` (full tool surface: `shared/penpot-mcp-tool-reference.md`).
It builds a base component as a Board with flex layout (every value tokenized via `penpot-foundations`
tokens), generates variants across axes, combines them into a variant container
(`penpotUtils.createVariantContainer` on ≥ 2.17; `penpot.createVariantFromComponents` as the low-level
fallback), and verifies completeness.

## 2. The One Rule That Matters Most
**Every interactive component ships every required state, and every value is a token.** No
hardcoded fills/spacing; no missing `Hover`/`Pressed`/`Focus`/`Disabled` unless the system explicitly
says otherwise. Build one variant at a time; checkpoint before combining.

## 3. Penpot MCP Tool Reference
Full surface: `shared/penpot-mcp-tool-reference.md`. Key calls:

| Call | Why |
|------|-----|
| `penpot.createBoard()` + `addFlexLayout()` | base component container |
| `penpot.library.local.createComponent(shapes)` | turn the base into a component |
| `shape.clone()` | derive variants from the base |
| `penpotUtils.createVariantContainer([{ shape, properties }])` | preferred (≥ 2.17): container + axes + values in one call — behind the duplicate-file gate |
| `penpot.createVariantFromComponents(mainInstances)` | low-level fallback when the helper is absent |
| `instance.switchVariant(pos, value)` | demonstrate/switch variants (`pos` = index in `variants.properties`) |
| `export_shape` | visual checkpoint of the matrix |

## 4. Plugin API Essentials
Gotcha numbers refer to `shared/plugin-api-gotchas.md`.
- Build the base as a **Board** (`createBoard`, NOT `createFrame`) with `addFlexLayout()`; set `dir`, gaps, padding, `horizontalSizing`/`verticalSizing`.
- **#4 flex/grid overrides child x/y** — order children by append; use `layoutChild` for per-child sizing/margins.
- `clone()` duplicates a shape with all properties — the basis for the variant matrix.
- **#9 variant API** — prefer `penpotUtils.createVariantContainer([{ shape: mainInstance, properties: { Size: "Medium", State: "Default" } }])` (≥ 2.17) behind the duplicate-file gate; the low-level `penpot.createVariantFromComponents(mainInstances)` + `renameProperty`/`addProperty`/`setVariantProperty` path only as fallback. Switch with `instance.switchVariant(pos, value)` — `pos` is the index in `variants.properties`, not the axis name. `Board.combineAsVariants(ids)` is listed by `penpot_api_info` on 2.17 but unverified — do not use.
- **#6 detach** before mutating an instance's internals — and NEVER on a variant instance (see #12).
- **#12 variant MUTATION corrupts the file — this skill's critical failure mode.** `setVariantProperty(pos, value)` updates the variant properties but not the variant root's internal `:variant-name`, so the file fails backend referential-integrity validation: from then on **every component-touching mutation is rejected with an HTTP 400 the plugin never surfaces** — calls hang ~30 s, the session dies, unflushed mutations roll back. The same poison applies to `addVariant()` + rename, `comp.instance()` + `detach()` on a variant, `createComponent` on a detached variant instance, and `shape.remove()` on a variant board; recovery is manual. *Reading* variants and instancing a specific variant are safe. **Safe strategy:** build each state as a standalone Board and `createComponent([board])` **one at a time**, named `Component / State`; Phase 3 (§6) carries the duplicate-file / verify-saves / fallback procedure.
- Verify unfamiliar signatures with `penpot_api_info('VariantContainer')` / `penpot_api_info('Variants')` first.

## 5. Token-Aware Brief Contract
- **Context** — which design system / token sets are active; component purpose.
- **Objective** — single component + its variant axes.
- **Inputs** — base layout, the token set (`penpot-foundations`), required axes.
- **Constraints** — all values tokenized; all required states present; naming `Property=Value`.
- **Acceptance Criteria** — matrix complete; zero hardcoded values; every state legible & AA-contrast; names follow convention.

Act as a **senior component engineer**.

## 6. Mandatory Workflow

> **Visual self-review (mandatory):** before every ✋ checkpoint that shows visual work,
> run the export → look → fix loop from `shared/visual-self-review.md` — export the unit you
> just built, inspect the image yourself against the checklist, fix visible defects (max 2
> iterations), and present that same export with any remaining defects named.

**Phase 0 — Discovery.** `high_level_overview`; read tokens (`tokenOverview()`) and existing components. Decide axes (`references/01-variant-axes.md`). ✋ Checkpoint: confirm the axis matrix.

**Phase 1 — Base.** Build the base Board with flex layout, tokenized (`scripts/buildComponentBase.js`), then `createComponent`. ✋ Checkpoint: review base (`export_shape`).

**Phase 2 — Variants as components.** For each matrix cell, clone the base, retokenize per state, and
**`createComponent` it** — `createVariantFromComponents` needs a component *per* variant. Use
`scripts/createVariants.js` (collects each cell's main-instance id). ✋ Checkpoint: review the cells.

**Phase 3 — Group, name axes, organize.** ⚠️ **HIGH-RISK PHASE — read `shared/plugin-api-gotchas.md`
#12 first.** Mutating variant components (`setVariantProperty`, axis renames, detaching/removing
variants) has **corrupted files and hung all subsequent saves** in live sessions (the backend rejects
every save with an unsurfaced HTTP 400). Before this phase: ✋ Checkpoint — ask the user to **duplicate
the file** (or confirm they accept the risk on a scratch file). Then apply **one** variant mutation,
verify the file still saves (a later read-only call must succeed and persist), and only then continue.
If any call hangs ~30 s, **stop immediately** and switch to the fallback below.

The variant flow: `scripts/createVariantGroup.js` is **gated** — it returns `{ halted: true }` unless
`storage.cf.fileDuplicatedConfirmed === true` (set it in a prior call only after the user duplicated the
file and confirmed saves work). It then prefers
`penpotUtils.createVariantContainer(records.map(r => ({ shape: main, properties: r.properties })))`
(path `"helper"`, ≥ 2.17: axes + values in one call), falling back to `penpot.createVariantFromComponents`
+ `renameProperty`/`addProperty`/`setVariantProperty` (path `"legacy"`, kept verbatim in the script).
Either way it clears the container fill (#11), **gives the container a flex layout** (variants stack at
the same spot otherwise: `container.flex || container.addFlexLayout()`; row, gaps, padding, `wrap`) and
returns `{ containerId, path, properties, components, next }`. **Save verification:** after the call,
make a trivial change in the Penpot UI and confirm it persists before any further mutation — a ~30 s
hang means the file is poisoned; discard the duplicate and switch to the fallback below. ✋ Checkpoint.

**Fallback (always safe):** skip the variant container entirely. Keep the per-cell components from
Phase 2 as standalone components named `Component / Axis=Value, …` (e.g. `Button / Size=Medium,
State=Hover`), created **one at a time** with a flush pause between calls, arranged in a labeled grid.
Penpot groups them by the `/` prefix and the user can convert them to real variants in the UI later.

**Phase 4 — Validate.** `scripts/validateComponent.js` — every required state present, all values tokenized, naming correct. Optional `scripts/switchVariantDemo.js` to prove switching. Report.

## 7. Critical Rules
1. All interactive components include `Default/Hover/Pressed/Focus/Disabled` unless the system says otherwise.
2. Zero hardcoded values — bind to semantic (or component) tokens.
3. Variant property/value names: `Property=Value`, PascalCase (`Size=Medium`, `State=Hover`).
4. Build as a flex Board; never absolute-position children unless `layoutChild.absolute`.
5. Idempotent: don't duplicate an existing variant.
6. Detach only when necessary, and report it — **never** detach a variant instance (gotchas #12).
7. After grouping, give the variant container a flex layout — variants stack at the same position otherwise.
8. Variant mutation is a known file-corruption risk (gotchas #12): duplicate the file before Phase 3,
   verify saves after the first mutation, and fall back to standalone `Component / State` components
   if anything hangs.

## 8. Domain Architecture
Standard axes:
- `Size = Small | Medium | Large`
- `Hierarchy = Primary | Secondary | Tertiary`
- `State = Default | Hover | Pressed | Focus | Disabled`
- `Icon = None | Left | Right`

The matrix is the Cartesian product you need — keep it as small as the system allows (don't generate
combinations the design language doesn't use). Each variant is a cloned base with state-specific
**token** bindings.

## 9. Modes & Policies
Default **review**. Variant/component restructuring and `detach()` are **never** auto-applied
(`shared/modes-and-policies.md`).

## 10. State Management
Ledger keys under `RUN_ID`: `phase`, `baseComponentId`, `created:[{variant:'Size=Medium,State=Hover', id}]`. Re-derive with a component read after truncation.

## 11. User Checkpoints
| After phase | Artifacts shown | What we ask |
|-------------|-----------------|-------------|
| 0 | proposed axis matrix | Approve axes? |
| 1 | base `export_shape` | Approve base? |
| 2 | variant grid `export_shape` | Approve variants? |
| 3 | variant container | Approve combine? |

## 12. Naming Conventions
`shared/naming-conventions.md`: component PascalCase (`Button`); variant `Property=Value`; internal
layers semantic (`label`, `icon`, `button`).

## 13. Anti-Rationalization Table
| Excuse | Why it's wrong | Countermeasure (halt) |
|--------|----------------|------------------------|
| "I'll add hover/disabled later." | Incomplete components ship broken states. | All required states are acceptance gates; build them now. |
| "A plain rectangle is fine for this state." | Hardcoded shapes drift from the system. | Clone the base and bind state tokens. |
| "I'll hardcode the hover color." | Breaks theming and governance. | Use/propose a semantic token (`color.action.primary.hover.bg`). |
| "Absolute-position the icon, it's easier." | Fights flex; breaks resizing. | Use flex order + `layoutChild`; absolute only with `layoutChild.absolute` and a reason. |
| "I'll assume the variant-creation method/args." | Variant API is easy to get wrong. | Prefer `penpotUtils.createVariantContainer`; low-level `createVariantFromComponents` only when the helper is absent; verify with `penpot_api_info('Variants')`. Never `combineAsVariants` (unverified). |
| "Variant mutation worked once — I'll batch the rest in one call." | One bad `setVariantProperty` poisons the file silently; every later save hangs (gotchas #12). | One mutation → verify saves persist → continue. On any ~30 s hang, stop and use the standalone-components fallback. |

## 14. Helper Code Snippets
```js
// Base as a flex Board (Phase 1) — gaps/fill/padding bound to tokens (padding binds on ≥ 2.17; mirror + exception on 2.16.x, gotchas #8)
const board = penpot.createBoard();
board.name = "Button";
const flex = board.addFlexLayout();
flex.dir = "row";
flex.horizontalSizing = "auto"; flex.verticalSizing = "auto";

// gap binds to a token; padding binds on Penpot ≥ 2.17 — try applyToken per side, fall back to the RESOLVED value + a padding-mirrors-token exception
const gapTok = penpotUtils.findTokenByName("spacing.inset.sm");   // or propose it at the checkpoint
if (gapTok) board.applyToken(gapTok, ["columnGap"]);
const padY = penpotUtils.findTokenByName("spacing.8");
const padX = penpotUtils.findTokenByName("spacing.16");
penpot.currentPage.root.appendChild(board);                                     // append before binding layout props
const exceptions = [];
for (const [tok, sides, fallback] of [[padY, ["paddingTop", "paddingBottom"], 8], [padX, ["paddingLeft", "paddingRight"], 16]]) {
  for (const side of sides) {
    try { if (tok) board.applyToken(tok, [side]); else throw new Error("token missing"); }
    catch { flex[side.replace("padding", "").toLowerCase() + "Padding"] = tok ? Number(tok.resolvedValue) : fallback; exceptions.push({ kind: "padding-mirrors-token", token: tok && tok.name, side }); }
  }
}

// FILL POLICY: a button is a SURFACE — bind its bg token (never a literal, never the default white)
board.fills = [];
const bgTok = penpotUtils.findTokenByName("color.action.primary.bg");
if (bgTok) board.applyToken(bgTok, ["fill"]);

const label = penpot.createText("Button");
board.appendChild(label);
const comp = penpot.library.local.createComponent([board]);
return { component: comp.name, id: comp.mainInstance().id, exceptions };
```

## 15. Reference Resources
- `penpot_api_info('Board')`, `penpot_api_info('VariantContainer')`, `penpot_api_info('Variants')`, `penpot_api_info('LibraryComponent')`.

## 16. Supporting Files
**references/**: `01-variant-axes.md`, `02-flex-grid-layout.md`, `03-variant-api.md`, `04-instance-swap-detach.md`, `05-anti-rationalization.md`, `06-error-recovery.md`.
**scripts/**: `buildComponentBase.js`, `createVariants.js` (one component per cell), `createVariantGroup.js` (gated; helper ≥ 2.17 or legacy path), `switchVariantDemo.js`, `validateComponent.js`.

**Doctrine paths.** `shared/…` and `policies/…` resolve inside this bundle in native installs (vendored by the installer); in a Claude Code plugin install they live at the plugin root — `${CLAUDE_PLUGIN_ROOT}/shared/…`, two directories up from this file.
