# 🇻🇳 Vietnam Agentic Skills (VAS) - English Edition

<p align="center">
  <a href="README.md#vietnamese"><b>🇻🇳 Tiếng Việt</b></a> &nbsp;|&nbsp;
  <a href="README.md#english"><b>🇬🇧 English (Bilingual README)</b></a>
</p>

<p align="center">
  <b>Universal, Modular Agentic Skills Catalog for AI Coding Agents</b><br>
  <i>Empowering Google Antigravity, OpenAI Codex, Claude Code, Cursor, Windsurf, Cline & GitHub Copilot CLI</i>
</p>

<p align="center">
  <a href="https://github.com/huytran1120/vietnam-agentic-skills"><img src="https://img.shields.io/badge/Agents-Antigravity%20%7C%20Codex%20%7C%20Claude%20%7C%20Cursor%20%7C%20Windsurf%20%7C%20Cline%20%7C%20Copilot-blueviolet?style=for-the-badge" alt="Universal Agents" /></a>
  <a href="https://github.com/huytran1120/vietnam-agentic-skills"><img src="https://img.shields.io/badge/Google%20Antigravity-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Antigravity" /></a>
  <a href="https://github.com/huytran1120/vietnam-agentic-skills"><img src="https://img.shields.io/badge/OpenAI%20Codex-412991?style=for-the-badge&logo=openai&logoColor=white" alt="Codex" /></a>
  <a href="https://github.com/huytran1120/vietnam-agentic-skills"><img src="https://img.shields.io/badge/Claude%20Code-D97706?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude Code" /></a>
  <a href="https://github.com/huytran1120/vietnam-agentic-skills"><img src="https://img.shields.io/badge/Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white" alt="Cursor" /></a>
  <a href="https://github.com/huytran1120/vietnam-agentic-skills"><img src="https://img.shields.io/badge/Windsurf-09B6A2?style=for-the-badge&logo=codeium&logoColor=white" alt="Windsurf" /></a>
</p>
<p align="center">
  <a href="https://github.com/huytran1120/vietnam-agentic-skills/actions/workflows/test.yml"><img src="https://img.shields.io/badge/CI-Passing-brightgreen?style=for-the-badge&logo=githubactions&logoColor=white" alt="CI Status" /></a>
  <a href="https://huytran1120.github.io/vietnam-agentic-skills/"><img src="https://img.shields.io/badge/Live%20Catalog-GitHub%20Pages-00C853?style=for-the-badge&logo=githubpages&logoColor=white" alt="Live Catalog" /></a>
  <a href="CATALOG.md"><img src="https://img.shields.io/badge/Catalog-3%2C070%2B%20Skills-00C853?style=for-the-badge" alt="Skills Count" /></a>
  <a href="vas.py"><img src="https://img.shields.io/badge/Zero--NPX-Pure%20Python%203-FF6D00?style=for-the-badge" alt="Zero NPX" /></a>
  <a href="https://github.com/huytran1120"><img src="https://img.shields.io/badge/Author-huytran1120-6200EA?style=for-the-badge&logo=github" alt="Author" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License: MIT" /></a>
</p>

