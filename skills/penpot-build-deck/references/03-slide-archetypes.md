# 03 — Slide archetypes

Loaded during Phase 0 (outline) and by every `buildSlide.js` call. Catalog adopted from the
Anthropic pptx skill, Figma `figma-use-slides` and the SlideSpeak slide-design skill, sized for the
kit's 1920×1080 stage and 12-column grid.

## Shared geometry (every archetype)

- Board 1920×1080 named `NN-archetype-slug`, `clipContent = true`, `showInViewMode = true`; fill
  bound to `deck.bg.<tone>`; flex column, padding 96 (`deck.space.margin`, bound per side with a
  numeric mirror on failure), gap 48 (`deck.space.gutter`) → content area 1728×888.
- Inner containers: `header` (eyebrow row, 48 high), `body` (row or grid, fills the rest), `footer`
  (source line · slide number, caption size). All `fills = []` — the slide board is the only surface.
- Column spans (100 px columns, 48 px gutters): 2 = 248 · 3 = 396 · 4 = 544 · 5 = 692 · 6 = 840 ·
  7 = 988 · 8 = 1136 · 9 = 1284 · 12 = 1728. Two rows with a 48 gap = 420 each.
- **Anchor** = where the title block sits (`top-left` · `top-right` · `bottom-left` · `bottom-right`
  · `left` · `right` · `center`); the dominant visual takes the opposite side. Center only on
  cover, quote, closing.
- Flex for rows and columns; `board.addGridLayout()` + `board.grid.appendChild(cell, row, col)`
  (1-based) for anything ≥ 2×2; grid failure → nested flex rows (`09-error-recovery.md`).
- Every archetype consumes `CONTENT.title`; `CONTENT.eyebrow` and `NOTES` (hidden `notes` text
  layer) are always accepted. A `stats[].source` or `imageSlots[].credit` renders in `footer`.
- Every slide has ≥ 1 visual: the motif, a placeholder image, a stat rendered as display type, a
  grid of cards, or a decorative edge shape. Text alone never passes `auditDeckQuality.js`.

## Catalog

### 1 `cover`
- Purpose: first impression; carries the one message.
- Recipe: anchor `bottom-left` (default) or `center`; `h1` 8-col at title size (up to 120 in
  Bold-editorial), ≤ 2 lines; `eyebrow` above; author/date caption below; motif at the opposite
  corner (numeral 400–600 px clipped by the board edge, or corner glow). Dark tone.
- Density: title ≤ 8 words · eyebrow ≤ 6 · 1 caption line.
- Visual: motif, or full-bleed image with a 55–70 % dark overlay.
- Varies: anchor, motif corner. CONTENT: `title`, `eyebrow`, `body[0]` (subtitle), `imageSlots[0]`.

### 2 `agenda`
- Purpose: promise the structure; ≥ 8-slide decks only.
- Recipe: anchor `top-left`; `h1` at section size (44); list in a 6-col column, each item a row of
  numeral (section size, muted or accent) + label (body); the remaining 6 col hold the motif or a
  4-col placeholder. Never a centered vertical list.
- Density: 3–6 items, ≤ 5 words each.
- Visual: the oversized numerals themselves count; add the motif.
- Varies: numerals left vs. right, motif. CONTENT: `title`, `body[]` (items).

### 3 `section`
- Purpose: chapter divider; resets attention. Dark tone by default.
- Recipe: anchor `left` or `bottom-left`; section code (`eyebrow`, mono or tracked caps) + `h1` at
  title size, ≤ 6 words; ≥ 60 % of the stage stays empty; motif large (numeral 500–600 px clipped).
- Density: title + eyebrow + optional 1-line `body[0]`.
- Visual: motif at scale, or half-bleed image.
- Varies: anchor (rotate TL → BL → BR across dividers), numeral edge. CONTENT: `title`, `eyebrow`, `body[0]`.

### 4 `content-bullets`
- Purpose: a claim with 3–6 supporting points. The archetype most likely to breach the 40 % share.
- Recipe: anchor `top-left`; `h1` 8-col; `ul` in a 6- or 7-col column (≤ 60 chars per line), items as
  rows of marker (accent dot 12 px or numeral) + `p`; the other 5–6 col hold a placeholder image,
  a stat, or the motif. Never bullets spanning 12 col; never centered.
