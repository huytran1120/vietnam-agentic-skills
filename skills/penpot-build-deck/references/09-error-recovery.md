# 09 — Error recovery (decks)

Loaded when a call throws, returns an empty result, or an export looks wrong. Gotcha numbers refer
to `shared/plugin-api-gotchas.md`; Finding numbers to `docs/mcp-api-findings.md`.

| Symptom | Cause | Recovery |
|---|---|---|
| Slide board appeared on `Page 1`, not on `Deck — <title>` | `createBoard()` targets the current page context; `openPage()` is async (#15) | A board created on the wrong page **cannot be moved** (Finding 9). Delete it (`shape.remove()`), run `createDeckPage.js` PHASE=verify until `penpot.currentPage.id === storage.deck.pageId`, then recreate. If verify keeps failing, stop and ask the user to switch page in the UI. |
| `createDeckPage.js` verify fails after a plugin restart | `storage` wiped, focus reset (#15) | Re-find the page by name (`penpot.pages.find(p => p.name === …)`), `openPage`, verify in the next call, rebuild `storage.deck` from the ledger. |
| `uploadMediaUrl` throws or `fills[0].fillImage` is undefined next call | CORS, 403, file size, private host, timeout | Restore `img-placeholder` fill + label; push `{ kind: "image-upload-failed", url, reason }` to `exceptions[]`; report at the checkpoint; do not retry more than once. |
| `addGridLayout()` throws or `grid.appendChild(cell, row, col)` misplaces cells | Grid API unavailable on this build, or rows/columns not set before append | Set `grid.rows`/`grid.columns` first; on failure rebuild the archetype as nested flex rows (2×2 → column of two rows) and note `gridFallback: true` in the slide's ledger entry. |
| `addInteraction` throws `Value not valid` or destination missing | Stale shape reference from an earlier call; wrong action shape | Re-find both boards by name in this call; action must be `{ type: "navigate-to", destination: board, animation }`; verify `penpot_api_info("Shape","addInteraction")`. |
| `createFlow` says the flow already exists | Previous run created `Deck` | Reuse via `page.flows.find`; remove and recreate only when the starting board differs. |
| `export_shape(slideId)` returns an http error | Remote MCP export size/time limit at 1920×1080 | Retry once; then export the slide's `body` container and state the truncation; never `export_shape("page")` (Finding 7). |
| Text renders serif/mono or wrong family | `findByName` substring match (#13b) or family absent from `penpot.fonts.all` | Resolve with `fonts.all.find(f => f.name === "…")`; fall back in this exact order, stating the swap: Inter → Work Sans → Source Sans 3 → Roboto (sans); Source Serif 4 → Lora (serif); JetBrains Mono → Source Code Pro (mono). |
| Title/body size reverted after styling | `applyToText` reset `fontSize`/`lineHeight`/`letterSpacing` (#13b) | Re-assert the three properties after `applyToText`; bind `deck.font.size.*` afterwards; read back next call. |
| Whole slide or a card renders mirrored | `layoutChild` fill expansion set `flipX` (#16) | Run `clearFlip(slide)` (`shared/visual-effects.md`); re-export. Prevent by `resize()`-ing rows to their span before appending children. |
| Text clipped at 1 line or overflowing its box | `resize()` forced `growType = "fixed"` (#3) | Set `text.growType = "auto-height"` after every resize. |
| Geometry reads stale (heights 0, bounds wrong) right after a build | Layout not flushed | `await slide.waitForLayoutUpdate()` (#17) before reading `height`/`bounds`; if `await` is unavailable, read in the next call. |
| Padding token throws `Value not valid` | Penpot 2.16 (#8, Finding 8) | Set numeric `flex.topPadding…` = 96 and push `{ kind: "padding-mirrors-token", token: "deck.space.margin" }` to `exceptions[]`. |
| Slide fill stays white / token not on `shape.tokens` | Token apply is async and flaky on some shape types (#2) | Verify in the next call; re-apply to the same property; never fall back to a literal hex. |
| Decorative shape invisible | Absolute child positioned with parent-relative numbers (#14), or appended to a clipped inner container | Recompute with page coords (`board.x + offset`); append to the slide board itself. |
| `auditDeckQuality.js` reports `unlinkedSlides[]` | Slide added after `wireDeckFlow.js` ran | Re-run `wireDeckFlow.js` (idempotent); verify interactions next call. |
| `consecutiveSameArchetype[]` non-empty | Outline changed during the build | Rebuild the later slide with a different archetype (`buildSlide.js`, same INDEX, new ARCHETYPE); update `outline[]`. |
| Lost place after truncation | No ledger read | Read the `RUN_ID` ledger; `slides[].done` tells the next INDEX; re-`openPage` and verify before building. |

## Recovery protocol (before any row above)

1. **Re-orient.** Read the `RUN_ID` ledger (`shared/state-management.md`): `deckPageId`, `deckStyle`,
   `outline[]`, `slides[].done`, `exceptions[]`. Never rebuild from memory of earlier calls.
2. **Verify the page.** `penpot.currentPage.id === storage.deck.pageId` (or the ledger's
   `deckPageId`) in the current call; if not, `openPage` and return — verify in the next call.
3. **Re-find by name, not by id.** After a restart every stored shape reference is dead; the board
   names `NN-archetype-slug` and the layer names (`h1`, `p`, `img-placeholder`, `notes`) are the
   stable handles. `buildSlide.js` is idempotent by board name, so re-running an INDEX is safe.
4. **Fix the smallest thing.** One targeted `execute_code` per defect, then `clearFlip`,
   `await waitForLayoutUpdate()`, `export_shape(slideId)`, look. Max 2 self-corrections per slide
   (`shared/visual-self-review.md`); a third failure is presented to the user with the defect named.
5. **Record it.** Every recovery that changed the deliverable (placeholder instead of image, grid
   fallback, padding mirror, font swap) goes to `exceptions[]` and into the final report.
