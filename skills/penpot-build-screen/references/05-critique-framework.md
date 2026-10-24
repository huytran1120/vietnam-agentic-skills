# 05 — Critique framework (scored)

Before declaring a screen done, run the scored critique from `shared/design-quality.md` §8. This is
no longer a free-prose checklist: it produces a **1–5 score on seven axes**, a structured report,
and — when any axis fails — a bounded revision loop. It runs *after* the structural gate
(`auditScreenQuality.js`) and the visual self-review (`shared/visual-self-review.md`), and scores
the same final export those steps produced.

## The seven axes

Anchors: **1** = a named tell *is* the design · **3** = competent but interchangeable ·
**5** = deliberate, distinctive, consistent.

| Axis | The question | Doctrine |
|---|---|---|
| `hierarchy` | Eye lands on the user's goal first; exactly one primary action | §1, §3 |
| `composition` | Named skeleton executed, dominant element present, real alignment | §5 |
| `typography` | Scale contrast, line heights by role, measure, casing | §2 |
| `color` | Accent budget, near-neutrals, accent owned by the CTA, feedback reserved | §3 |
| `spacing` | Gap ladder, proximity rule (between ≥ 2× within), section rhythm | §4 |
| `content` | Honest, realistic, verb-first labels, empty/error states covered | §6 |
| `distinctiveness` | Recognizable vs. the average output for this brief; zero §7 tells | §7 |

## Procedure

1. Score each axis **against the export image** — every score cites evidence visible in the export
   or the shape tree. A score without evidence is invalid; a 3 without evidence of competence is a 2.
2. Any axis **< 3** → one targeted revision pass on the flagged shapes, re-export, re-score.
   Maximum **2 passes** (same bound as the visual self-review). Still < 3? Stop and present the
   export with the weak axes named — never silently accept, never round up.
3. Record findings with stable ids (`dq-<axis>-NN`); on workflow iterations, diff against the
   previous report's ids — call out fixed, still-open, and newly introduced.

## Output

Emit **both**, per `shared/report-schemas/design-quality-report.schema.json`:

- A short Markdown critique for the user: what works, what's weak, concrete fixes — and a one-line
  justification of the aesthetic decisions (profile, skeleton, accent placement).
- The JSON report object (returned from the final `execute_code` assembly step and mirrored to the
  run ledger). Include the derived `belowThreshold` field — `brief-to-screen`'s exit branch reads
  it, together with the accessibility report's `highOrMedium`.

Contrast checks stay with `penpot-audit-accessibility` — this critique scores *design* quality; it
does not re-audit WCAG.
