/**
 * wireDeckFlow.js
 * Purpose: make the boards a DECK — order the slide boards, create the flow "Deck" starting at slide
 *          01, add click → navigate-to(next) interactions (+ optional after-delay auto-advance) with a
 *          slide animation, and one flow per section slide. Penpot View mode plays boards in
 *          Layers-panel order and ←/→ walk them; the flow gives the deck a start + a share link.
 * Usage:   paste into execute_code once (Phase N+1), idempotent — re-run after adding slides.
 * Input:   FLOW_NAME, ADVANCE, ANIMATION, SECTION_ANIMATION, SECTION_FLOWS.
 * Output:  { flow, slides, interactions, sectionFlows, reordered, playOrderNote }.
 * Note:    verify Page.createFlow / Shape.addInteraction with penpot_api_info on a new instance.
 *          Layers-panel order vs. children index direction is verified live once and stored in
 *          storage.deck.capabilities.playOrder ("index-asc" | "index-desc") — check View mode after
 *          the first run and set it if the deck plays backwards.
 */
const FLOW_NAME = "Deck";                                                // REPLACE-ME
const ADVANCE = { click: true, afterDelayMs: null };                     // REPLACE-ME: e.g. afterDelayMs: 8000 for auto-advance
const ANIMATION = { type: "slide", way: "in", direction: "left", duration: 300, easing: "ease-out" }; // REPLACE-ME
const SECTION_ANIMATION = { type: "dissolve", duration: 300, easing: "ease-in-out" };
const SECTION_FLOWS = true;                                              // REPLACE-ME
const PLAY_ORDER = (storage.deck && storage.deck.capabilities && storage.deck.capabilities.playOrder) || "index-asc";

const page = penpot.currentPage;
if (!(storage.deck && storage.deck.verified && page.id === storage.deck.pageId)) {
  return { halted: true, reason: "Deck page not verified as current — run createDeckPage.js PHASE=verify first." };
}

// 1. Collect + order slides by their NN prefix.
const slides = page.root.children
  .filter((c) => c.type === "board" && /^\d{2}-/.test(c.name))
  .sort((a, b) => parseInt(a.name.slice(0, 2), 10) - parseInt(b.name.slice(0, 2), 10));
if (slides.length < 2) return { error: "need at least 2 slides named NN-archetype-slug" };

// 2. Reorder page children so the deck plays 01 → NN (Layers-panel order = play order).
const ordered = PLAY_ORDER === "index-desc" ? [...slides].reverse() : slides;
let reordered = 0;
ordered.forEach((s, i) => {
  if (page.root.children[i] !== s) { try { page.root.insertChild(i, s); reordered++; } catch (e) { try { s.setParentIndex(i); reordered++; } catch {} } }
});

// 3. Flow "Deck" from slide 01 (idempotent).
let flow = (page.flows || []).find((f) => f.name === FLOW_NAME);
if (!flow) flow = page.createFlow(FLOW_NAME, slides[0]);
else if (flow.startingBoard && flow.startingBoard.id !== slides[0].id) flow.startingBoard = slides[0];

// 4. Interactions: click → next (and optional auto-advance). Clear ours first so re-runs don't stack.
let interactions = 0;
for (let i = 0; i < slides.length; i++) {
  const cur = slides[i], next = slides[i + 1];
  for (const it of [...(cur.interactions || [])]) {
    if (it.action && it.action.type === "navigate-to") { try { cur.removeInteraction(it); } catch {} }
  }
  if (!next) continue;
  const anim = next.name.split("-")[1] === "section" ? SECTION_ANIMATION : ANIMATION;
  if (ADVANCE.click) { cur.addInteraction("click", { type: "navigate-to", destination: next, animation: anim }); interactions++; }
  if (ADVANCE.afterDelayMs) { cur.addInteraction("after-delay", { type: "navigate-to", destination: next, animation: anim }, ADVANCE.afterDelayMs); interactions++; }
}

// 5. Section flows — one per `section` slide, named after the slide's title text if present.
const sectionFlows = [];
if (SECTION_FLOWS) {
  for (const s of slides) {
    if (s.name.split("-")[1] !== "section") continue;
    const h1 = penpotUtils.findShape((c) => c.type === "text" && c.name === "h1", s);
    const name = `Section: ${h1 ? h1.characters.slice(0, 40) : s.name.slice(3)}`;
    if (!(page.flows || []).some((f) => f.name === name)) { page.createFlow(name, s); sectionFlows.push(name); }
  }
}

// 6. Helper boards (not slides) should not show in View mode.
for (const c of page.root.children) if (c.type === "board" && !/^\d{2}-/.test(c.name) && "showInViewMode" in c) c.showInViewMode = false;

storage.deck.flowName = FLOW_NAME;
try {
  const runId = storage.deck.runId || "RUN_ID_HERE";
  const led = JSON.parse(penpot.currentFile.getSharedPluginData("penpot-ai", runId + ".ledger") || "{}");
  Object.assign(led, { phase: 4, flowName: FLOW_NAME, sectionFlows, playOrder: PLAY_ORDER });
  penpot.currentFile.setSharedPluginData("penpot-ai", runId + ".ledger", JSON.stringify(led));
} catch {}

return {
  flow: { id: flow.id, name: flow.name, start: slides[0].name },
  slides: slides.map((s) => s.name), interactions, sectionFlows, reordered,
  playOrderNote: "Open View mode (G V) and press → once. If the deck plays backwards, set storage.deck.capabilities.playOrder = \"index-desc\" and re-run.",
};
