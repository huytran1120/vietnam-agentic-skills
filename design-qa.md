# VAS logo integration — 2026-10-26

Scope: selected logo option 3, header, dark theme, favicon and touch icon. The rest of the page retains its existing design.

## Visual truth and evidence

- Selected source: `/Users/huytran/.codex/generated_images/01a17381-eab8-7b81-991c-affd461b7a2f/exec-fe1abd07-8961-492d-a5b7-23fdcdb48608.png` (1487 × 1058 presentation board).
- Implemented mark: `docs/assets/brand/vas-monogram.png` (2010 × 782 transparent PNG), displayed at 84 × 34 CSS px on desktop and 58 × 26 on mobile; `object-fit: contain` preserves its proportions. At 320px viewport the mark uses a 48 × 24 box.
- Icon: `docs/assets/brand/vas-icon.png` (1254 × 1254 transparent-corner PNG), linked as favicon and touch icon.
- Full desktop evidence: `/Users/huytran/.codex/visualizations/2026/10/25/01a17381-eab8-7b81-991c-affd461b7a2f/vas-logo/desktop-full.jpg`.
- Full mobile evidence: `/Users/huytran/.codex/visualizations/2026/10/25/01a17381-eab8-7b81-991c-affd461b7a2f/vas-logo/mobile-full.jpg`.
- Focused light/dark evidence: `header-light.png` and `header-dark.png` in the same evidence directory.
- Source and rendered evidence were inspected together in one comparison input. Compare the mark, wordmark and descriptor, rather than the surrounding presentation board. The source is an identity board, not a website layout reference; pixel-for-pixel full-page matching is not applicable.
- Browser viewports: desktop default; mobile 390 × 844 and 320 × 760 CSS px. Full captures were assessed at their native scale, without stretching the logo. Mobile document width was 305px with a 320px viewport and scrollbar.

## Comparison history

1. [P2] Blue mark had weak contrast on the dark header. Fixed by rendering the same asset white with a CSS filter, matching the selected board's reversed application. Confirmed with `header-dark.png`.
2. [P2] At 320px, the longer mark displaced the menu and caused horizontal overflow (330px document width). Fixed by reducing the logo and wordmark size and hiding the descriptor below 380px. Confirmed in the full mobile capture, with both theme and menu controls visible and no document overflow.
3. Final review: the VAS ribbon geometry, detached A crossbar, blue/white applications, name and descriptor match the selected direction. No remaining P0/P1/P2 visual findings.

## Verification and limits

- Theme switching and mobile menu opening/closing tested in the browser.
- Browser console reported no errors.
- Existing page regression checks: 18/18 passed; asset references resolve locally.
- Favicon/touch-icon links point to the generated square asset; native iOS home-screen installation was not tested.
- P3 follow-up: the delivered assets retain full-resolution raster originals. A dedicated vector master and smaller web derivatives could reduce transfer size further.
- The original `docs/favicon.svg` remains available for compatibility but is no longer linked by this page.

final result: passed