- Density: ≤ 6 bullets · ≤ 2 lines each · body 28–36.
- Visual: mandatory in the free column — never text-only.
- Varies: list left vs. right, marker style. CONTENT: `title`, `body[]`, `imageSlots[0]`, `stats[0]`.

### 5 `content-cards`
- Purpose: 2–4 parallel points that each need a label + short text.
- Recipe: anchor `top-left`; `h1` 12-col; row of cards, spans 6+6, 4+4+4, or 3+3+3+3 (never 5 cards);
  card = column flex, padding 48, gap 24, `deck.surface.card` on light profiles / glass on dark;
  label at section size, text at body. One card may be accent-filled to break symmetry.
- Density: 2–4 cards · ≤ 40 words per card.
- Visual: the cards; optional icon or numeral per card.
- Varies: card count, which card is emphasized, row vs. staggered heights. CONTENT: `title`, `columns[]` (`{label, text}`).

### 6 `big-number`
- Purpose: one figure the audience must remember.
- Recipe: anchor `left` or `bottom-left`; `stat` at 140–200 (`deck.font.size.stat`), tracking −2 %,
  ≤ 6 characters; `label` at section size directly below, ≤ 8 words; `source` line in `footer`
  (caption, muted). Up to 3 secondary stats at 72 in a 4-col column on the opposite side.
- Density: 1 hero stat · ≤ 3 secondary · every value carries `source`.
- Visual: the stat is the visual; add the motif small.
- Varies: hero left vs. right, secondary stats present or not. CONTENT: `title` (as claim), `stats[]` (`{value,label,source}`).

### 7 `two-column`
- Purpose: comparison or before/after.
- Recipe: anchor `top-left`; `h1` 12-col; two columns 6+6 (comparison) or 7+5 / 8+4 (argument +
  evidence); each column = `eyebrow` (column label) + `p` list; the emphasized column gets a
  surface or accent stroke, the other stays bare. A 1 px vertical rule between columns is allowed;
  a horizontal accent line under the title is not.
- Density: ≤ 4 points per column · ≤ 60 chars per line.
- Visual: emphasized column surface, or a placeholder image replacing one column.
- Varies: 6+6 vs. 8+4, emphasized side. CONTENT: `title`, `columns[]` (`{label, items[]}`).

### 8 `feature-grid`
- Purpose: 4–6 equal-weight features.
- Recipe: anchor `top-left`; `h1` 12-col; `addGridLayout()` 2×2 (cells 840×420) or 2×3 (544×420),
  gap 48; each cell = column flex with numeral or icon slot (48 px), label (section size), text (body).
  Cells transparent on Keynote/Editorial; cards on Corporate/Tech/Playful.
- Density: 4–6 cells · ≤ 25 words per cell.
- Visual: the grid; every cell has its numeral/icon slot filled.
- Varies: 2×2 vs. 2×3, cell surfaces vs. bare. CONTENT: `title`, `columns[]` (`{label, text}`).

### 9 `bento`
- Purpose: one dominant idea plus 2–3 supporting facts.
- Recipe: anchor `top-left`; `h1` 12-col; row 8+4 (dominant left 1136×888, right a 544 column of two
  420-high cells) or 4+4+4 with the middle cell spanning both rows; the dominant cell holds the
  image placeholder, the hero stat or the key claim at section size. Mirror (4+8) on the next use.
- Density: 3–4 cells · dominant cell ≥ 2× any other.
- Visual: the dominant cell (image or stat).
- Varies: 8+4 vs. 4+8 vs. 4+4+4, which cell is dominant. CONTENT: `title`, `columns[]`, `stats[]`, `imageSlots[]`.

### 10 `quote`
- Purpose: a human voice; a rhythm break.
- Recipe: anchor `center` or `left`; `blockquote` at section-to-title size (44–72) in a 8-col text
  box, ≤ 30 words, sentence case, no quotation-mark glyph larger than the text; attribution as
  `eyebrow` (name · role) below; a 4-col portrait placeholder or the motif on the free side.
- Density: 1 quote · 1 attribution.
- Visual: portrait placeholder or motif at scale.
- Varies: left vs. center, portrait vs. motif. CONTENT: `quote`, `eyebrow` (attribution), `imageSlots[0]`.

