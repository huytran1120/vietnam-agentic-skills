# 01 — Deck brief analysis

Loaded during Phase 0 (discovery). Turns a talk request into an approved outline, a tonal arc and a
motif before any board exists. Nothing in this file touches the canvas.

## Extraction checklist

| Item | Pin down | If the brief is silent |
|---|---|---|
| Audience | who watches, what they already know, what they decide afterwards | ask — it sets tone, density and vocabulary |
| Occasion | pitch · keynote · internal review · lecture · conference talk | ask |
| Duration | minutes on stage → slide budget (below) | assume 15 min and state it |
| Screen | projector at distance · shared laptop · PDF-only read | assume projector; the 20 px floor holds in every case |
| Language | of the slides, not of the brief | the brief's language |
| The one message | one claim the audience must be able to repeat | draft a candidate; confirm at the checkpoint |
| Sections | 2–5 chapters, each with one claim | derive from the message |
| Data | every number **with its source** | a number without a source is not used (`shared/design-quality.md` §6) |
| Quotes | ≤ 30 words, with attribution | drop, or ask |
| Images | public URLs the user owns or licenses, or "placeholders" | labeled placeholders (`05-visuals-and-effects.md`) |
| Existing system | brand tokens, fonts present in `penpot.fonts.all`, logo component | `setupDeckSystem.js` aliases `deck.*` to what exists |
| Playback | click-only · auto-advance seconds · section flows · notes · PDF | click-only, notes on, PDF instructions at the end |

Read the file first: `high_level_overview`, `penpotUtils.tokenOverview()`, `penpot.fonts.all.map(f => f.name)`,
`penpot.pages.map(p => p.name)`. A page named `Deck — <title>` that already exists means a resume,
not a fresh build (`shared/state-management.md`).

## Slide budget

- Default ≈ 1 slide per 1–2 min: 10 min → 6–10 slides · 20 min → 12–18 · 45 min → 25–35.
- The brief's explicit count or cap wins over the rule. Say the resulting number at the checkpoint.
- More slides, not denser slides: when content exceeds a density limit (`03-slide-archetypes.md`),
  split into two slides. Never shrink body below 28 px or anything below 20 px to make it fit.
- Fixed positions: `01` cover · `02` agenda when the deck has ≥ 8 slides · last = closing.
  Section dividers count toward the budget.

## The one message

Write it as a claim in sentence case, ≤ 12 words ("Onboarding v2 doubled week-4 retention"). Every
slide title must support it; a slide that doesn't is cut or merged. The cover carries it verbatim or
shortened; the closing repeats it next to the CTA.

## Outline table — the Phase 0 deliverable

Format, one row per slide: `n | archetype | title (≤ 8 words) | key content | visual | tone`

| n | archetype | title | key content | visual | tone |
|---|---|---|---|---|---|
| 01 | cover | Onboarding v2 doubled retention | eyebrow "Q3 product review" · date | oversized "02" numeral clipped bottom-right | dark |
| 02 | agenda | Three things you will leave with | 3 items | numbered 6-col list, 4-col empty right | light |
| 03 | big-number | 2.1× week-4 retention | value 2.1×, label, source "Mixpanel cohort 2026-07" | the stat itself at 180 px | light |
| 04 | image-bleed | What changed on day one | 3 short lines | half-bleed placeholder "IMAGE — new welcome screen" | light |
| 05 | section | Why it worked | — | dark divider, numeral "01" motif | dark |

Rules: `archetype` comes from `03-slide-archetypes.md`; titles are claims, not categories
("Retention doubled" beats "Retention"); `visual` is never empty; `tone` ∈ `dark` | `light`. An
optional `anchor` column (`top-left` · `top-right` · `bottom-left` · `bottom-right` · `left` ·
`right` · `center`) may be added; if omitted, `buildSlide.js` ANCHOR is chosen at build time and must
still pass the variety rule. The approved table is stored in the ledger as `outline[]` and drives
every `buildSlide.js` call (INDEX, ARCHETYPE, SLUG, TONE, ANCHOR, CONTENT, NOTES).

## Tonal arc

Default: **dark cover → light body → dark section dividers → light body → dark closing**. Dark
slides bind `deck.bg.dark` + `deck.text.on-dark`; light slides `deck.bg.light` + `deck.text.on-light`.
Alternatives, stated at the checkpoint: all-dark (Keynote-minimal, Tech-dark-gradient) or a dark
cover with an all-light body (Corporate-clean). Record as ledger `tonalArc` (`"dark-light-dark"` ·
`"all-dark"` · `"cover-dark"`). Never alternate tone on every slide — that is flicker, not rhythm.

## Motif menu — pick exactly one, vary it

| Motif | Device | What varies slide to slide |
|---|---|---|
| Oversized numerals | slide number or key figure at 400–600 px, 6–10 % opacity, clipped by one edge | corner, size, which edge clips |
| Corner glow | one radial gradient anchored at a corner (`05-visuals-and-effects.md`) | corner, radius |
| Rotated tile | one rectangle rotated 8–15°, near an edge, accent or surface fill | edge, scale |
| Eyebrow + slide number | `eyebrow` top-left, `NN / total` top-right, caption size | eyebrow text only — the frame is the constant |
| Edge shapes | a circle or bar bleeding off one edge | edge, size, fill |
| Half-bleed image | image column 50–60 % of the stage | left/right, crop |
| Mono label | monospace caption for section codes (`01 / CONTEXT`) | content |

The motif appears on ≥ 60 % of slides and is never identical on two consecutive slides. Record it as
ledger `motif`.

## Variety pre-check — run on the outline, before building

1. No two consecutive rows share `archetype`.
2. Consecutive rows differ on ≥ 1 of archetype · anchor · tone.
3. No archetype exceeds 40 % of rows (`content-bullets` is the usual offender — convert to cards,
   two-column, big-number).
4. Every row has a `visual`.
5. Every run of 5 slides contains ≥ 1 rhythm break (big-number, quote, image-bleed or section).
6. Every stat names its source; every quote names its speaker.

Any failure → rewrite the outline now. Fixing variety mid-build costs one rebuilt slide per fix.

## Questions for the Phase 0 checkpoint

Present outline + style profile (`02-deck-styles.md`) + tonal arc + motif + slide budget, then ask
only what blocks the build:

- Is the one message right, and is the closing CTA the action you want?
- Confirm the slide count against the time slot (state the ratio used).
- Sources for stats X/Y are missing — provide them, or accept a labeled placeholder `— (source TBD)`?
- Images: URLs you own, or placeholders for now?
- Fonts: `<family>` is / is not in `penpot.fonts.all` — accept the exact fallback named?
- Playback: click-only, or auto-advance every N seconds? Section flows? Speaker notes?
- Which existing tokens should `deck.accent` / `deck.bg.*` alias to?

"Looks good" approves the outline only — name the next phase (`createDeckPage.js` create + verify,
then `setupDeckSystem.js`) before starting it.
