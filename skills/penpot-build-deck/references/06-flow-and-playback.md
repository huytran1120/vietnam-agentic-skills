# 06 — Flow and playback

Loaded during Phase N+1 (`wireDeckFlow.js`) and for the final checkpoint's playback and export
instructions. API facts verified on Penpot 2.17.

## Playback order = Layers-panel order

- Penpot View mode steps through the page's boards in the order of the Layers panel; ←/→ moves
  between them. The click interactions below make the deck play correctly regardless, but ←/→ and
  the PDF page order follow the panel.
- `wireDeckFlow.js` collects boards matching `^\d{2}-`, sorts by the numeric prefix and reorders
  them with `page.root.insertChild(index, board)`. Helper boards keep their place.
- **Verify the direction once per instance**: after wiring, open View mode on slide 01 and press →.
  If slide 02 follows, the panel maps to ascending child index; if the last slide follows, it maps
  to descending. Record the verdict in the ledger as `playbackOrder: "children-asc" | "children-desc"`;
  `wireDeckFlow.js` reads it and reverses the insert order on the next run. Do not assume.

## The `Deck` flow

```js
const page = penpot.currentPage;                       // createDeckPage.js PHASE=verify passed
const slides = page.root.children.filter(s => /^\d{2}-/.test(s.name)).sort((a, b) => a.name.localeCompare(b.name));
let flow = page.flows.find(f => f.name === "Deck");
if (flow && flow.startingBoard?.id !== slides[0].id) { flow.remove(); flow = null; }
if (!flow) flow = page.createFlow("Deck", slides[0]);
```

Idempotent: an existing flow with the right start is reused; a wrong start is removed and
recreated. Every flow has its own share link in View mode, so the flow name is user-facing.

## Interactions: click → navigate-to next

```js
const slideAnim = { type: "slide", way: "in", direction: "left", duration: 300, easing: "ease-out" };
const dissolve  = { type: "dissolve", duration: 400, easing: "ease-in-out" };
for (let i = 0; i < slides.length - 1; i++) {
  const next = slides[i + 1];
  const anim = /^\d{2}-section-/.test(next.name) ? dissolve : slideAnim;
  slides[i].addInteraction("click", { type: "navigate-to", destination: next, preserveScrollPosition: false, animation: anim });
}
```

- Trigger set: `'click' | 'mouse-enter' | 'mouse-leave' | 'after-delay'`. Only `click` and
  `after-delay` are used; hover triggers are refused (they fire on the presenter's mouse).
- Animation: `slide` for content-to-content (300 ms, `ease-out`, `way: "in"`, `direction: "left"` =
  the new slide enters from the right); `dissolve` when entering a `section` or the `closing`;
  `push` is allowed as the profile's stated alternative (Playful) but not mixed with `slide`.
  Duration 200–400 ms; never > 500.
- The interaction goes on the **board**, so a click anywhere advances. No "prev" hotspot: ←/→ are
  native. No "next" button drawn on the slide.
- Set every interaction in one call per 10 slides; read `slide.interactions.length` next call to
  verify. A destination id that no longer resolves → `09-error-recovery.md`.
- `wireDeckFlow.js` returns `{ flow, slides, interactions, sectionFlows[], reordered }`; the
  ledger stores `flowName` and `slides[].done = true` only after interactions verify.

## Optional auto-advance

`ADVANCE.afterDelayMs` set → add `slides[i].addInteraction("after-delay", { type: "navigate-to",
destination: next, animation: anim }, ADVANCE.afterDelayMs)` alongside the click interaction. Use
one delay for the whole deck (typical 8 000–15 000 ms); section dividers may take half. The closing
slide gets none. Tell the user auto-advance is on — a kiosk deck and a presented deck are different
deliverables.

## Section flows

`SECTION_FLOWS = true` → for each `NN-section-<slug>` board create `page.createFlow("Section: <Title
case slug>", sectionBoard)`. Each section flow shares the same interactions (they live on the
boards), so the presenter can start from any chapter and share a per-section link. Idempotent by name.

## Helper boards

Anything on the deck page that is not a slide (`Notes`, a `swatches` board, a master component
board) gets `showInViewMode = false` so it never appears in playback or ←/→ order. `auditDeckQuality.js`
reports `unlinkedSlides[]` — a `^\d{2}-` board without an incoming interaction — and any board
with `showInViewMode = true` that is not a slide.

## Speaker notes

Penpot has no native speaker notes. Kit convention: each slide holds a text layer named `notes`
(`hidden = true`, caption size, placed absolute at the slide's bottom-left inside the margin) with
the `NOTES` string from `buildSlide.js`. Hidden layers do not render in View mode or PDF. Fallback
when the user wants notes readable in one place: a `Notes` page with one text block per slide,
titled with the board name. Say which convention was used in the final report.

## Full-screen and share

- View mode: `Shift+F` toggles full-screen; ←/→ navigate; the flow selector (top-left) switches
  between `Deck` and `Section: …`.
- Share: View mode → Share → copy link; each flow can be shared separately. The link is created by
  the user in the UI — the plugin API does not expose it.

## PDF export (native, Penpot ≥ 2.12)

1. Design mode → select all slide boards (click `01-…`, shift-click the last; helper boards
   unselected).
2. Right panel → Export → add export → format **PDF** → Export. One PDF, one page per board, in
   Layers-panel order — verify the order after `wireDeckFlow.js` reordered.
3. Images and gradients export as rendered; hidden `notes` layers are omitted. Fonts are embedded
   from Penpot's font service — a font missing there prints as fallback, which is why #13b exact
   matching matters.

Give these steps verbatim at the final checkpoint; the plugin API cannot trigger the PDF export.

## Previews for checkpoints

`export_shape(<slideId>)` per slide, PNG; never `export_shape("page")` (Finding 7: http error on
whole-page export). A 1920×1080 export that fails with an http error on the remote MCP → retry
once, then export the slide's `body` container and note the truncation. Batch checkpoints show 3–5
slide exports, each already looked at (`shared/visual-self-review.md`).
