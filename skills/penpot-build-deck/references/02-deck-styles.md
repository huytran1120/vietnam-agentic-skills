# 02 — Deck styles

Loaded during Phase 0, applied in Phase 1 (`setupDeckSystem.js`), frozen after slide 03. Profiles
adopted from the Anthropic pptx skill, Figma `figma-use-slides` and the SlideSpeak slide-design
skill, expressed in this kit's numbers.

Generic decks converge on a white board, default blue, a centered title with an accent line and
three equal cards. A profile is a set of numbers committed at Phase 0 so the critique
(`07-critique-framework.md`) can score against them. One profile per deck.

## The five profiles

| Row | Keynote-minimal | Bold-editorial | Tech-dark-gradient | Corporate-clean | Playful |
|---|---|---|---|---|---|
| Palette weights (bg / surface+text / accent) | 90 / 8 / 2 | 80 / 10 / ≤ 10 | 82 / 10 / 8 | 80 / 10 / 10 | 60 / 25 / 15 (2–3 saturated hues in blocks) |
| Background | near-black flat, L ≈ 8–12 %, no gradient | paper L ≈ 97 %, warm-neutral (not cream) | dark base L ≈ 10 % + **one** radial glow anchored at an edge | light neutral L ≈ 96–98 % with a whisper of brand hue | flat saturated blocks; one full-bleed accent slide every 4–6 |
| Type pairing (size / weight) | one sans · title 88 / 600 · body 32 / 400 | display serif or grotesk · title 96–120 / 700 on cover, section, closing · 96 / 700 elsewhere · body 32 / 400 | one geometric sans + mono for `eyebrow` · title 80 / 600 · body 32 / 400 | one humanist sans · title 72 / 600 · body 28–32 / 400 | one wide or rounded sans · title 96 / 800 · body 32 / 500 |
| Title tracking | −2 % | −2 % (−3 % at ≥ 110) | −2 % | −1.5 % | −1 % |
| Radius `deck.radius.card` | 0 — no cards | 0 | 24 | 16 | 32 |
| Elevation | none — space separates | none — rules and whitespace | 1 level: glass card (white 8 % + `backgroundBlur` 24 + 1 px stroke 12 %) | 1 soft shadow on cards only | none — contrast blocks |
| Motif | oversized numerals | half-bleed image + pull-quotes, 70/30 asymmetry | corner glow + glass cards | eyebrow + slide number | rotated tile or edge shapes |
| Tonal arc | all-dark | cover-dark, paper body | all-dark | cover-dark or dark-light-dark | dark-light-dark, accent blocks count as dark |
| Refuse | cards, shadows, icons, accent used more than once per slide | centered body, 50/50 symmetry, gradients | glow in the center, a second glow, glass on light | decorative bars, stock bleeds, accent above 10 % | pastels, weights < 500, drop shadows, a 4th hue |

Sizes live inside the scale of `04-typography-and-grid.md` (stat 140–200 · title 72–96 · section
40–48 · body 28–36 · caption 20–24 · floor 20). Bold-editorial's 110–120 titles are the only
sanctioned exception, and only on cover / section / closing.

## Refused on every profile

Accent lines under titles · decorative bars or stripes · centered body text · default blue
(`#0066FF`, `#1E90FF`, the Office/Google blues) · cream backgrounds · text-only slides · the same
layout on two consecutive slides · pure `#000` / `#FFF` · italic titles · more than 2 families or
3 weights · more than one accent hue (Playful excepted, capped at 3).

## Commit to one

1. Pick from audience + occasion: investor or sales pitch → Bold-editorial or Tech-dark-gradient ·
   internal review → Corporate-clean · conference keynote → Keynote-minimal · consumer launch →
   Playful. Brand tokens bend the profile's values; the profile never overrides the brand.
2. Say it at the Phase 0 checkpoint with numbers: "Tech-dark-gradient — title 80/600, body 32,
   radius 24, one glow bottom-right, glass cards, all-dark, motif corner glow".
3. Record `deckStyle` in the ledger. Slides 01–03 are the **style freeze**: after the user approves
   them no profile number moves. A change after the freeze re-exports slides 01–03 for re-approval.

## How a profile maps to `deck.*` tokens

`setupDeckSystem.js` creates the set `deck` once (idempotent, `toggleActive`); the profile supplies
values, or `ALIAS_TO_EXISTING` points a token at the brand (`deck.accent → "{color.brand.500}"`).
Alpha colors are 8-digit hex strings; every token `value` is a string (`shared/plugin-api-gotchas.md` #8).

| Token | Keynote-minimal | Bold-editorial | Tech-dark-gradient | Corporate-clean | Playful |
|---|---|---|---|---|---|
| `deck.bg.dark` | `#121214` | `#1A1917` | `#0B0F1A` | brand dark, L ≈ 12 % | brand dark, saturated |
| `deck.bg.light` | = `deck.bg.dark` (all-dark) | `#F6F4EF` | = `deck.bg.dark` | `#F7F8FA` | `#F4F4F8` |
| `deck.text.on-dark` | `#F2F2F2` | `#F3F1EC` | `#EEF2FF` | `#F7F8FA` | `#FAFAFA` |
| `deck.text.on-light` | = on-dark | `#1A1917` | = on-dark | `#1B1F2A` | `#161616` |
| `deck.text.muted` | `#F2F2F299` | `#1A19178C` | `#EEF2FF99` | `#1B1F2A8C` | `#16161699` |
| `deck.accent` | one hue, ≤ 2 % of area | one warm hue | one electric hue | brand primary | 2–3 hues (`deck.accent`, `deck.accent.2`, `deck.accent.3`) |
| `deck.surface.card` | unused | unused | `#FFFFFF14` | `#FFFFFF` | accent block |
| `deck.surface.glass` | — | — | `#FFFFFF14` (+ blur, literal) | — | — |
| `deck.surface.placeholder` | `#F2F2F21A` | `#1A191714` | `#EEF2FF1A` | `#1B1F2A14` | `#1616161A` |
| `deck.font.size.title` | `88` | `96` | `80` | `72` | `96` |
| `deck.font.size.body` | `32` | `32` | `32` | `30` | `32` |
| `deck.radius.card` | `0` | `0` | `24` | `16` | `32` |

Constant across profiles: `deck.font.size.stat` 180 · `section` 44 · `caption` 22 ·
`deck.space.margin` 96 · `gutter` 48 · `stack` 24 · `deck.font.family.display|body` = the two exact
family names verified in `penpot.fonts.all` (#13b). Gradients, glass blur and shadows cannot bind to
tokens — they are literals recorded in the ledger `exceptions` (`shared/visual-effects.md`).
