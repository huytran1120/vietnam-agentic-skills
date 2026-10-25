---
name: implement-spec
description: >-
  Implement the result of /to-spec and /to-tickets in code.
disable-model-invocation: true
category: "development"
risk: "critical"
source: "https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/implement-spec"
source_repo: "mattpocock/skills"
author: "Matt Pocock"
license: "MIT"
license_source: "https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/LICENSE"
source_revision: "5beb35b040e3de97e54fa9e386d7e42d15c295c2"
source_path: "skills/engineering/implement-spec"
tags:
  - mattpocock
  - workflow
  - coding-agents
  - implementation
  - specifications
---
_Source: [Matt Pocock / skills](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/implement-spec), MIT, revision `5beb35b040e3`. See [UPSTREAM-NOTICE.md](UPSTREAM-NOTICE.md) for import changes._

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


You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The issue tracker should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved the way the issue tracker closes work.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency.

## Steps

1. Read the spec and tickets to understand the task graph.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create the integration branch. If the issue tracker closes work through PRs, or the user asks for one, open a draft PR after the first merge in step 5 (a branch with no commits ahead of main can't open one), marked as closing the spec and tickets.

4. Use **implementer subagents** to implement each ticket, each in its own worktree on its own branch. Each implementer subagent:
   - confirms its isolated worktree is based on the integration branch before starting; if it is not, stops and requests a fresh worktree without resetting user work;
   - calls the Skill tool with `tdd` to build the ticket;
   - merges the integration branch tip into its own branch before reporting done

5. Once an **implementer subagent** completes, merge its work to the integration branch with a **merger subagent**.

6. If this changes the **frontier** of available tickets, kick off more **implementer subagents** to work on the new tickets. This allows for maximum concurrency.

7. Once all tickets are complete, call the Skill tool with `code-review` on the integration branch. Fix all issues raised by the code review in a single **implementer subagent**.

8. If a draft PR exists, mark it ready for review. Otherwise, resolve each ticket the way the issue tracker closes work, and report the integration branch.

9. Clean up all **implementer subagent** worktrees.
