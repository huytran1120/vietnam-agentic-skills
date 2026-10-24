# 05 — Visuals and effects

Loaded during Phases 2–N (slide builds) whenever a slide needs more than type. Recipes (gradient
API shape, glass card, shadow object, image fill, `clearFlip`) live in `shared/visual-effects.md`;
this file says where and how much on a slide. Applied through `applyDeckEffects.js`
(`EFFECTS[{ target, kind: "gradient" | "glass" | "shadow" | "image-url" | "image-placeholder", params }]`).

## Budget per slide

| Effect | Allowed on | Max per slide | Profiles |
|---|---|---|---|
| Radial glow (gradient) | the slide board's fill or one absolute rectangle behind everything | 1 | Tech-dark-gradient; optional on Playful accent slides |
| Linear gradient | image overlays only | 1 | any, as overlay |
| Glass card | cards on **dark** tone only | 4 | Tech-dark-gradient |
| Shadow | cards on **light** tone only, 1 level | 4 | Corporate-clean |
| Image (URL or placeholder) | `img` / `img-placeholder` | 2 | any |
| Decorative edge shape | absolute child of the slide board | 2 | Playful, Keynote (numerals), Editorial |
| Blur / blend modes | never on text; `blendMode` only for image tints | 1 | any |

Every gradient, blur and shadow is a literal (no token binding exists) → `applyDeckEffects.js` pushes
`{ slide, target, kind: "gradient-literal" | "shadow-literal" | "blur-literal", value }` to the
ledger `exceptions[]`. `penpot-audit-tokens` will flag them; the exception is the agreed answer.

## Glow: one, at an edge, never centered

- Radial gradient on the slide board (`fillColorGradient`, `type: "radial"`), center pinned to a
  corner or edge midpoint: `startX/startY` ∈ {0, 1} on at least one axis. A glow at (0.5, 0.5) is
  the "AI hero" tell — refused.
- Stops: accent at 18–28 % opacity → transparent by offset 0.6–0.7; `width` 0.8–1.2 of the board.
- The glow corner moves with the motif (cover bottom-right → section top-left → closing bottom-left)
  but stays on the same edge family across a section.
- Because the board fill is then a literal gradient, keep `deck.bg.dark` bound on the **first** fill
  entry and the gradient as the second entry where the API allows two fills; if it does not, record
  the exception and keep the tone in the ledger `slides[].tone`.

## Glass cards (dark tone only)

Fill `deck.surface.glass` (white 6–10 %), `backgroundBlur` 16–32 (24 default), 1 px stroke white
12 %, radius `deck.radius.card`. Glass needs something behind it to blur — a glow or image; on a
flat dark board it reads as a grey rectangle: add the glow first. Never glass on a light board.

## Shadows (light tone only)

One level: `{ color: deck.text.on-light, opacity 0.08–0.12, offsetY 8–16, blur 24–40, spread 0 }`
(exact object per `penpot_api_info("Shadow")`). All cards on a slide share it; a second, heavier
level is reserved for a single emphasized card. No shadows on Keynote-minimal, Bold-editorial, Playful.

## Placeholder image spec

- Rectangle named `img-placeholder`, fill bound to `deck.surface.placeholder`, radius
  `deck.radius.card`, sized to its column span (4-col 544 · 6-col 840 · 8-col 1136 · half-bleed
  960–1136 · full 1920×1080).
- Centered label text `IMAGE — <description>` (or `CHART — <type>: <series>`), 20–24 px,
  `deck.text.muted`, sentence case after the dash; the description comes from
  `CONTENT.imageSlots[i].description`, never "Image here".
- A placeholder is a visual for the purposes of `hasVisual`; it is also listed in the final report
  so the user knows what to replace.

## Real images: `uploadMediaUrl`, two-call verification

1. Only URLs the user supplied. No stock, no guessed CDN paths, no hot-linked logos.
2. Call A (`applyDeckEffects.js` kind `image-url`): `const img = await penpot.uploadMediaUrl(name, url);
   target.fills = [{ fillOpacity: 1, fillImage: img }];` — the target is the `img-placeholder` rect,
   renamed to `img`. Returns `verifyNext[]` with the shape ids.
3. Call B: read `shape.fills[0].fillImage` for each id, then `export_shape` the slide and look
   (`shared/visual-self-review.md`). A missing `fillImage` or a blank export = failure.
4. Failure (CORS, 403, size, timeout) → restore the placeholder fill, keep the label, push
   `{ kind: "image-upload-failed", url, reason }` to `exceptions[]`, tell the user in the checkpoint.
   Never retry a URL more than once in a session.
5. Cropping: the fill covers the rectangle; choose the rectangle's aspect (16:9, 4:5 portrait,
   1:1) for the slot, not the image's.

## Decorative shapes near edges

- Create the shape, append it to the **slide board** (not an inner container), then set
  `layoutChild.absolute = true` and position with **page coordinates**: `board.x + offset`,
  `board.y + offset` (#14). Set `absolute` only after `appendChild` (#15).
- Deliberate clipping is the point: a 560 px numeral at `board.x + 1920 − 320` shows 320 px and
  clips the rest because `clipContent = true`. Always confirm in the export — a shape placed with
  parent-relative numbers lands off-page and is invisible.
- Opacity 6–12 % for numerals and tiles on the same tone; full accent for small edge shapes.
- Never over text: an edge shape's bounds must not intersect any text shape's bounds. Check with
  `bounds` before the export.

## Executing the tonal arc

- `TONE` from the outline row → `buildSlide.js` binds `deck.bg.<tone>` and picks `deck.text.on-<tone>`;
  no per-slide literal colors.
- A dark slide following a light one uses the same accent hue; the glow/motif carries the
  continuity. A section divider takes the cover's treatment, mirrored.
- Light body slides get no glow; dark slides get no shadow. Mixing both on one slide fails `07`'s
  `color` axis.

## After every slide

Run `clearFlip(slide)` from `shared/visual-effects.md` (gotcha #16), `await slide.waitForLayoutUpdate()`
(#17), then `export_shape(slideId)` and look before the next slide. Never `export_shape("page")`
(Finding 7).
