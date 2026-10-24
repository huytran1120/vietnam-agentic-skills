/**
 * applyDeckEffects.js
 * Purpose: apply the deck's atmospheric/visual devices to ONE slide — a gradient background, a glass
 *          card, a shadow, an image placeholder, or a real image from a USER-SUPPLIED URL. Every
 *          literal the token API cannot express is recorded in the ledger `exceptions`
 *          (shared/visual-effects.md). Image uploads are async + fallible: verify in the NEXT call.
 * Usage:   paste into execute_code after buildSlide.js for that slide (Phases 2..N); one slide per call.
 * Input:   SLIDE_ID, EFFECTS[].
 * Output:  { applied, failed, verifyNext } — then run the "verify" snippet in the next call.
 * Note:    gotchas #18 (image fills), #11 (surfaces only), #14 (absolute children); verify shapes of
 *          Gradient / Shadow / Blur with penpot_api_info before first use on a new instance.
 */
const SLIDE_ID = storage.deck && storage.deck.slides.length ? storage.deck.slides[storage.deck.slides.length - 1].id : "SLIDE_ID_HERE"; // REPLACE-ME
const EFFECTS = [                                                             // REPLACE-ME
  // { kind: "gradient", target: "bg", type: "linear", from: "#0B1020", to: "#1B2A4A", derivedFrom: ["deck.bg.dark", "deck.accent"] },
  // { kind: "gradient", target: "deco-glow", type: "radial", from: "#4F7CFF", to: "#4F7CFF", fromOpacity: 0.35, toOpacity: 0, derivedFrom: ["deck.accent"] },
  // { kind: "glass", target: "card", blur: 24, opacity: 0.08 },
  // { kind: "shadow", target: "card", level: 2 },
  // { kind: "image-url", target: "img-placeholder", url: "https://…/hero.jpg", name: "hero" },   // URL supplied by the USER only
  // { kind: "image-placeholder", target: "img-placeholder", description: "team photo" },
];

const slide = penpotUtils.findShapeById(SLIDE_ID);
if (!slide) return { error: `slide ${SLIDE_ID} not found` };
const findTarget = (name) => name === "bg" ? slide : penpotUtils.findShape((s) => s.name === name, slide);
const applied = [], failed = [], verifyNext = [];
const ledgerException = (e) => { storage.deck.exceptions = [...(storage.deck.exceptions || []), e]; };

for (const fx of EFFECTS) {
  const target = findTarget(fx.target);
  if (!target) { failed.push({ ...fx, reason: "target not found" }); continue; }
  try {
    if (fx.kind === "gradient") {
      const radial = fx.type === "radial";
      target.fills = [{
        fillOpacity: 1,
        fillColorGradient: radial
          ? { type: "radial", startX: 0.5, startY: 0.5, endX: 0.5, endY: 1, width: 1, stops: [{ color: fx.from, opacity: fx.fromOpacity ?? 1, offset: 0 }, { color: fx.to, opacity: fx.toOpacity ?? 0, offset: 1 }] }
          : { type: "linear", startX: 0, startY: 0, endX: 1, endY: 1, width: 1, stops: [{ color: fx.from, opacity: fx.fromOpacity ?? 1, offset: 0 }, { color: fx.to, opacity: fx.toOpacity ?? 1, offset: 1 }] },
      }];
      ledgerException({ kind: "gradient-literal", shape: target.id, slide: slide.name, stops: [fx.from, fx.to], derivedFrom: fx.derivedFrom || [] });
      applied.push({ kind: fx.kind, target: target.name });
    } else if (fx.kind === "glass") {
      target.fills = [{ fillColor: "#FFFFFF", fillOpacity: fx.opacity ?? 0.08 }];
      target.strokes = [{ strokeColor: "#FFFFFF", strokeOpacity: 0.12, strokeWidth: 1, strokeAlignment: "inner" }];
      if ("backgroundBlur" in target) { target.backgroundBlur = { type: "layer-blur", value: fx.blur ?? 24 }; storage.deck.capabilities.backgroundBlur = "works"; }
      else { storage.deck.capabilities.backgroundBlur = "missing"; }
      ledgerException({ kind: "glass-literal", shape: target.id, slide: slide.name, detail: `white @ ${fx.opacity ?? 0.08}, blur ${fx.blur ?? 24}` });
      applied.push({ kind: fx.kind, target: target.name });
    } else if (fx.kind === "shadow") {
      const lv = fx.level === 1 ? { offsetY: 2, blur: 8, opacity: 0.08 } : { offsetY: 8, blur: 24, opacity: 0.12 };
      target.shadows = [{ style: "drop-shadow", offsetX: 0, offsetY: lv.offsetY, blur: lv.blur, spread: 0, color: { color: "#0B1020", opacity: lv.opacity } }];
      ledgerException({ kind: "shadow-literal", shape: target.id, slide: slide.name, detail: `level ${fx.level || 2}` });
      applied.push({ kind: fx.kind, target: target.name });
    } else if (fx.kind === "image-url") {
      if (!fx.url || !/^https:\/\//.test(fx.url)) { failed.push({ ...fx, reason: "only user-supplied https URLs" }); continue; }
      const img = await penpot.uploadMediaUrl(fx.name || target.name, fx.url);       // async (gotcha #18)
      target.fills = [{ fillOpacity: 1, fillImage: img }];
      const cap = penpotUtils.findShape((s) => s.name === "caption", target); if (cap) cap.hidden = true;
      target.name = fx.name ? `img-${fx.name}` : "img";
      verifyNext.push(target.id);
      applied.push({ kind: fx.kind, target: target.name, url: fx.url });
    } else if (fx.kind === "image-placeholder") {
      const cap = penpotUtils.findShape((s) => s.name === "caption", target);
      if (cap) cap.characters = `IMAGE — ${fx.description || "describe the image here"}`;
      applied.push({ kind: fx.kind, target: target.name });
    } else {
      failed.push({ ...fx, reason: "unknown kind" });
    }
  } catch (e) {
    failed.push({ ...fx, reason: String(e) });
    if (fx.kind === "image-url") ledgerException({ kind: "image-upload-failed", slide: slide.name, url: fx.url, reason: String(e) });
  }
}

storage.deck.pendingImages = verifyNext;
return {
  applied, failed, verifyNext,
  next: verifyNext.length
    ? "NEXT CALL: for each id in storage.deck.pendingImages check `penpotUtils.findShapeById(id).fills[0].fillImage` — if missing, restore the placeholder + ledger {kind:'image-upload-failed'}; then export_shape(slide)"
    : "export_shape(slide) → look → fix (max 2 iterations)",
};

/* ---- verify snippet (paste as the NEXT execute_code call when verifyNext was non-empty) ----
const results = (storage.deck.pendingImages || []).map((id) => {
  const s = penpotUtils.findShapeById(id);
  const ok = !!(s && s.fills[0] && s.fills[0].fillImage);
  if (!ok && s) { s.fills = []; const cap = penpotUtils.findShape((c) => c.name === "caption", s); if (cap) cap.hidden = false; s.name = "img-placeholder";
    storage.deck.exceptions.push({ kind: "image-upload-failed", shape: id, reason: "fillImage missing after upload" }); }
  return { id, ok };
});
storage.deck.capabilities.uploadMediaUrl = results.every((r) => r.ok) ? "works" : "failed";
storage.deck.pendingImages = [];
return results;
--------------------------------------------------------------------------------------------- */
