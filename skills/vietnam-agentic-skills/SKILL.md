---
name: vietnam-agentic-skills
category: workflow
risk: safe
tags:
  - antigravity
  - agentic-skills
  - vietnam
  - installer
description: >-
  Search, discover, and install curated agentic skills from the Vietnam Agentic Skills (VAS)
  catalog into Google Antigravity workspaces or global configurations without npx.
  Use when the user or agent needs specialized playbooks for security, devops, testing,
  fullstack, ai-ml, cloud, database, or workflow optimization.
---

# Vietnam Agentic Skills (VAS) for Google Antigravity

Vietnam Agentic Skills provides 2,951+ modular playbooks (`SKILL.md`) ready to be discovered and loaded by Google Antigravity.

## When to Use This Skill

Activate this skill when:
- The user asks for a skill, playbook, or runbook for a specific technology (e.g. Docker security, React Native, Kubernetes deployment, Next.js optimization).
- The user asks to search, browse, or install skills into their Antigravity workspace or global profile.
- You need a proven, step-by-step checklist or domain-specific guideline to carry out complex development tasks.

## Commands (Zero NPX)

All commands run through the native Python 3 CLI `./vas` (or `python3 vas.py`) with zero external dependencies:

### 1. Search for a Skill
```bash
./vas search <keyword>
# Example:
./vas search docker-security
```

### 2. View Skill Details and Instructions
```bash
./vas show <skill_id>
# Example:
./vas show 007
```

### 3. Install to Current Workspace (.agents/skills)
```bash
./vas install <skill_id> --target workspace --mode link
```
> [!TIP]
> Using `--mode link` creates symbolic links, requiring zero extra disk space and staying automatically up-to-date with this repository.

### 4. Install Globally for Antigravity (~/.gemini/antigravity/skills)
```bash
./vas install <skill_id> --target global
```

### 5. Batch Install by Category or Tag
```bash
./vas install --category security --target workspace
./vas install --tag python --target workspace
```

### 6. Check Installed Skills
```bash
./vas status
```

### 7. Remove an Installed Skill
```bash
./vas uninstall <skill_id>
```

## How Antigravity Uses Installed Skills

1. Antigravity monitors the `.agents/skills/` directory in the active workspace and `~/.gemini/antigravity/skills/` globally.
2. It reads only the YAML frontmatter (`name`, `description`) during startup to preserve context tokens (**progressive disclosure**).
3. When the user prompt matches a skill description, Antigravity loads the full `SKILL.md` into memory and follows its specialized runbook.