> 🌐 **Live Web Explorer**: [https://huytran1120.github.io/vietnam-agentic-skills/](https://huytran1120.github.io/vietnam-agentic-skills/)

The catalog-first website supports keyword/author/source search, category filters, agent selection, and inline install commands. Counts come from the actual catalog; no download or rating figures are fabricated. The website copies commands, not installs software on your machine. Preview locally with `python3 -m http.server 8765 --directory docs`. Run the UI logic regressions with `node --test tests/pages.test.cjs`.

---

### 📌 Table of Contents
- [1. Overview](#1-overview)
- [2. Multi-Agent Compatibility](#2-multi-agent-compatibility)
- [3. Why Vietnam Agentic Skills?](#3-why-vietnam-agentic-skills)
- [4. Quickstart](#4-quickstart)
- [5. Agent-Specific Setup Guides](#5-agent-specific-setup-guides)
- [6. CLI Reference (`./vas`)](#6-cli-reference-vas)
- [7. Open Skill Specification (`SKILL.md`)](#7-open-skill-specification-skillmd)
- [8. Senior Engineering SDLC & 25 Addy Osmani Skills](#8-senior-engineering-sdlc--25-addy-osmani-skills)
- [9. 7 Technical Checklists & Reviewer Personas](#9-7-technical-checklists--reviewer-personas)
- [10. Honest Comparison Matrix (How VAS Compares)](#10-honest-comparison-matrix-how-vas-compares)
- [11. Featured & Viral Skills Showcase (Top 20)](#11-featured--viral-skills-showcase-top-20)
- [12. Frequently Asked Questions (FAQ)](#12-frequently-asked-questions-faq)
- [13. Author & License](#13-author--license)

---

### 1. Overview

**Vietnam Agentic Skills (VAS)** is a vendor-neutral, production-ready catalog of **3,070+ modular agentic skills**, created and maintained by **Huy Tran** ([@huytran1120](https://github.com/huytran1120)).

VAS strictly adheres to the **Open Agent Skills specification ([agentskills.io](https://agentskills.io/))** and is engineered specifically for modern AI coding agents such as **Google Antigravity, OpenAI Codex / OpenCode, Claude Code, Cursor, Windsurf (Codeium), Cline / Roo Code, and GitHub Copilot CLI**.

Instead of treating your AI coding assistant as an entry-level intern that generates shallow answers, VAS equips agents with Senior-grade playbooks: deep diagnostic checklists, security hardening rules, performance formulas, and deterministic execution scripts.

---

### 2. Multi-Agent Compatibility

VAS installs skills into native target directories across all leading AI coding assistants with a single command:

| AI Agent / IDE | Target Directory | Install Command |
| :--- | :--- | :--- |
| **Google Antigravity** | `.agents/skills/` or `~/.gemini/antigravity/skills/` | `./vas install <skill> --target antigravity` |
| **OpenAI Codex / OpenCode** | `.codex/skills/` or `.agents/skills/` | `./vas install <skill> --target codex` |
| **Claude Code** | `.claude/skills/` or `~/.claude/skills/` | `./vas install <skill> --target claude` |
| **Cursor IDE** | `.cursor/skills/` | `./vas install <skill> --target cursor` |
| **Windsurf (Codeium)** | `.windsurf/skills/` | `./vas install <skill> --target windsurf` |
| **Cline / Roo Code** | `.cline/skills/` | `./vas install <skill> --target cline` |
| **GitHub Copilot CLI** | `.github/skills/` | `./vas install <skill> --target copilot` |
| **ALL AGENTS AT ONCE** | Installs into all target folders above | `./vas install <skill> --target all` |

---

### 3. Why Vietnam Agentic Skills?

| Feature | Legacy NPX Solutions | Vietnam Agentic Skills (VAS) |
| :--- | :--- | :--- |
| **Runtime Requirements** | Requires Node.js & remote `npx` execution | **Native Python 3 CLI (`./vas`)** with standard library only |
| **Network Reliance** | Requires internet connectivity on every run | **100% Offline & Zero Dependencies** |
| **CLI Latency** | 3s - 15s per invocation | **< 0.05 seconds** (instantaneous) |
| **Agent Ecosystem** | Limited or manual copy-pasting | **Native support for 7+ AI Coding Agents** |
| **Installation Engine** | Manual file copying | **Symlink (`--mode link`) & Atomic Copy** with automatic rollbacks |
| **Context Window Preservation** | Prone to context bloat | **Strict Progressive Disclosure** (saving up to 99% of prompt tokens) |

---

### 4. Quickstart

```bash
# Step 1: Clone the repository
git clone https://github.com/huytran1120/vietnam-agentic-skills.git
cd vietnam-agentic-skills
chmod +x vas vas.py

# Step 2: Search for skills
./vas search docker-expert
./vas list --category security --limit 10
./vas categories

# Step 3: Install for your AI coding assistant
./vas install ui-ux-pro-max --target codex
./vas install docker-expert --target antigravity
./vas install fastapi-pro --target claude
./vas install react-component-performance --target cursor

# Install for ALL agents in your repository at once:
./vas install ui-ux-pro-max 007 pdf --target all
```
*(Smart alias system included: invoking `docker-security`, `fastapi-best-practices`, `react-performance`, or `nextjs-perf` will automatically map to the canonical skill).*

---

### 5. Agent-Specific Setup Guides

- **Google Antigravity**: Discovered automatically through `.agents/skills/` or globally at `~/.gemini/antigravity/skills/`:
  ```bash
  ./vas install <skill_id> --target antigravity --mode link
  ./vas install <skill_id> --target global
  ```
- **OpenAI Codex / OpenCode**: Excels at direct code reasoning and command execution:
  ```bash
  ./vas install <skill_id> --target codex --mode link
  ```
  *Sample prompt for Codex:*
  > *"Inspect the runbook at `.codex/skills/<skill_id>/SKILL.md` and execute the security audit workflow for this workspace."*
- **Claude Code**: Reads skills from `.claude/skills/` or user home `~/.claude/skills/`:
  ```bash
  ./vas install <skill_id> --target claude --mode link
  ```
- **Cursor IDE**: Links to `.cursor/skills/` and integrates with `.cursorrules` or `@.cursor/skills/<skill_id>` in Composer:
  ```bash
  ./vas install <skill_id> --target cursor --mode link
  ```
- **Windsurf (Codeium)**: Loads workflows seamlessly from `.windsurf/skills/`:
  ```bash
  ./vas install <skill_id> --target windsurf --mode link
  ```
- **Cline / Roo Code**:
  ```bash
  ./vas install <skill_id> --target cline --mode link
  ```
- **GitHub Copilot CLI**: Integrates test & CI/CD skills under `.github/skills/`:
  ```bash
  ./vas install <skill_id> --target copilot --mode link
  ```

---

### 6. CLI Reference (`./vas`)

```bash
# 1. Search skills by keyword
./vas search kubernetes
./vas search "react performance" --limit 15

# 2. List skills with optional filters
./vas list --category security
./vas list --tag python --limit 20

# 3. Inspect metadata and preview Runbook
./vas show ui-ux-pro-max
./vas show docker-expert

# 4. Install skills
./vas install ui-ux-pro-max 007 --target codex
./vas install --category devops --target claude
./vas install --category security --target all

# 5. Uninstall skills
./vas uninstall 007 --target codex
./vas uninstall docker-expert --target all

# 6. Check installed skills status
./vas status --target codex
./vas status --target antigravity

# 7. Initialize workspace & rebuild index
./vas init
./vas sync
./vas guide
```

---

### 7. Open Skill Specification (`SKILL.md`)

Every skill within `skills/<skill_name>/` follows the vendor-neutral Open Agent Skills format:

```text
skills/<skill_name>/
├── SKILL.md          # [Required] YAML Frontmatter + Step-by-step Runbook
├── scripts/          # [Optional] Automation scripts (Python, Bash, JS)
├── examples/         # [Optional] Sample configs, input/output fixtures
└── references/       # [Optional] In-depth technical guides & checklists
```

```markdown
---
name: docker-expert
category: devops
tags: [docker, security, hardening, containers]
risk: safe
description: >-
  Use this skill when auditing Dockerfile or container configurations
  against security vulnerabilities, root execution, and secret leaks.
---

# Docker Security Hardening Runbook

## Instructions
1. Run static analysis: `scripts/analyze.sh`
2. Verify base image tags and non-root USER directive.
3. Review exposed ports and multi-stage build patterns.
```

---

### 8. Senior Engineering SDLC & 25 Addy Osmani Skills

By default, AI coding agents follow the path of least resistance: jumping directly into code without a specification, bypassing test-driven development, skipping security or performance threat modeling, and self-rationalizing that *"it seems right"*.

Inspired by and directly synchronized with the official **v0.6.13 release of Addy Osmani's agent skills** ([addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) & [skills.addy.ie](https://skills.addy.ie/)), VAS integrates all **25 production-grade skills** mapped 1:1 across **6 phases of the software development lifecycle (SDLC)**:

```text
   DEFINE           PLAN            BUILD           VERIFY          REVIEW           SHIP
  ┌────────┐      ┌────────┐      ┌────────┐      ┌────────┐      ┌────────┐      ┌────────┐
  │  Idea  │ ───▶ │  Spec  │ ───▶ │  Code  │ ───▶ │  Test  │ ───▶ │   QA   │ ───▶ │   Go   │
  │ Refine │      │  PRD   │      │  Impl  │      │ Debug  │      │  Gate  │      │  Live  │
  └────────┘      └────────┘      └────────┘      └────────┘      └────────┘      └────────┘
   /spec           /plan           /build          /test          /review          /ship
```

#### 🛡️ The 4 Pillars of Senior Engineering Discipline
1. **Process, not prose**: Skills are actionable execution workflows with discrete steps, checkpoints, and strict exit criteria—not generic prompt advice.
2. **Anti-rationalization**: Every skill includes a *Common Rationalizations* table dismantling typical agent excuses (*"I'll write tests later"*, *"This is too trivial for security review"*), paired with actionable *Red Flags*.
3. **Verification is non-negotiable**: Agents must prove claims with reproducible evidence (passing test suites, runtime logs, DOM inspection, heap snapshots). "Seems right" is never accepted.
4. **Progressive disclosure**: `SKILL.md` serves as a lightweight entry point (< 150 prompt tokens initially). Supplementary in-depth guides load strictly on demand.

#### 📋 Complete Catalog of 25 Addy Osmani Skills by Phase

##### 🧭 Meta - Workflow Routing
| Skill | Core Capability | Trigger Condition |
| :--- | :--- | :--- |
| [`using-agent-skills`](skills/using-agent-skills/SKILL.md) | Maps incoming work to the appropriate skill workflow and defines shared operating boundaries | Starting a session or deciding which workflow applies |

##### 🎯 1. Define - Clarify What to Build
| Skill | Core Capability | Trigger Condition |
| :--- | :--- | :--- |
| [`interview-me`](skills/interview-me/SKILL.md) | Interrogates requirements one question at a time until reaching ~95% confidence on user intent | Requirements are ambiguous or user invokes "interview me" / "grill me" |
| [`idea-refine`](skills/idea-refine/SKILL.md) | Structured divergent/convergent thinking transforming raw ideas into concrete technical proposals | Exploring or scoping a rough early concept |
| [`spec-driven-development`](skills/spec-driven-development/SKILL.md) | Authors detailed PRDs covering objectives, CLI commands, architecture, code style, and testing gates before code | Starting a greenfield project, new feature, or major refactor |
| [`constraint-driven-development`](skills/constraint-driven-development/SKILL.md) | Establishes an enforceable quality bar in `CONSTRAINTS.md`, preventing agents from lowering thresholds | Team standards lack enforcement or an agent writes excessive unchecked code |

##### 🗺️ 2. Plan - Deconstruct & Sequence
| Skill | Core Capability | Trigger Condition |
| :--- | :--- | :--- |
| [`planning-and-task-breakdown`](skills/planning-and-task-breakdown/SKILL.md) | Decomposes specs into atomic, testable units with explicit acceptance criteria and topological ordering | A spec exists and needs implementation-ready task slices |

##### 🔨 3. Build - Implement with Rigor
| Skill | Core Capability | Trigger Condition |
| :--- | :--- | :--- |
| [`incremental-implementation`](skills/incremental-implementation/SKILL.md) | Delivers thin vertical slices: Implement → Test → Verify → Commit. Features safe defaults & rollback safety | Any code change touching more than one file |
| [`test-driven-development`](skills/test-driven-development/SKILL.md) | Red-Green-Refactor, 80/15/5 test pyramid, DAMP over DRY, Beyonce Rule, runtime browser verification | Writing new logic, fixing bugs, or changing system behavior |
| [`context-engineering`](skills/context-engineering/SKILL.md) | Feeds agents optimal context: rules configuration, context packing, MCP tool scoping | Starting a session, context switching, or when response quality degrades |
| [`source-driven-development`](skills/source-driven-development/SKILL.md) | Anchors framework decisions in official upstream documentation, citing sources and flagging deprecated APIs | High-correctness implementations requiring verified modern patterns |
| [`doubt-driven-development`](skills/doubt-driven-development/SKILL.md) | Fresh-context adversarial review of high-stakes decisions: CLAIM → EXTRACT → DOUBT → RECONCILE → STOP | High-risk changes (production, auth, finance), or unfamiliar codebases |
| [`frontend-ui-engineering`](skills/frontend-ui-engineering/SKILL.md) | Component architecture, state machines, responsive typography, and WCAG 2.1 AA accessibility | Designing or implementing client-facing web interfaces |
| [`api-and-interface-design`](skills/api-and-interface-design/SKILL.md) | Contract-first API design, Hyrum's Law, One-Version Rule, robust error semantics, input boundary validation | Authoring public APIs, microservice contracts, or module boundaries |

##### 🔍 4. Verify - Prove Correctness
| Skill | Core Capability | Trigger Condition |
| :--- | :--- | :--- |
| [`browser-testing-with-devtools`](skills/browser-testing-with-devtools/SKILL.md) | Leverages Chrome DevTools MCP for live runtime telemetry: DOM tree, console logs, network waterfalls, profiling | Building or troubleshooting browser-executed applications |
| [`debugging-and-error-recovery`](skills/debugging-and-error-recovery/SKILL.md) | 5-step triage: Reproduce → Localize → Reduce → Fix → Guard. Stop-the-line protocol and safe fallbacks | Failing test suites, broken builds, or unexpected runtime faults |

##### ⚖️ 5. Review - Pre-Merge Quality Gates
| Skill | Core Capability | Trigger Condition |
| :--- | :--- | :--- |
| [`code-review-and-quality`](skills/code-review-and-quality/SKILL.md) | Multi-axis review, ~100-line change sizing, explicit severity labels (Nit/Optional/FYI), review speed norms | Prior to merging any Pull Request |
| [`code-simplification`](skills/code-simplification/SKILL.md) | Chesterton's Fence, Rule of 500, dead code removal, minimizing cognitive complexity while preserving behavior | Functional code that suffers from excessive indirection or bloat |
| [`security-and-hardening`](skills/security-and-hardening/SKILL.md) | OWASP Top 10 mitigation, secrets hygiene, dependency supply-chain auditing, 3-tier trust boundary model | Handling untrusted input, user authentication, storage, or external APIs |
| [`performance-optimization`](skills/performance-optimization/SKILL.md) | Measurement-driven performance: Core Web Vitals (LCP, INP, CLS), CPU/RAM profiling, bundle budgeting | Strict performance SLAs exist or regression is suspected |

##### 🚀 6. Ship - Deploy with High Confidence
| Skill | Core Capability | Trigger Condition |
| :--- | :--- | :--- |
| [`git-workflow-and-versioning`](skills/git-workflow-and-versioning/SKILL.md) | Trunk-based development, atomic commits, and the commit-as-save-point pattern | Making any code modification in version control |
| [`ci-cd-and-automation`](skills/ci-cd-and-automation/SKILL.md) | Shift Left testing, Faster is Safer principle, quality gate pipelines, failure feedback loops | Establishing or optimizing automated build and deployment pipelines |
| [`deprecation-and-migration`](skills/deprecation-and-migration/SKILL.md) | Treating code as a liability, sunsetting zombie code, managing structured data & user migration paths | Sunsetting legacy services, deprecating endpoints, or refactoring schemas |
| [`documentation-and-adrs`](skills/documentation-and-adrs/SKILL.md) | Architecture Decision Records (ADRs), API references, documenting the *Why* behind engineering choices | Making architectural choices, public interface changes, or shipping milestones |
| [`observability-and-instrumentation`](skills/observability-and-instrumentation/SKILL.md) | Structured JSON logging, RED/USE metrics, OpenTelemetry distributed tracing, symptom-based alerting | Instrumenting telemetry or preparing services for production operations |
| [`shipping-and-launch`](skills/shipping-and-launch/SKILL.md) | Pre-flight checklists, staged canary rollouts, instant rollback procedures, active monitoring watch | Pre-release production deployments |

```bash
# Install the entire Addy Osmani Engineering Suite into your workspace:
./vas install test-driven-development debugging-and-error-recovery security-and-hardening performance-optimization code-review-and-quality --target all
```

---

### 9. 7 Technical Checklists & Reviewer Personas

#### 📚 Enterprise-Grade Reference Checklists (`references/`)
VAS skills dynamically load 7 comprehensive technical reference checklists housed in `references/`:

| Reference Guide | Subject Matter |
| :--- | :--- |
| [`references/definition-of-done.md`](references/definition-of-done.md) | Global Definition of Done (DoD) contract that every PR and task slice must satisfy |
| [`references/testing-patterns.md`](references/testing-patterns.md) | Production test layouts, naming semantics, mocking boundaries, React/API/E2E patterns, and anti-patterns |
| [`references/security-checklist.md`](references/security-checklist.md) | Pre-commit sanity checks, authz/authn, CSP headers, CORS policies, OWASP Top 10 mitigations |
| [`references/performance-checklist.md`](references/performance-checklist.md) | Core Web Vitals thresholds, frontend/backend optimization checklists, quantitative profiling commands |
| [`references/accessibility-checklist.md`](references/accessibility-checklist.md) | Keyboard navigation, screen reader compatibility, color contrast ratios, WCAG 2.1 AA ARIA rules |
| [`references/observability-checklist.md`](references/observability-checklist.md) | 2 AM on-call operational checks, structured logging standards, RED/USE metrics, distributed traces |
| [`references/orchestration-patterns.md`](references/orchestration-patterns.md) | Approved multi-agent orchestration designs, with the rule that personas cannot recursively invoke personas |

#### 👥 Specialist Reviewer Personas
During `/ship` pre-flight or code auditing, 4 specialist personas can be fanned out in parallel for multi-perspective validation:
* 👨‍💻 **Code Reviewer (Staff Engineer)**: 5-axis review upholding the standard *"Would a Staff Engineer approve this PR?"*.
* 🧪 **Test Engineer (QA Specialist)**: Evaluates test pyramid distribution, boundary conditions, and the Prove-It pattern.
* 🛡️ **Security Auditor (Security Specialist)**: Audits STRIDE threat boundaries, privilege escalation, and OWASP vulnerabilities.
* ⚡ **Web Performance Auditor (Performance Specialist)**: Enforces Core Web Vitals metrics honesty with Quick/Deep audit passes.

---

### 10. Honest Comparison Matrix (How VAS Compares)

| Dimension | Vietnam Agentic Skills (VAS) | Addy Osmani (`agent-skills`) | Superpowers (`obra`) | Matt Pocock Skills |
| :--- | :--- | :--- | :--- | :--- |
| **Catalog Scale** | **3,070+ Skills** (World's most extensive) | 25 Core Skills | ~14 Skills | ~30 Skills |
| **Tooling & Engine** | **Native Python 3 CLI (`./vas`) — Zero-NPX** | `npx skills` / Plugins | Git Worktrees / Shell scripts | Claude Code / `npx skills` |
| **Dependencies & Offline**| **100% Offline, Zero external dependencies** | Requires Node & remote NPX | Requires clone & git setup | Requires Node & remote NPX |
| **Agent Support** | **7+ AI Coding Assistants** (Antigravity, Codex, Claude, Cursor, Windsurf, Cline, Copilot) | Claude Code, Codex, Antigravity, Cursor, Copilot | Claude Code, Codex, Cursor | Claude Code primary |
| **SDLC Lifecycle Depth**| **Complete 6-Phase Lifecycle**: Define ➔ Plan ➔ Build ➔ Verify ➔ Review ➔ Ship | Complete 6-Phase Lifecycle | Focused on Build/Plan loop | Focused on Grilling & TDD |
| **Anti-Rationalization**| **Common Rationalizations & Red Flags in skills** | Built into all 25 skills | Task reviewer sign-off gate | None explicit |
| **Quality & Regression**| **95 Automated Tests (Python, Node, Cloudflare Security)** | 3-tier eval framework | TDD for documentation | No in-repo tests |
| **Context Optimization**| **Strict Progressive Disclosure** (< 150 prompt tokens initially) | Progressive Disclosure | Subagent Context Handoff | Split User/Model Invoked |

---

### 11. Featured & Viral Skills Showcase (Top 20)

VAS includes **3,070+ skills** across **118 specialized categories**. Browse the full directory in [CATALOG.md](CATALOG.md).

| # | Skill ID | Stars | Capability Overview | Quick Install Command |
| :-: | :--- | :---: | :--- | :--- |
| 1 | `ui-ux-pro-max` | ⭐ 139K | Generates a full Design System (79 styles, 192 palettes, 74 font pairings) from a project brief | `./vas install ui-ux-pro-max --target all` |
| 2 | `impeccable` | ⭐ 86K | Anti "AI-slop" design skill with 62 rule-based checks and 30+ bespoke design refinement modes | `./vas install impeccable --target all` |
| 3 | `hyperframes` | ⭐ 71K | HTML-rendered MP4 video for AI agents; includes `hyperframes-figma`, `motion-doctrine`, `seam-craft` | `./vas install hyperframes --target all` |
| 4 | `remotion` | ⭐ 67K | Official 12-skill suite for programming video in React (`remotion-create`, `remotion-render`, `remotion-captions`...) | `./vas install remotion-best-practices --target all` |
| 5 | `penpot` | ⭐ 62K | Open-source Figma alternative MCP server + 14 Penpot AI Kit skills (`penpot-build-screen`, `penpot-audit-tokens`...) | `./vas install penpot penpot-router --target all` |
| 6 | `diagram-design` | ⭐ 60K | Outputs 45 architectural & technical diagram types as standalone HTML+SVG matched to your brand tokens | `./vas install diagram-design --target all` |
| 7 | `blender-mcp` | ⭐ 32K | Connects Blender 3D to any LLM via MCP for prompt-driven modeling, materials, lighting, and rendering | `./vas install blender-mcp --target all` |
| 8 | `img2threejs` | ⭐ 19K | Procedurally reconstructs objects from reference images into code-only, animation-ready Three.js | `./vas install img2threejs --target all` |
| 9 | `video-shotcraft` | ⭐ 13K | Captures real web pages, selects from 150+ shot recipes, and renders promo videos using Remotion | `./vas install video-shotcraft --target all` |
| 10 | `lemo-opuscar` | ⭐ 6.5K | Directs and produces short films with 59 cinema styles crafted entirely in code, no video model required | `./vas install lemo-opuscar --target all` |
| 11 | `landing-page-design` | ⭐ Hot | Complete system for building high-converting landing pages (intake, layout, copy, visual system, fluid island nav, fluid motion) | `./vas install landing-page-design --target all` |
| 12 | `day-trader-skill` | ⭐ Hot | 11-skill Day Trading suite for US equities: chart scanning, SEC EDGAR news, entry/exit timing, Monte Carlo Time Machine, risk management & broker orders | `./vas install day-trader-skill --target all` |
| 13 | `ffmpeg-skill` | ⭐ Hot | 42-script local FFmpeg automation suite: lossless cutting, 9:16 reframe, karaoke subtitles, silence removal, ducking & compliance exports | `./vas install ffmpeg-skill --target all` |
| 14 | `design-to-motion` | ⭐ Hot | Converts static designs (Figma frames, dashboards, UI cards) into animated HTML, MP4 for X, and seamless 800×500 GIFs | `./vas install design-to-motion --target all` |
| 15 | `skills-manager` | ⭐ Hot | Orchestrates, syncs, backs up, and audits skills across Claude Code, Antigravity, Cursor, Windsurf, Codex | `./vas install skills-manager --target all` |
| 16 | `react-spring` | ⭐ 28K | Physics-based spring animation engine for natural, fluid UI motion in React, Three.js & Canvas | `./vas install react-spring --target all` |
| 17 | `pixijs` | ⭐ 43K | High-performance 2D WebGL/WebGPU graphics rendering engine for interactive canvases, particles & visual effects | `./vas install pixijs --target all` |
| 18 | `rapier` | ⭐ 6.8K | Fast 2D & 3D WebAssembly physics engine written in Rust for Three.js, React Three Fiber & game simulations | `./vas install rapier --target all` |
| 19 | `faster-whisper` | ⭐ 17K | Up to 4x faster speech-to-text transcription via CTranslate2 with word-level timestamps & SRT/VTT export | `./vas install faster-whisper --target all` |
| 20 | `obs-studio` | ⭐ 60K | Programmatic screen capture, scene automation, and high-bitrate recording pipelines via OBS WebSocket v5 | `./vas install obs-studio --target all` |

```text
📊 TOP CATEGORY DISTRIBUTION:
├── 🛡️  Security              : 267 skills (OWASP, Pentest, Secret Audit, IAM, Hardening)
├── 💻  Development           : 231 skills (Refactoring, Clean Code, Design Patterns, OOP)
├── 📈  Business & Strategy   : 179 skills (Market Research, Financial Models, Growth)
├── ☁️  Cloud                 : 170 skills (AWS, GCP, Azure, Serverless, Cloud Architecture)
├── ⚙️  DevOps                : 169 skills (Docker, K8s, Terraform, CI/CD, Ansible, SRE)
├── 🤖  AI & Machine Learning : 135 skills (RAG, LLM Evaluation, Prompt Engineering)
├── 🎨  Design, 3D & Video    : 120+ skills (Impeccable, UI/UX Pro Max, HyperFrames, Remotion, Penpot, Blender)
├── 🌐  Web & Fullstack       : 113 skills (React, Next.js, Vue, Node.js, FastAPI, Spring)
├── 🧪  Testing & QA          :  51 skills (Playwright, Jest, Pytest, E2E, Chaos Testing)
└── ... and 100+ more specialized domains.
```

#### 🌟 Top 10 High-End Demo Cards: Full Capabilities Showcase

<p align="center">
  <img src="docs/assets/demos/10-skills-demo-showcase.svg" alt="Top 10 High-End Demo Cards - Vietnam Agentic Skills" width="100%" />
</p>

* 🚀 **landing-page-design**: High-converting landing page architecture & Fluid Island Nav
* 🎨 **ui-ux-pro-max**: Generative Design System, 192 product palettes & 74 font pairings
* 🛡️ **impeccable**: Anti AI-slop design suite with 62 quantitative audit rules
* 🧊 **blender-mcp & img2threejs**: Natural language Blender 3D control & procedural Three.js
* 🎬 **video-shotcraft, hyperframes, remotion**: Programmatic video generation in React/HTML
* 📊 **diagram-design**: Enterprise cloud architecture diagrams in single HTML+SVG
* 🛠️ **chrome-devtools**: Automated browser debugging, LCP optimization, heap profiling & A11y
* ⚡ **bigquery-sql**: BigQuery query optimization, cost reduction & partition tuning
* 🔒 **firebase-firestore**: NoSQL data modeling & Firestore security rules red-team audit
* 🧬 **alphafold-fetch**: 3D biomolecular structure analysis & pLDDT confidence scoring

<details open>
<summary><b>1. High-Converting Landing Page Architecture (<code>landing-page-design</code>)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/landing-page-design.svg" alt="Landing Page Architecture Demo" width="850" />
</p>

* **Dual-Track Framework**: Strict separation between **Part A (Conversion Strategy & Copy)** and **Part B (Strict Visual Token System)**.
* **Core Doctrine**: *One offer → One audience → One primary action*.
* **Precision Engineering**: Fluid Island Navigation (floating pill nav), nested corner radius formula `r_in = r_out - padding`, fluid motion physics `cubic-bezier(0.32, 0.72, 0, 1)`, zero gratuitous background gradients.
* **Install**: `./vas install landing-page-design --target all`
</details>

<details open>
<summary><b>2. Full Design System & Palette Generation (<code>ui-ux-pro-max</code> — ⭐ 139K)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/ui-ux-pro-max.svg" alt="UI UX Pro Max Demo" width="850" />
</p>

* **Capabilities**: Generates complete, harmonious design systems from brief descriptions (79 styles, 192 product palettes, 74 typography pairings).
* **Standards**: WCAG 2.1 AAA/AA contrast compliance, 119 UX guidelines, with fast interactive CLI style search.
* **Install**: `./vas install ui-ux-pro-max --target all`
</details>

<details open>
<summary><b>3. Anti AI-Slop & Design Refinement Suite (<code>impeccable</code> — ⭐ 86K)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/impeccable.svg" alt="Impeccable Anti AI-Slop Demo" width="850" />
</p>

* **Capabilities**: Eliminates generic AI design tropes (gratuitous purple gradients, card soup, random spacing) using 62 rule-based checks.
* **Senior Modes**: Offers 30+ bespoke refinement modes (`/delight`, `/polish`, `/audit`, `/critique`) to elevate code to Out-of-Distribution Craft.
* **Install**: `./vas install impeccable --target all`
</details>

<details open>
<summary><b>4. Blender 3D Control & Procedural Three.js (<code>blender-mcp</code> & <code>img2threejs</code>)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/blender-and-3d.svg" alt="Blender and Three.js 3D Demo" width="850" />
</p>

* **Blender MCP**: Direct two-way bridge to Blender 3D via MCP server. Create meshes, assign PBR materials, rig, light, and render via natural language prompts.
* **img2threejs**: Reconstructs objects from 2D reference images into lightweight, code-only, animation-ready Three.js procedural models.
* **Install**: `./vas install blender-mcp img2threejs --target all`
</details>

<details open>
<summary><b>5. Programmatic Video & Motion Suite (<code>hyperframes</code>, <code>remotion</code>, <code>video-shotcraft</code>, <code>lemo-opuscar</code>)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/video-and-motion.svg" alt="Video and Motion Demo" width="850" />
</p>

* **HyperFrames**: Render HTML/CSS/SVG into deterministic MP4 videos for AI agents.
* **Remotion Suite**: Official 12-skill suite for programming video compositions in React.
* **Video Shotcraft & Lemo Opuscar**: 152 automated shot recipes and 59 cinema styles crafted completely in code, zero expensive video models needed.
* **Install**: `./vas install hyperframes video-shotcraft remotion --target all`
</details>

<details open>
<summary><b>6. Editorial & Cloud Architecture Diagramming (<code>diagram-design</code> — ⭐ 60K)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/diagram-design.svg" alt="Diagram Design Demo" width="850" />
</p>

* **Capabilities**: Generates 45+ complex architectural and system diagrams (AWS/GCP Cloud Architecture, K8s topology, Sequence Diagrams) into a single standalone HTML+SVG file.
* **Brand Alignment**: Automatically adopts corporate color palettes, font stacks, and layout hierarchy.
* **Install**: `./vas install diagram-design --target all`
</details>

<details open>
<summary><b>7. Automated Browser Debugging & A11y Audits (<code>chrome-devtools</code> — Google Official)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/chrome-devtools.svg" alt="Chrome DevTools MCP Automation Demo" width="850" />
</p>

* **Capabilities**: Direct autonomous browser interaction via Chrome DevTools MCP protocol. Live DOM tree inspection, memory leak diagnostics via heap snapshots, Core Web Vitals (LCP) performance profiling, and automated WCAG accessibility audits.
* **Automation**: Captures network HAR logs, pinpoints auth / CORS redirects, and autonomously fixes UI and rendering bugs.
* **Install**: `./vas install chrome-devtools --target all`
</details>

<details open>
<summary><b>8. Enterprise BigQuery SQL Cost & Performance Optimizer (<code>bigquery-sql</code> — Data Agent Kit)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/bigquery-sql.svg" alt="BigQuery SQL Performance Demo" width="850" />
</p>

* **Capabilities**: Analyzes SQL queries for anti-patterns, recommends date/timestamp partitioning and clustering keys, cuts scan volume (bytes billed) by up to 84%, and slashes query execution slot-ms.
* **Data Ecosystem**: Pairs seamlessly with dbt-bigquery, Dataform ELT, and Dataproc Serverless PySpark.
* **Install**: `./vas install bigquery-sql --target all`
</details>

<details open>
<summary><b>9. Firestore Security Rules Red-Team Auditor & NoSQL Modeling (<code>firebase-firestore</code> — Firebase Suite)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/firebase-firestore.svg" alt="Firebase Firestore Security Demo" width="850" />
</p>

* **Capabilities**: Automated security rule auditor identifying privilege escalation vulnerabilities, missing authorization checks, unvalidated writes, and resource exhaustion attacks.
* **Architecture**: Production-ready NoSQL document modeling, composite index creation, and SSR integration with Next.js/Angular via Firebase App Hosting.
* **Install**: `./vas install firebase-firestore --target all`
</details>

<details open>
<summary><b>10. 3D Biomolecular Structure Analysis & AlphaFold Scoring (<code>alphafold-fetch</code> — Science Plugin)</b></summary>
<br>

<p align="center">
  <img src="docs/assets/demos/alphafold-science.svg" alt="AlphaFold Science 3D Suite Demo" width="850" />
</p>

* **Capabilities**: Queries the AlphaFold Database by UniProt accession ID, retrieves predicted 3D structures (mmCIF), calculates pLDDT confidence scores, assesses domain boundaries, and flags disordered regions.
* **Interactive 3D Viewer**: Plugs directly into the Mol* Biomolecular Structure Viewer sidecar and biological research databases (ChEMBL, ClinVar, BLAST).
* **Install**: `./vas install alphafold-fetch --target all`
</details>

---

#### Matt Pocock skills

Added **16 missing stable skills** from [mattpocock/skills](https://github.com/mattpocock/skills)
at revision `5beb35b040e3de97e54fa9e386d7e42d15c295c2`, preserving **19 existing customized skills**.
All 31 current stable upstream skills are represented; 4 legacy entries remain available.
The 7 experimental `in-progress/` skills are intentionally excluded.

```bash
./vas search mattpocock/skills --limit 40
./vas install code-review to-spec to-tickets writing-for-agents --target antigravity
```

New imports retain Matt Pocock's MIT license and supporting files. Target-project prerequisites
(such as Claude Code, Bash/jq, or Node.js) are separate from the dependency-free VAS manager.
See the [pinned import manifest](data/mattpocock-skills.json) for provenance.

---

#### 🎨 94 Specialized Blender 3D Skills Suite (`arjun988/blender-skills`)

Integrated the comprehensive suite of **94 specialized 3D & Blender skills** from [arjun988/blender-skills](https://github.com/arjun988/blender-skills) by **Arjun Shukla** (MIT License), transforming AI coding assistants into an end-to-end **Senior Technical Art Team**:

* **Modeling & Sculpting**: `blender-modeler`, `hard-surface`, `sculpting`, `retopology`, `uv-workflow`, `procedural-modeling`, `geometry-nodes`, `cloth-sim`, `hair-groom`.
* **Shading & Lookdev**: `materials`, `texture-workflow`, `lighting`, `blender-lookdev`, `camera-cinematography`, `rendering`, `compositing`, `vfx-fx`.
* **Rigging & Animation**: `rigging`, `animation`, `physics-sim`.
* **Game Engine Pipelines**: `unity-export`, `unreal-export`, `godot-export`, `export-pipeline`, `asset-optimization`, `lod-pipeline`, `collision-proxy`, `qa-review`.
* **Art Disciplines**: `character-artist`, `creature-artist`, `environment-artist`, `prop-artist`, `vehicle-artist`, `vegetation-artist`, `archviz`.
* **40+ Artistic Styles & Game Genres**: `psx-horror-style`, `anime-style`, `manga-style`, `pixel-art-style`, `retro-16bit-style`, `lowpoly-style`, `stylized-style`, `realistic-style`, `isometric-style`, `frutiger-aero-style`, `liminal-space-style`, `genre-rpg`, `genre-soulslike`, `genre-shooter`, `genre-survival`...

```bash
# Search Blender skills:
./vas search "blender"
./vas search "Arjun Shukla" --limit 20

# Install core 3D technical art skills:
./vas install blender-director blender-modeler hard-surface materials rigging --target antigravity
```

Every skill includes modular references, polycount budget specifications (`references/polycount-budgets.md`), validation checklists, and Blender MCP integration. See [data/blender-skills.json](data/blender-skills.json) for details.

---

#### 🛡️ Cloudflare Security Audit (`cloudflare-security-audit`)

Integrated directly from Cloudflare's official open-source repository: [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill).

Enterprise-grade security guidance and adversarial vulnerability review pipeline designed to eliminate LLM context degradation and speculative false positives:
* **Deterministic Six-Phase Review Pipeline**: Reconnaissance, Coverage-Led Hunting, Candidate Validation, Structured Output, Independent Record Verification, Target-Neutral Reporting.
* **12 Targeted Attack Class Companions**: AI/LLM Prompt Injection & Tool Poisoning, Memory Safety & Binary, Cloud & Deployment SSRF, Web Protocols & Auth, ReDoS, Supply Chain, and Data Isolation.
* **Zero-Dependency Validators Included**: Bundled with deterministic Node.js verification harnesses (`validate-coverage-ledger.cjs` & `validate-findings.cjs`, passing all 65 test suites).

```bash
# Inspect the skill or use convenient aliases:
./vas show cloudflare-security-audit
./vas show security-audit-skill

# Install into your preferred AI agent:
./vas install cloudflare-security-audit --target antigravity --mode link
./vas install cloudflare-security-audit --target all
```

---

#### 🎬 The 20 Creative Coding, Motion & Programmatic Video Stack

VAS integrates the comprehensive modern stack of 20 creative coding, animation, 2D/3D physics, audio, and programmatic video rendering tools for AI agents:

| # | Tool | Skill / Alias | Core Focus & Domain | Quick Install Command |
| :-: | :--- | :--- | :--- | :--- |
| 01 | **Remotion** | `remotion` | React Video Engine for code-driven video | `./vas install remotion --target all` |
| 02 | **HyperFrames** | `hyperframes` | High-fidelity HTML-to-video rendering pipeline | `./vas install hyperframes --target all` |
| 03 | **Anime.js** | `animejs` / `anime.js` | Timeline choreography, SVG morphing & CSS animations | `./vas install animejs --target all` |
| 04 | **React Spring** | `react-spring` | Physics-based spring animation engine for React & 3D | `./vas install react-spring --target all` |
| 05 | **PixiJS** | `pixijs` / `pixi` | High-performance 2D WebGL/WebGPU graphics rendering | `./vas install pixijs --target all` |
| 06 | **p5.js** | `p5js` / `p5` | Generative art, algorithmic visuals & creative coding | `./vas install p5js --target all` |
| 07 | **Paper.js** | `paperjs` / `paper` | Vector graphics, Bézier math & boolean path operations | `./vas install paperjs --target all` |
| 08 | **Matter.js** | `matterjs` / `matter` | 2D rigid body dynamics & collision simulation | `./vas install matterjs --target all` |
| 09 | **Three.js** | `threejs` / `three` | 3D scenes, WebGL geometry, materials & lighting | `./vas install threejs --target all` |
| 10 | **Rapier** | `rapier` / `rapier3d` | Ultra-fast 2D & 3D physics in Rust & WebAssembly | `./vas install rapier --target all` |
| 11 | **OGL** | `ogl` / `ogl-webgl` | Minimal (~10KB) WebGL library for custom GLSL shaders | `./vas install ogl --target all` |
| 12 | **tsParticles** | `tsparticles` | Interactive particle nodes, canvas backgrounds & confetti | `./vas install tsparticles --target all` |
| 13 | **glTF Transform**| `gltf-transform` / `gltf` | 3D glTF/GLB optimization, DRACO, Meshopt & KTX2 | `./vas install gltf-transform --target all` |
| 14 | **GL Transitions**| `gl-transitions` | 50+ GLSL shader transitions for web canvas & video | `./vas install gl-transitions --target all` |
| 15 | **OBS Studio** | `obs-studio` / `obs` | Programmatic screen capture & OBS WebSocket v5 | `./vas install obs-studio --target all` |
| 16 | **Chatterbox** | `chatterbox` | Neural AI voiceover & voice cloning (Resemble AI) | `./vas install chatterbox --target all` |
| 17 | **Tone.js** | `tonejs` / `tone` | Web Audio framework for synths, SFX & audio scheduling | `./vas install tonejs --target all` |
| 18 | **faster-whisper**| `faster-whisper` / `whisper` | Fast speech-to-text transcription & SRT/VTT captions | `./vas install faster-whisper --target all` |
| 19 | **OpenCut** | `opencut` / `video-editor` | Timeline-based video composition & editing via code | `./vas install opencut --target all` |
| 20 | **FFmpeg** | `ffmpeg` / `ffmpeg-skill` | 42 local scripts for cutting, LUFS, subtitles & exports | `./vas install ffmpeg --target all` |

---

#### 📈 Automated US Equities Day Trading Suite (`day-trader-skill` - 11 Modules)

A modular 11-skill trading pipeline equipping AI agents to analyze, screen, and execute US equity trades:
* **The 11 Dedicated Modules**:
  - `trader-scanner`: Momentum, relative volume & volatility breakout screener.
  - `trader-news`: Real-time financial headlines & sentiment extraction.
  - `trader-entry` & `trader-exit`: Precise technical entry/exit triggers based on Risk-to-Reward.
  - `trader-risk` & `trader-budget`: Capital allocation, position sizing, and stop-loss enforcement.
  - `trader-broker`: Brokerage execution API connector (Alpaca, Interactive Brokers).
  - `trader-timemachine`: Strategy backtesting over historical tick and bar data.
  - `trader-alerts`: Multi-channel notification pipeline (Telegram, Discord, Webhooks).
  - `trader-analyst`: Fundamental balance sheet & valuation metrics analysis.
  - `trader-pelosi`: Real-time tracking of congressional stock trade disclosures.

```bash
# Install the complete suite:
./vas install day-trader-skill --target all

# Or install individual modules:
./vas install trader-scanner trader-risk trader-entry --target antigravity
```

---

#### 🎥 The 11 YouTube Channel Agent Suite (`Jakeschincariol/youtube-agent-skill`)

VAS integrates the complete **11-skill YouTube channel operations suite** from [Jakeschincariol/youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill) by **Jake Schincariol** (MIT License), providing deterministic Python heuristics and playbooks for professional video creators:

* **Scriptwriting & Quantitative Hook Scoring (`yt-script`)**: Turn ideas into complete spoken scripts with 5 hook variants evaluated across 21 formulas using `hookscore.py` (measuring Specificity, Address, Stakes, Curiosity, Brevity).
* **Title & Thumbnail Packaging Linter (`yt-package`)**: Lint titles and thumbnail text as a unified pairing via `title.py` to prevent redundant phrasing and maximize CTR.
* **Transcript Edit Decision Lists (`yt-edit`)**: Analyze timestamped SRT/VTT/Whisper transcripts to flag dead air, filler words, and repeated takes using `deadair.py`.
* **Audience Retention Diagnostics (`yt-retention`)**: Ingest YouTube Studio retention CSVs via `retention.py` to isolate 30s hook leak, steep cliffs, and middle slide.
* **Shorts Extraction & Repurposing (`yt-shorts`)**: Detect 20–55s standalone spans from long-form transcripts with fresh opening hooks and loop points.
* **Validated Chapter Generation (`yt-chapters`)**: Generate YouTube-compliant chapter blocks (starts at 00:00, ≥3 chapters, ≥10s duration) using `chapters.py`.
* **Outlier Virality Analysis (`yt-viral`)**: Benchmark niche videos by multiple over channel median view counts using `swipe.py`.
* **SEO, Comments & Channel Strategy (`yt-seo`, `yt-comment`, `yt-plan`, `yt-audit`)**: Optimize metadata for real queries, triage comment responses, plan weekly output, and execute channel audits that conclude in ONE actionable priority.

```bash
# Search YouTube skills:
./vas search youtube
./vas search "Jake Schincariol"

# Score a video hook with pure Python:
python3 skills/yt-script/hookscore.py --hook "I spent 100 hours testing AI tools so you don't waste your money"

# Install into Antigravity, Claude, or Codex:
./vas install yt-script yt-package yt-retention yt-edit yt-shorts yt-chapters yt-audit --target antigravity --mode link
```

---

#### ✨ The 16 Design Engineering & Motion Craft Suite (`emilkowalski/skills`)

VAS integrates the complete **16-skill Design Engineering, Motion & UI Polish suite** from [emilkowalski/skills](https://github.com/emilkowalski/skills) by **Emil Kowalski** (creator of Sonner and [animations.dev](https://animations.dev/) - MIT License), bringing taste, fluid physics, and rigorous motion audit standards to AI Coding Agents:

* **Motion From Scratch (`animate`, `animate-expo`)**: Build animations with the decision hierarchy that determines feel (purpose → tool → GPU `transform`/`opacity` properties → bezier curve & duration → interruption & exit). Full support for Web (CSS transitions, Framer Motion/WAAPI) and React Native/Expo (Reanimated, Gesture Handler, Haptics).
* **Frame Budgets & 60fps Performance (`animation-performance`)**: Keep animations within the 16.6ms budget: composite-only pipelines, avoiding layout/paint thrashing, profiling `will-change`, CSS variable re-evaluation, and blur filter costs.
* **High-Craft Motion Review (`review-animations`)**: Brutal motion auditing against non-negotiable rules (`STANDARDS.md`): defaults to flagging, verifies sub-300ms durations, spatial origin, easing curves, and `prefers-reduced-motion` conformance.
* **Codebase Audit Roadmaps (`improve-animations`, `find-animation-opportunities`)**: Survey entire repositories to generate prioritized finding tables and self-contained step-by-step execution plans (`plans/`) for downstream agents.
* **Motion Reduction & Cleanup (`remove-animations`)**: Identify and subtract gratuitous animations on hot surfaces, keyboard actions, and functional data to maximize app snappiness.
* **Motion Terminology Reverse-Lookup (`animation-vocabulary`)**: Translate intuitive visual descriptions into industry-standard animation nomenclature ("rubber-banding", "pop-in", "stagger", "spring overshoot").
* **Apple Design Philosophy (`apple-design`)**: Translates Apple's interface principles to the web: fluid gestures, physics springs, translucent depth materials, spatial consistency, optical tracking, and restraint.
* **Mobile Web Native Polish (`mobile-native`)**: Eliminate web quirks on mobile devices: sticky hover, tap highlight flash, 100vh viewport shifts, auto-zoom on inputs, notch insets, and long-press selection traps.
* **Sonner Toast Architecture (`ask-sonner`)**: Master-level integration and debugging for the Sonner toast engine (stacked toasts, promise toasts, custom styling, modal z-index stacking).
* **UI Edge-Case Stress Testing (`break-ui`)**: Inject worst-case boundary data (super long names, unbreakable emails, emoji floods, empty states, huge counters) from `CATALOG.md` behind a live toggle to expose layout breaks before shipping.
* **Variant Prototyping Harness (`emil-prototype`)**: Build multiple divergent UI explorations behind an instant live picker (`PICKER.md`) for real-world side-by-side evaluation.
* **Curated UI Library Selection (`pick-ui-library`)**: Highly opinionated selection guide for frontend components (OTP inputs, virtual scrolling, drag-drop, charts, command menus).
* **Modern Swift & Concurrency (`write-swift`)**: Comprehensive Swift 6 guidance covering data-race safety, `@concurrent`, actor boundaries, Swift Testing, and value type semantics.

```bash
# Search Emil Kowalski skills:
./vas search animation
./vas search "Emil Kowalski"

# Install core design engineering skills:
./vas install animate animation-performance review-animations emil-design-eng ask-sonner --target antigravity --mode link
```


---

#### 🗂️ Multi-Agent Skills Library Orchestrator (`skills-manager`)

Orchestrates, syncs, backs up, and audits skill configurations across modern AI coding assistants:
* **Cross-Agent Support**: Native coordination for Claude Code, Google Antigravity, Cursor, Windsurf, Codex, Cline, and Copilot CLI.
* **Core Capabilities**: Automatic discovery of installed skill directories, zero-copy symlink distribution, and configuration integrity audits.

```bash
./vas show skills-manager
./vas install skills-manager --target all
```

---

#### 🎨 Static Design to Fluid Motion & Video (`design-to-motion`)

A structured 3-phase methodology converting static designs (Figma frames, UI cards, dashboards) into living, interactive animated HTML, MP4 video for X, and seamless 800×500 showcase GIFs:
* **Part A (Pixel-Exact Recreation)**: 1:1 fidelity reconstruction of the design without arbitrary styling divergence.
* **Part B (Motion Choreography)**: Natural enter transitions from empty states into perpetual narrative loops.
* **Part C (Multi-Format Delivery)**: Automated video and GIF encoding for social sharing and web embedding.

```bash
./vas show design-to-motion
./vas install design-to-motion --target all
```

---

#### 🎞️ Automated Local Video & Audio Suite (`ffmpeg-skill`)

A comprehensive 42-script automation toolkit for pure Python local video and audio workflows:
* **Lossless Editing**: Keyframe-exact cuts, 9:16 vertical reframing for Reels/TikTok, scene detection, and visual contact sheets.
* **Audio & Subtitle Processing**: EBU R128 loudness normalization (-14 LUFS), automatic speech ducking, and word-accurate animated subtitles.

```bash
./vas show ffmpeg-skill
./vas install ffmpeg-skill --target all
```

### 12. Frequently Asked Questions (FAQ)

**Q: What value does the 25 Addy Osmani Senior Engineering skills suite bring to AI coding agents?**  
AI coding agents default to the path of least resistance: bypassing specs, jumping straight to code without test coverage, ignoring OWASP threat boundaries, and rationalizing that "it seems to work". The 25 production-grade skills enforce a disciplined 6-phase SDLC (Define → Plan → Build → Verify → Review → Ship) with anti-rationalization tables and strict evidence requirements before code can ship.

**Q: Do I need any special setup for OpenAI Codex / OpenCode?**  
*No.* Simply run `./vas install <skill_id> --target codex`. Codex parses markdown instructions natively and executes companion scripts directly in your shell environment.

**Q: Is Node.js or npm/npx required?**  
*Not at all.* VAS is built on the **Zero-NPX** philosophy. Searching, listing, and installing operate offline using standard Python 3 via `./vas`.

**Q: How do I install a skill across ALL my AI assistants?**  
Run `./vas install <skill_id> --target all`. This automatically provisions symlinks into `.agents/skills`, `.claude/skills`, `.cursor/skills`, `.windsurf/skills`, `.codex/skills`, `.cline/skills`, and `.github/skills`.

**Q: How does Progressive Disclosure save prompt tokens?**  
Even with hundreds of skills installed, AI agents initially only load the short YAML frontmatter summary. Full runbooks and scripts are injected into context only when your prompt matches the skill's trigger domain.

---

### 13. Author & License

* **Curator & Maintainer**: **Huy Tran** ([@huytran1120](https://github.com/huytran1120))
* **Email**: `66549585+huytran1120@users.noreply.github.com`
* **Official Repository**: [https://github.com/huytran1120/vietnam-agentic-skills](https://github.com/huytran1120/vietnam-agentic-skills)
* **Live Catalog**: [https://huytran1120.github.io/vietnam-agentic-skills/](https://huytran1120.github.io/vietnam-agentic-skills/)
* **License**: [MIT License](LICENSE) — Free for both personal and commercial use.

---

<p align="center">
  <b>Proudly developed & optimized for the global developer and AI agent community 🇻🇳 🌏</b><br>
  <i>Feedback and new skill proposals are welcome via <a href="https://github.com/huytran1120/vietnam-agentic-skills/issues">GitHub Issues</a>.</i>
</p>
