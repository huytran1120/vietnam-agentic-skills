---
name: research
description: >-
  Investigate a question against high-trust primary sources and capture the findings as a Markdown
  file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or
  reading legwork delegated to a background agent.
category: "productivity"
risk: "safe"
source: "https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/research"
source_repo: "mattpocock/skills"
author: "Matt Pocock"
license: "MIT"
license_source: "https://github.com/mattpocock/skills/blob/5beb35b040e3de97e54fa9e386d7e42d15c295c2/LICENSE"
source_revision: "5beb35b040e3de97e54fa9e386d7e42d15c295c2"
source_path: "skills/engineering/research"
tags:
  - mattpocock
  - workflow
  - coding-agents
  - research
  - primary-sources
---
_Source: [Matt Pocock / skills](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/research), MIT, revision `5beb35b040e3`. See [UPSTREAM-NOTICE.md](UPSTREAM-NOTICE.md) for import changes._

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


Research directly unless the user requested delegation. When authorized, use a **background agent** while doing independent work.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.
