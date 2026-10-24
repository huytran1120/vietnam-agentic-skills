/**
 * auditDeckQuality.js
 * Purpose: the deck's STRUCTURAL gate (read-only, plus the idempotent flipX sweep). Runs before the
 *          scored critique (references/07-critique-framework.md). A non-`pass` result blocks "done".
 * Usage:   paste into execute_code once (Phase N+1, after wireDeckFlow.js). Re-run after fixes.
 * Input:   TYPE_FLOOR, BODY_MIN, SAFE, MAX_SHARE, REQUIRE_NOTES.
 * Output:  { slides, wrongDims, noVisual, belowTypeFloor, offSafeArea, placeholders, rawFills,
 *            consecutiveSameArchetype, archetypeShare, unlinkedSlides, flowPresent, flipCleared, pass }
 *          — the `structuralGate` object of shared/report-schemas/deck-quality-report.schema.json.
 */
const TYPE_FLOOR = 20;      // px — nothing visible below this
const BODY_MIN = 28;        // px — `p` layers at least this
const SAFE = 96;            // safe margin
const MAX_SHARE = 0.4;      // no archetype above 40 % of the deck
const REQUIRE_NOTES = false; // REPLACE-ME: true when the brief asked for speaker notes
const W = 1920, H = 1080;

const page = penpot.currentPage;
const slides = page.root.children
  .filter((c) => c.type === "board" && /^\d{2}-/.test(c.name))
  .sort((a, b) => parseInt(a.name.slice(0, 2), 10) - parseInt(b.name.slice(0, 2), 10));
if (!slides.length) return { pass: false, reason: "no slide boards (NN-…) on the current page" };

const wrongDims = [], noVisual = [], belowTypeFloor = [], offSafeArea = [], placeholders = [], rawFills = [], unlinkedSlides = [], missingNotes = [];
const PLACEHOLDER_RE = /lorem|REPLACE-ME|\bTBD\b|Item \d|John Doe/i;
const clearFlip = (sh) => { let n = 0; const walk = (s) => { if (s.flipX) { s.flipX = false; n++; } (s.children || []).forEach(walk); }; walk(sh); return n; };
let flipCleared = 0;

for (const s of slides) {
  if (Math.round(s.width) !== W || Math.round(s.height) !== H) wrongDims.push(`${s.name} (${Math.round(s.width)}×${Math.round(s.height)})`);
  flipCleared += clearFlip(s);
  let visual = 0, minFont = Infinity, hasNotes = false;
  penpotUtils.analyzeDescendants(s, (root, d) => {
    if (d.name === "notes") { hasNotes = true; return null; }
    if (d.hidden) return null;
    if (d.type === "text") {
      const fs = parseFloat(d.fontSize) || 0;
      minFont = Math.min(minFont, fs);
      if (fs && fs < TYPE_FLOOR) belowTypeFloor.push(`${s.name}/${d.name} ${fs}px`);
      if (d.name === "p" && fs && fs < BODY_MIN) belowTypeFloor.push(`${s.name}/${d.name} body ${fs}px < ${BODY_MIN}`);
      if (d.name === "stat" || d.name === "stat-value" || fs >= 140) visual++;
      if (PLACEHOLDER_RE.test(d.characters || "")) placeholders.push(`${s.name}/${d.name}: ${String(d.characters).slice(0, 40)}`);
    } else if (["rectangle", "ellipse", "path", "image", "svg-raw", "boolean"].includes(d.type) || d.name === "img-placeholder" || d.name === "chart-placeholder" || (d.fills || []).some((f) => f.fillImage) || (typeof d.isComponentInstance === "function" && d.isComponentInstance())) {
      visual++;
    }
    // Safe-area: anything visible whose bounds poke outside the slide's safe area (absolute decorations are exempt by name prefix `deco-` / bleeds).
    if (!/^(deco-|img-|chart-)/.test(d.name) && !(d.layoutChild && d.layoutChild.absolute)) {
      const b = d.bounds;
      if (b && (b.x < s.x + SAFE - 1 || b.y < s.y + SAFE - 1 || b.x + b.width > s.x + W - SAFE + 1 || b.y + b.height > s.y + H - SAFE + 1)) offSafeArea.push(`${s.name}/${d.name}`);
    }
    // Raw fills on surfaces: slide root or `card` boards without a fill token binding.
    if (d.type === "board" && (d.name === "card" || d.name.startsWith("card-")) && (d.fills || []).length && !(d.tokens && d.tokens.fill) && !(d.fills[0] && d.fills[0].fillColorGradient)) rawFills.push(`${s.name}/${d.name}`);
    return null;
  }, 10);
  if ((s.fills || []).length && !(s.tokens && s.tokens.fill) && !(s.fills[0] && s.fills[0].fillColorGradient)) rawFills.push(`${s.name} (slide bg)`);
  if (!visual) noVisual.push(s.name);
  if (REQUIRE_NOTES && !hasNotes) missingNotes.push(s.name);
}

// Variety / monotony.
const archetypes = slides.map((s) => s.name.split("-")[1]);
const consecutiveSameArchetype = [];
for (let i = 1; i < archetypes.length; i++) if (archetypes[i] === archetypes[i - 1]) consecutiveSameArchetype.push(`${slides[i - 1].name} → ${slides[i].name}`);
const counts = archetypes.reduce((m, a) => (m[a] = (m[a] || 0) + 1, m), {});
const maxArchetypeShare = Math.max(...Object.values(counts)) / slides.length;
const archetypeShare = Object.fromEntries(Object.entries(counts).map(([k, v]) => [k, +(v / slides.length).toFixed(2)]));

// Flow + reachability: every slide except the last needs a navigate-to to the next one.
const flowPresent = (page.flows || []).some((f) => f.name === ((storage.deck && storage.deck.flowName) || "Deck"));
for (let i = 0; i < slides.length - 1; i++) {
  const ok = (slides[i].interactions || []).some((it) => it.action && it.action.type === "navigate-to" && it.action.destination && it.action.destination.id === slides[i + 1].id);
  if (!ok) unlinkedSlides.push(slides[i].name);
}

const pass = !wrongDims.length && !noVisual.length && !belowTypeFloor.length && !consecutiveSameArchetype.length
  && maxArchetypeShare <= MAX_SHARE && flowPresent && !unlinkedSlides.length && !placeholders.length && !missingNotes.length;

const result = {
  slides: slides.map((s) => s.name), slideCount: slides.length,
  wrongDims, noVisual, belowTypeFloor, offSafeArea, placeholders, rawFills,
  consecutiveSameArchetype, archetypeShare, maxArchetypeShare: +maxArchetypeShare.toFixed(2), distinctArchetypes: Object.keys(counts).length,
  flowPresent, unlinkedSlides, missingNotes, flipCleared, pass,
  note: "offSafeArea and rawFills are advisory (report them); the other lists block `pass`.",
};
if (storage.deck) storage.deck.structuralGate = result;
return result;
