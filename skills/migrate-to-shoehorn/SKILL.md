---
name: migrate-to-shoehorn
description: >-
  Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user
  mentions shoehorn, wants to replace `as` in tests, or needs partial test data.
category: "testing"
risk: "safe"
source: "https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/misc/migrate-to-shoehorn"
source_repo: "mattpocock/skills"
author: "Matt Pocock"
license: "MIT"
license_source: "https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/LICENSE"
source_revision: "5beb35b040e3de97e54fa9e386d7e42d15c295c2"
source_path: "skills/misc/migrate-to-shoehorn"
tags:
  - mattpocock
  - workflow
  - coding-agents
  - typescript
  - test-data
---
_Source: [Matt Pocock / skills](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/misc/migrate-to-shoehorn), MIT, revision `5beb35b040e3`. See [UPSTREAM-NOTICE.md](UPSTREAM-NOTICE.md) for import changes._

## VAS integration

This VAS adaptation takes precedence over the upstream process below.
Use only the scope the user requested. Delegate work, publish tracker changes or
pull requests, install dependencies, and create persistent hooks only when the
user has authorized those actions. Otherwise work directly or prepare a draft.
Use the current client's available tools; named upstream slash commands are
skill references, not a guarantee that a command or integration is installed.
Preserve existing user work and configuration.

Manage catalog discovery and installation with `./vas` or `python3 vas.py`.
Dependencies named by the workflow are prerequisites for the target project,
not dependencies of the VAS catalog manager.


# Migrate to Shoehorn

## Why shoehorn?

`shoehorn` lets you pass partial data in tests while keeping TypeScript happy. It replaces `as` assertions with type-safe alternatives.

**Test code only.** Never use shoehorn in production code.

Problems with `as` in tests:

- Trained not to use it
- Must manually specify target type
- Double-as (`as unknown as Type`) for intentionally wrong data

## Install

```bash
npm install --save-dev @total-typescript/shoehorn
```

## Migration patterns

### Large objects with few needed properties

Before:

```ts
type Request = {
  body: { id: string };
  headers: Record<string, string>;
  cookies: Record<string, string>;
  // ...20 more properties
};

it("gets user by id", () => {
  // Only care about body.id but must fake entire Request
  getUser({
    body: { id: "123" },
    headers: {},
    cookies: {},
    // ...fake all 20 properties
  });
});
```

After:

```ts
import { fromPartial } from "@total-typescript/shoehorn";

it("gets user by id", () => {
  getUser(
    fromPartial({
      body: { id: "123" },
    }),
  );
});
```

### `as Type` → `fromPartial()`

Before:

```ts
getUser({ body: { id: "123" } } as Request);
```

After:

```ts
import { fromPartial } from "@total-typescript/shoehorn";

getUser(fromPartial({ body: { id: "123" } }));
```

### `as unknown as Type` → `fromAny()`

Before:

```ts
getUser({ body: { id: 123 } } as unknown as Request); // wrong type on purpose
```

After:

```ts
import { fromAny } from "@total-typescript/shoehorn";

getUser(fromAny({ body: { id: 123 } }));
```

## When to use each

| Function        | Use case                                           |
| --------------- | -------------------------------------------------- |
| `fromPartial()` | Pass partial data that still type-checks           |
| `fromAny()`     | Pass intentionally wrong data (keeps autocomplete) |
| `fromExact()`   | Force full object (swap with fromPartial later)    |

## Workflow

1. **Gather requirements** - ask user:
   - What test files have `as` assertions causing problems?
   - Are they dealing with large objects where only some properties matter?
   - Do they need to pass intentionally wrong data for error testing?

2. **Install and migrate**:
   - [ ] Install: `npm install --save-dev @total-typescript/shoehorn`
   - [ ] Find test files with `as` assertions: `grep -r " as [A-Z]" --include="*.test.ts" --include="*.spec.ts"`
   - [ ] Replace `as Type` with `fromPartial()`
   - [ ] Replace `as unknown as Type` with `fromAny()`
   - [ ] Add imports from `@total-typescript/shoehorn`
   - [ ] Run type check to verify