### 11 `timeline`
- Purpose: 3–5 dated milestones.
- Recipe: anchor `top-left`; `h1` 12-col; horizontal row of milestones, equal `fill` columns, each
  = date (`eyebrow`), marker (accent circle 16–24 px on a 2 px muted rule drawn as a row of
  rectangles, not a border), label (body); the current milestone gets the accent fill. Vertical
  variant (6-col list) when > 4 milestones.
- Density: ≤ 5 milestones · ≤ 6 words each.
- Visual: the rule + markers; motif small.
- Varies: horizontal vs. vertical, which milestone is emphasized. CONTENT: `title`, `steps[]` (`{date,label}`).

### 12 `process-steps`
- Purpose: an ordered procedure.
- Recipe: anchor `top-left`; `h1` 12-col; row of 3–5 step cards or bare columns, each = numeral
  (72, accent or muted) + label (section) + text (body); an arrow glyph between steps is optional
  and must be a text character, never a stretched line. Stagger vertically (steps descend 48 px
  each) once per deck.
- Density: ≤ 5 steps · ≤ 20 words per step.
- Visual: the numerals; optional icon slot.
- Varies: staggered vs. flat, numeral style. CONTENT: `title`, `steps[]` (`{label,text}`).

### 13 `image-bleed`
- Purpose: let one image carry the slide.
- Recipe: **half**: image column 50–60 % (960–1136 px) as an absolute child at page coords bleeding
  to three edges, copy in the remaining 6–7 col, anchor opposite; **full**: image covers the board,
  overlay rectangle 55–70 % `deck.bg.dark`, `h1` anchored `bottom-left` in on-dark text. Image =
  `img-placeholder` with label unless the user supplied a URL (`05-visuals-and-effects.md`).
- Density: title + ≤ 3 lines of body (half) · title + eyebrow (full).
- Visual: the image.
- Varies: half left vs. right vs. full. CONTENT: `title`, `body[]`, `imageSlots[0]` (`{url?, description, credit?}`).

### 14 `chart-placeholder`
- Purpose: a chart that will be pasted later; the title states the insight.
- Recipe: anchor `top-left`; `h1` = the claim ("Churn fell 38 % after month 2"), 8-col; chart area
  as `img-placeholder` 8-col × 600 labeled "CHART — <type>: <series>"; 4-col column with ≤ 3
  takeaways or 1–2 secondary stats; `source` in `footer`. Never draw fake bars with invented values.
- Density: 1 chart slot · ≤ 3 takeaways.
- Visual: the chart slot.
- Varies: chart left vs. right, takeaways vs. stats. CONTENT: `title`, `body[]`, `stats[]`, `imageSlots[0]` (`{description}`).

### 15 `closing`
- Purpose: repeat the one message, give the CTA and contact. Dark tone.
- Recipe: anchor `center` or `bottom-left`; `h1` at title size = the message (≤ 8 words); `p` with
  the CTA (verb-first, ≤ 5 words); contact / URL as caption; motif mirrored from the cover (other
  corner). No "Thank you" as the title — the message is the title, "Thank you" may be the eyebrow.
- Density: title + CTA + ≤ 2 contact lines.
- Visual: motif at scale, or the cover image reused.
- Varies: mirror of the cover's anchor. CONTENT: `title`, `eyebrow`, `body[]` (CTA, contact).

## Monotony rules

- Consecutive slides differ on ≥ 1 of archetype · anchor · tone. Same archetype twice in a row
  never passes, even with different content.
- No archetype exceeds 40 % of the deck. Six content slides in a 12-slide deck means at most four
  of one kind — rotate `content-bullets` → `content-cards` → `two-column` → `bento`.
- Anchor cycles: never the same anchor three slides running; `top-left` is the resting default and
  must be broken by a `left` / `bottom-left` / `right` at least every third slide.
- The motif varies (corner, scale, edge) every slide it appears on.
- `auditDeckQuality.js` reports `consecutiveSameArchetype[]` and `archetypeShare`; the critique
  (`07-critique-framework.md`) scores `consecutiveRepeats`, `distinctArchetypes`, `maxArchetypeShare`.
  Fix a monotony finding by changing the archetype of the later slide, not by shuffling content.
