# 07 — Critique framework (scored, deck)

Loaded during Phase N+1, after `auditDeckQuality.js` (structural gate) and the per-slide visual
self-review have passed. Axes adopted from `shared/design-quality.md` §8 and redefined for decks
with doctrine from the Anthropic pptx skill, Figma `figma-use-slides` and the SlideSpeak
slide-design skill. It scores the **exports** of every slide, 1–5 on seven axes, plus a
deck-level monotony check, and produces Markdown + JSON.

## The seven axes

Anchors: **1** = a named tell *is* the slide · **3** = competent but interchangeable · **5** =
deliberate, distinctive, consistent with the committed profile.

| Axis | The question | Evidence at 1 | Evidence at 3 | Evidence at 5 |
|---|---|---|---|---|
| `hierarchy` | Does each slide have one thing the eye lands on first, and is it the claim? | title and body at 44/40; three equal cards under a centered title | title clearly first, but the visual competes on 2+ slides | on every slide one dominant element (stat, image, title) ≥ 2× the next; reading order matches the outline |
| `composition` | Full canvas used? Asymmetry? Anchor varies? | content huddled in the center 900 px; every slide `top-left` | grid respected, 50/50 splits, anchor changes twice in 12 slides | 70/30 splits, bleeds and clipped motif use the edges; anchor rotates per `03` rules |
| `typography` | Real scale difference, exact fonts, measure, casing, floor? | fallback serif rendered (#13b); body 24; title at body line-height | scale holds, one title wraps to 3 lines, a 62-char line | stat 180 / title 88 / body 32 read at a glance; ≤ 60 chars; −2 % tracking; no text < 20 |
| `color` | 60/30/10 held? One accent? Tonal arc executed? | default blue accent line under titles; cream background | accent ≤ 10 % but on icons *and* stats; arc flat (all light) | accent owned by the one emphasized element per slide; dark/light arc visible in the contact sheet |
| `spacing` | 24/48/96 ladder, 96 margin, proximity rule? | text touching the board edge; uniform 32 gaps | margins held, gap ladder uniform inside cards | within < between < region; footer source line sits on the margin; nothing off safe area |
| `content` | Honest, sourced, dense within limits, claim titles? | invented "+47 %"; "Lorem"; 9 bullets | sourced stats, category titles ("Results") | every title is a claim; every stat carries a source line; ≤ 6 bullets; quote ≤ 30 words |
| `distinctiveness` | Zero AI-slide tells; one motif, varied; would this deck be recognized next to the average? | accent bars, centered body, identical layouts, stock-photo bleed | clean but motif-less; could be any company | motif on ≥ 60 % of slides and never identical twice; profile numbers traceable in every slide |

## Deck-level monotony check

Computed from the ledger `slides[]` (not eyeballed), reported in `monotony`:

| Field | Definition | Threshold |
|---|---|---|
| `consecutiveRepeats` | count of `i` where `slides[i].archetype === slides[i+1].archetype` | 0 |
| `distinctArchetypes` | number of distinct archetypes used | ≥ 5 for decks ≥ 8 slides; ≥ 3 below |
| `maxArchetypeShare` | max(count of one archetype) / `slideCount` | ≤ 0.40 |
| `slideCount` | slides with `^\d{2}-` and `showInViewMode = true` | = outline length |

Any threshold missed caps `distinctiveness` at 2 and adds a finding with `slide` = the first
offending index. Consecutive slides that also share anchor **and** tone add a `composition`
finding at Medium.

## Procedure

1. Score against the **slide exports** produced in Phases 2–N (re-export any slide changed since).
   Every score cites a slide number and what is visible there or in the shape tree. A score
   without evidence is invalid; a 3 without evidence of competence is a 2.
2. Score the deck, not the average slide: one slide at 1 on an axis drags the axis to ≤ 2.
3. Any axis **< 3** → one targeted revision pass on the flagged slides only (`buildSlide.js` on the
   same INDEX is idempotent by name, or `applyDeckEffects.js` for effect-only fixes), re-export,
   re-score. Maximum **2 passes**. Still < 3 → stop and present the exports with the weak axes
   named. Never round up. Never rebuild the deck.
4. Findings use stable ids `dk-<axis>-NN` and carry `slide` (the board index) so workflow
   iterations (`brief-to-deck`) diff cleanly: fixed · still open · newly introduced.
5. Contrast is not re-scored here — `penpot-audit-accessibility` `scope:deck` owns it.

## Output

Emit both, per `shared/report-schemas/deck-quality-report.schema.json`:

- **Markdown critique** for the user: three lines on what works, the weak axes with slide numbers,
  concrete fixes, and one line justifying the aesthetic decisions (profile, tonal arc, motif,
  anchor rotation). Include the contact-sheet mental picture: which slides are dark, where the
  motif sits.
- **JSON** returned from the final `execute_code` and mirrored to the ledger `deckQuality`:
  `runId, scope, deckStyle, tonalArc, outline[], axes[7]{axis, score, evidence, fix?},
  monotony{consecutiveRepeats, distinctArchetypes, maxArchetypeShare, slideCount},
  structuralGate{pass, noVisual, belowTypeFloor, offSafeArea, unlinkedSlides},
  belowThreshold, findings[]{id, severity, axis, slide, tell?, shapeId?, issue, measured?, target?, fix},
  revisionPasses ≤ 2, truncation`.
- `belowThreshold` = count of axes < 3; `brief-to-deck` exits only when it is 0 **and**
  `structuralGate.pass` is true **and** the accessibility report's `highOrMedium` is 0.

## Anti-rationalization (critique)

| Excuse | Why it's wrong | Countermeasure (halt) |
|---|---|---|
| "Every slide passed self-review, the deck is fine." | Self-review checks defects per slide; monotony and arc only exist at deck level. | Run the monotony check and score the axes on the set. |
| "Scoring 3 across the board is safe." | A flat score dodges revision and names no evidence. | Each score cites a slide number and a visible fact. |
| "The user asked for 12 content slides — repetition is their choice." | The count is theirs; the archetype rotation is yours. | Rotate bullets / cards / two-column / bento; report the share. |
