---
name: agent-skills-spec
category: workflow
risk: safe
tags:
  - agentskills
  - specification
  - standard
  - skill-creator
  - validation
description: >-
  Official Agent Skills format specification, authoring doctrine, and validation standards
  from the open Agent Skills standard (agentskills.io). Use when creating, structuring,
  evaluating, or validating skills for Google Antigravity, Claude, or other agent systems.
---

# Agent Skills Format Specification & Authoring Standard

This skill encapsulates the official [Agent Skills open specification](https://agentskills.io) created for modular AI agent extensibility.

## Core Structure of an Agent Skill

Every agent skill lives in its own dedicated directory matching its `name` attribute:

```text
<skill-name>/
├── SKILL.md          # Required: Frontmatter (name, description) + instructions
├── scripts/          # Optional: Executable automation code (Python, Bash, Node)
├── references/       # Optional: In-depth domain manuals, specs, or checklists
└── assets/           # Optional: Templates, diagrams, boilerplate files
```

## Frontmatter Specification

The `SKILL.md` file MUST begin with YAML frontmatter bounded by `---`:

| Field | Required | Constraints & Description |
| :--- | :---: | :--- |
| `name` | **Yes** | Max 64 chars. Lowercase letters, numbers, single hyphens. Must match directory name. |
| `description` | **Yes** | Max 1024 chars. Precise summary of **what** the skill does and **when** the agent should activate it. |
| `category` | No | Architectural category (e.g. `security`, `devops`, `workflow`). |
| `tags` | No | List of searchable keywords for discovery. |
| `risk` | No | Operational risk level: `safe`, `general`, `critical`. |
| `license` | No | SPDX license identifier or reference to bundled license file. |
| `compatibility` | No | Max 500 chars. Environment requirements (OS, packages, tools). |

## The Three Stages of Progressive Disclosure

1. **Discovery (Startup)**: Antigravity reads ONLY `name` and `description` to index capabilities while preserving token context.
2. **Activation (Matching)**: When a user's task matches the description, Antigravity injects the full `SKILL.md` body into context.
3. **Execution (Runbook)**: The agent executes procedures step-by-step, loading `references/` or running `scripts/` only on-demand.

## Validating a Skill

To validate any skill directory against this specification, run the bundled zero-dependency validator:

```bash
python3 skills/agent-skills-spec/scripts/validate.py skills/<skill_name>
```

## Reference Documentation

- [Complete Format Specification](references/specification.md)
- [Authoring Best Practices](references/best-practices.md)
- [Optimizing Skill Descriptions for Recall](references/optimizing-descriptions.md)
- [Evaluating Skills & Regression Testing](references/evaluating-skills.md)
- [Bundling & Executing Helper Scripts](references/using-scripts.md)
