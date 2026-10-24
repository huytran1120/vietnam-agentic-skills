# 04 — Component migration

## Mapping
- Figma **component** → Penpot component (`createComponent([board])`).
- Figma **component set** (variants) → Penpot variant container: prefer `penpotUtils.createVariantContainer([{ shape: mainInstance, properties: { Size: "Medium" } }])` (≥ 2.17); `penpot.createVariantFromComponents(mainInstances)` as the low-level fallback. `Board.combineAsVariants(ids)` is listed by `penpot_api_info` on 2.17 but unverified — do not use.
- Figma variant properties → Penpot `Property=Value` (PascalCase).

## Process
1. For each IR component, build the base Board with flex per the IR layout, bind tokens.
2. For variant sets, build each variant Board, then combine into a container (verify API with `penpot_api_info`).
3. Preserve required interactive states; if Figma omitted some, flag rather than invent.
4. Reuse `penpot-component-factory` patterns for matrices and validation.

## Fidelity
Record any Figma feature that doesn't map cleanly (e.g. certain constraints, boolean interactions) as a
gap for the validation report.
