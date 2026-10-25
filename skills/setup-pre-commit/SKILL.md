---
name: setup-pre-commit
description: >-
  Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the
  current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged,
  or add commit-time formatting/typechecking/testing.
category: "devops"
risk: "critical"
source: "https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/misc/setup-pre-commit"
source_repo: "mattpocock/skills"
author: "Matt Pocock"
license: "MIT"
license_source: "https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/LICENSE"
source_revision: "5beb35b040e3de97e54fa9e386d7e42d15c295c2"
source_path: "skills/misc/setup-pre-commit"
tags:
  - mattpocock
  - workflow
  - coding-agents
  - git-hooks
  - linting
---
_Source: [Matt Pocock / skills](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/misc/setup-pre-commit), MIT, revision `5beb35b040e3`. See [UPSTREAM-NOTICE.md](UPSTREAM-NOTICE.md) for import changes._

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


# Setup Pre-Commit Hooks

## What This Sets Up

- **Husky** pre-commit hook
- **lint-staged** running Prettier on all staged files
- **Prettier** config (if missing)
- **typecheck** and **test** scripts in the pre-commit hook

## Steps

### 1. Detect package manager

Check for `package-lock.json` (npm), `pnpm-lock.yaml` (pnpm), `yarn.lock` (yarn), `bun.lockb` (bun). Use whichever is present. Default to npm if unclear.

### 2. Install dependencies

Install as devDependencies:

```
husky lint-staged prettier
```

### 3. Initialize Husky

```bash
./node_modules/.bin/husky init
```

This creates `.husky/` dir and adds `prepare: "husky"` to package.json.

### 4. Create `.husky/pre-commit`

Write this file (no shebang needed for Husky v9+):

```
./node_modules/.bin/lint-staged
npm run typecheck
npm run test
```

**Adapt**: Replace `npm` with detected package manager. If repo has no `typecheck` or `test` script in package.json, omit those lines and tell the user.

### 5. Create `.lintstagedrc`

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

### 6. Create `.prettierrc` (if missing)

Only create if no Prettier config exists. Use these defaults:

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "printWidth": 80,
  "singleQuote": false,
  "trailingComma": "es5",
  "semi": true,
  "arrowParens": "always"
}
```

### 7. Verify

- [ ] `.husky/pre-commit` exists and is executable
- [ ] `.lintstagedrc` exists
- [ ] `prepare` script in package.json is `"husky"`
- [ ] `prettier` config exists
- [ ] Run `./node_modules/.bin/lint-staged` to verify it works

### 8. Commit

If the user requested a commit, stage only this task's files and commit with message: `Add pre-commit hooks (husky + lint-staged + prettier)`

This will run through the new pre-commit hooks: a good smoke test that everything works.

## Notes

- Husky v9+ doesn't need shebangs in hook files
- `prettier --ignore-unknown` skips files Prettier can't parse (images, etc.)
- The pre-commit runs lint-staged first (fast, staged-only), then full typecheck and tests
