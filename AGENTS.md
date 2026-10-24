# Vietnam Agentic Skills (VAS) - Instructions for Antigravity

This repository is **Vietnam Agentic Skills (VAS)**, curated and maintained by **Huy Tran** (`huytran1120`).
It serves as a comprehensive catalog of 2,650+ modular, agentic skills specifically designed for **Google Antigravity**.

## Golden Rules for Agents

1. **Zero NPX / Zero External Dependencies**:
   - Never run `npx` or prompt the user to run `npx`.
   - All management, searching, listing, and installing must be performed using `./vas` or `python3 vas.py`.
2. **Progressive Disclosure**:
   - When introducing skills to an Antigravity project, do NOT dump thousands of full files into context.
   - Use `./vas install <skill_id> --target workspace --mode link` to install only the necessary skills into `.agents/skills/`.
   - Antigravity scans the YAML frontmatter (`name`, `description`) of installed skills and loads the full instructions on-demand.
3. **Skill Structure**:
   Every skill inside `skills/<skill_name>/` must follow Antigravity's standard convention:
   ```text
   skills/<skill_name>/
   ├── SKILL.md          # Required: Frontmatter (name, description, category, tags) + Runbook
   ├── scripts/          # Optional: Helper scripts (bash, python)
   ├── examples/         # Optional: Example inputs/outputs
   └── references/       # Optional: In-depth specifications and reference material
   ```

## Agent Runbook

- **To search for a skill**:
  `./vas search <keyword>`
- **To view a skill**:
  `./vas show <skill_id>`
- **To install into the current workspace**:
  `./vas install <skill_id> --target workspace --mode link`
- **To install globally into Antigravity**:
  `./vas install <skill_id> --target global`
- **To view status**:
  `./vas status`
- **To rebuild index after adding new skills**:
  `./vas sync`
