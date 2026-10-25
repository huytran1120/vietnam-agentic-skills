# Vietnam Agentic Skills (VAS) - Instructions for AI Agents

This repository is **Vietnam Agentic Skills (VAS)**, curated and maintained by **Huy Tran** (`huytran1120`).
It serves as a comprehensive catalog of 2,921+ modular, agentic skills designed for **Google Antigravity, Claude Code, Cursor, Windsurf (Codeium), OpenAI Codex / OpenCode, Cline / Roo Code, and GitHub Copilot CLI**.

## Golden Rules for Agents

1. **Zero NPX / Zero External Dependencies**:
   - Never run `npx` or prompt the user to run `npx`.
   - All management, searching, listing, and installing must be performed using `./vas` or `python3 vas.py`.
2. **Progressive Disclosure**:
   - Do NOT dump thousands of full files into prompt context.
   - Use `./vas install <skill_id> --target <agent> --mode link` to install only the necessary skills.
   - AI Agents scan the YAML frontmatter (`name`, `description`) of installed skills and load full instructions on-demand.
3. **Skill Structure**:
   Every skill inside `skills/<skill_name>/` follows the Open Agent Skills specification (`agentskills.io`):
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
  - Antigravity / Universal: `./vas install <skill_id> --target antigravity --mode link`
  - OpenAI Codex: `./vas install <skill_id> --target codex --mode link`
  - Claude Code: `./vas install <skill_id> --target claude --mode link`
  - Cursor: `./vas install <skill_id> --target cursor --mode link`
  - Windsurf: `./vas install <skill_id> --target windsurf --mode link`
  - Cline / Roo Code: `./vas install <skill_id> --target cline --mode link`
  - GitHub Copilot CLI: `./vas install <skill_id> --target copilot --mode link`
  - All Agents: `./vas install <skill_id> --target all`
- **To view status**:
  `./vas status --target <agent>`
- **To rebuild index after adding new skills**:
  `./vas sync`
