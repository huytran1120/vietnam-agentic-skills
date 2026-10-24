# 06 — Error recovery (components)

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `createComponent` returns nothing useful | Passed wrong shapes / empty array | Pass the base Board in an array: `createComponent([board])`. |
| Children jump around after layout | Flex overriding x/y | Order via append; use `layoutChild`; set `absolute` only intentionally. |
| `createVariantContainer` / `createVariantFromComponents` errors | Wrong arg / not main-instances | Prefer `penpotUtils.createVariantContainer([{ shape: mainInstance, properties }])` (≥ 2.17); the low-level `createVariantFromComponents(Board[])` needs component MAIN INSTANCES. `Board.combineAsVariants(ids)` is listed on 2.17 but unverified — do not use. |
| `switchVariant` no effect | Wrong position index/value | Read `Variants.properties` order; match value casing exactly. |
| Variant looks unstyled | Token applied but read too soon | Token application is async; verify in a later call. |
| Duplicate variants on re-run | No idempotency | Check existing variant descriptors before cloning. |
| Instance edits affect main | Mutated attached instance | `detach()` first (and report it). |
