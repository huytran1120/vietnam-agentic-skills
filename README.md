# 🇻🇳 Vietnam Agentic Skills (VAS)

> **Kho lưu trữ 2,904+ kỹ năng (Agentic Skills) chuẩn quốc tế cho mọi AI Coding Agent.**  
> **Tương thích toàn diện: Google Antigravity, Claude Code, Cursor, Windsurf (Codeium), OpenAI Codex / OpenCode, Cline / Roo Code & GitHub Copilot CLI.**  
> **100% Zero-NPX. Không phụ thuộc Node.js hay NPM Registry. Tốc độ phản hồi sub-second với Python 3 chuẩn.**

[![Target: Universal Agents](https://img.shields.io/badge/Agents-Antigravity%20%7C%20Claude%20%7C%20Cursor%20%7C%20Windsurf%20%7C%20Codex%20%7C%20Cline%20%7C%20Copilot-blueviolet?style=for-the-badge)](https://github.com/huytran1120/vietnam-agentic-skills)
[![Google Antigravity](https://img.shields.io/badge/Antigravity-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://github.com/huytran1120/vietnam-agentic-skills)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-D97706?style=for-the-badge&logo=anthropic&logoColor=white)](https://github.com/huytran1120/vietnam-agentic-skills)
[![Cursor](https://img.shields.io/badge/Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white)](https://github.com/huytran1120/vietnam-agentic-skills)
[![Windsurf](https://img.shields.io/badge/Windsurf-09B6A2?style=for-the-badge&logo=codeium&logoColor=white)](https://github.com/huytran1120/vietnam-agentic-skills)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI%20Codex-412991?style=for-the-badge&logo=openai&logoColor=white)](https://github.com/huytran1120/vietnam-agentic-skills)
[![Live Catalog](https://img.shields.io/badge/Live%20Catalog-GitHub%20Pages-00C853?style=for-the-badge&logo=githubpages&logoColor=white)](https://huytran1120.github.io/vietnam-agentic-skills/)
[![Skills Count](https://img.shields.io/badge/Catalog-2%2C713%2B%20Skills-00C853?style=for-the-badge)](CATALOG.md)
[![Zero NPX](https://img.shields.io/badge/Zero--NPX-Pure%20Python%203-FF6D00?style=for-the-badge)](vas.py)
[![Author: huytran1120](https://img.shields.io/badge/Author-huytran1120-6200EA?style=for-the-badge&logo=github)](https://github.com/huytran1120)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

> 🌐 **Trải nghiệm tìm kiếm và tra cứu trực tiếp trên web**: [https://huytran1120.github.io/vietnam-agentic-skills/](https://huytran1120.github.io/vietnam-agentic-skills/)

---

## 📌 Mục Lục (Table of Contents)

- [1. Giới Thiệu (Overview)](#1-giới-thiệu-overview)
- [2. Hỗ Trợ Đa Nền Tảng (Multi-Agent Compatibility)](#2-hỗ-trợ-đa-nền-tảng-multi-agent-compatibility)
- [3. Vì Sao Chọn Vietnam Agentic Skills?](#3-vì-sao-chọn-vietnam-agentic-skills)
- [4. Cài Đặt & Sử Dụng Nhanh (Quickstart)](#4-cài-đặt--sử-dụng-nhanh-quickstart)
- [5. Hướng Dẫn Chi Tiết Cho Từng AI Agent](#5-hướng-dẫn-chi-tiết-cho-từng-ai-agent)
  - [Google Antigravity](#-google-antigravity)
  - [OpenAI Codex / OpenCode](#-openai-codex--opencode)
  - [Claude Code](#-claude-code)
  - [Cursor IDE](#-cursor-ide)
  - [Windsurf (Codeium)](#-windsurf-codeium)
  - [Cline / Roo Code](#-cline--roo-code)
  - [GitHub Copilot CLI](#-github-copilot-cli)
- [6. Cẩm Nang Lệnh CLI (`./vas`)](#6-cẩm-nang-lệnh-cli-vas)
- [7. Cấu Trúc Chuẩn Của Một Skill](#7-cấu-trúc-chuẩn-của-một-skill)
- [8. Danh Mục Kỹ Năng Nổi Bật](#8-danh-mục-kỹ-năng-nổi-bật)
- [9. Câu Hỏi Thường Gặp (FAQ)](#9-câu-hỏi-thường-gặp-faq)
- [10. Tác Giả & Giấy Phép](#10-tác-giả--giấy-phép)

---

## 1. Giới Thiệu (Overview)

**Vietnam Agentic Skills (VAS)** là dự án thư viện kỹ năng agentic mã nguồn mở được khởi xướng và phát triển bởi **Huy Tran** ([@huytran1120](https://github.com/huytran1120)). 

Dự án đóng gói **hơn 2,904 playbooks (`SKILL.md`)** chuyên sâu thuộc 115 danh mục công nghệ, tuân thủ nghiêm ngặt **Chuẩn mở Agent Skills Quốc tế ([agentskills.io](https://agentskills.io/))**.

Với VAS, các AI Coding Agent không còn là những lập trình viên trả lời chung chung, mà trở thành những cộng sự kỹ thuật cấp Senior thực thụ, có quy trình chuẩn đoán, checklist bảo mật, công thức tối ưu và kịch bản thực thi chính xác.

---

## 2. Hỗ Trợ Đa Nền Tảng (Multi-Agent Compatibility)

VAS hỗ trợ cài đặt bằng một câu lệnh duy nhất cho tất cả các AI coding tools thịnh hành nhất hiện nay:

| AI Agent / IDE | Thư Mục Mục Tiêu | Lệnh Cài Đặt Với `./vas` |
| :--- | :--- | :--- |
| **Google Antigravity** | `.agents/skills/` hoặc `~/.gemini/antigravity/skills/` | `./vas install <skill> --target antigravity` |
| **OpenAI Codex / OpenCode** | `.codex/skills/` hoặc `.agents/skills/` | `./vas install <skill> --target codex` |
| **Claude Code** | `.claude/skills/` hoặc `~/.claude/skills/` | `./vas install <skill> --target claude` |
| **Cursor IDE** | `.cursor/skills/` | `./vas install <skill> --target cursor` |
| **Windsurf (Codeium)** | `.windsurf/skills/` | `./vas install <skill> --target windsurf` |
| **Cline / Roo Code** | `.cline/skills/` | `./vas install <skill> --target cline` |
| **GitHub Copilot CLI** | `.github/skills/` | `./vas install <skill> --target copilot` |
| **TẤT CẢ CÁC AGENT** | Cài đồng bộ vào mọi thư mục trên | `./vas install <skill> --target all` |

---

## 3. Vì Sao Chọn Vietnam Agentic Skills?

So sánh giữa giải pháp gốc dùng `npx` (`agentic-awesome-skills`) và **Vietnam Agentic Skills (VAS)**:

| Tiêu Chí | Giải Pháp Cũ (`npx`) | Vietnam Agentic Skills (VAS) |
| :--- | :--- | :--- |
| **Công cụ quản lý** | Bắt buộc Node.js & gọi `npx` từ remote | **Native Python 3 CLI (`./vas`)** dùng thư viện chuẩn |
| **Kết nối mạng** | Cần Internet mỗi lần chạy npx | **100% Offline & Zero Dependencies** |
| **Tốc độ phản hồi** | 3s - 15s mỗi lần chạy | **< 0.05 giây** (tức thì) |
| **Khả năng tương thích** | Giới hạn hoặc nạp thủ công | **Hỗ trợ 7+ AI Agent lớn** (Antigravity, Codex, Claude, Cursor, Windsurf, Cline, Copilot) |
| **Cơ chế cài đặt** | Copy thủ công | Hỗ trợ cả **Symlink** (`--mode link`) và **Deep Copy** |
| **Bảo toàn ngữ cảnh** | Dễ gây phình token ngữ cảnh | Tuân thủ tuyệt đối **Progressive Disclosure** (tiết kiệm 99% token) |

---

## 4. Cài Đặt & Sử Dụng Nhanh (Quickstart)

### Bước 1: Clone kho lưu trữ về máy
```bash
git clone https://github.com/huytran1120/vietnam-agentic-skills.git
cd vietnam-agentic-skills
chmod +x vas vas.py
```

### Bước 2: Tìm kiếm kỹ năng bạn cần
```bash
# Tìm kiếm kỹ năng theo từ khóa
./vas search docker-expert

# Liệt kê theo danh mục
./vas list --category security --limit 10

# Khám phá các danh mục có sẵn
./vas categories
```

### Bước 3: Cài đặt cho Agent bạn đang sử dụng

```bash
# Cài cho OpenAI Codex:
./vas install ui-ux-pro-max --target codex

# Cài cho Google Antigravity:
./vas install docker-expert --target antigravity

# Cài cho Claude Code:
./vas install fastapi-pro --target claude

# Cài cho Cursor:
./vas install react-component-performance --target cursor

# Cài cho tất cả AI Agent trong dự án cùng một lúc:
./vas install ui-ux-pro-max 007 pdf --target all
```
*(Hệ thống hỗ trợ bí danh tự động: các lệnh gọi alias như `docker-security`, `fastapi-best-practices`, `react-performance`, `nextjs-perf` sẽ tự động trỏ tới skill thực).*

---

## 5. Hướng Dẫn Chi Tiết Cho Từng AI Agent

### 🤖 Google Antigravity
Google Antigravity quét kỹ năng tự động qua thư mục `.agents/skills/` trong workspace hoặc thư mục toàn cục `~/.gemini/antigravity/skills/`:
```bash
# Cài đặt cho dự án hiện tại:
./vas install <skill_id> --target antigravity --mode link

# Cài đặt toàn cục (dùng cho mọi dự án):
./vas install <skill_id> --target global
```

### 🧠 OpenAI Codex / OpenCode
OpenAI Codex có thế mạnh vượt trội về suy luận code và thực thi lệnh terminal. Codex nhận diện kỹ năng qua thư mục `.codex/skills/`, `.agents/skills/`, hoặc file chỉ dẫn `AGENTS.md` ở root:
```bash
# Cài đặt vào workspace của Codex:
./vas install <skill_id> --target codex --mode link

# Hoặc cài toàn cục cho Codex trên máy:
./vas install <skill_id> --target codex --global
```
*Prompt mẫu trong Codex:*
> *"Hãy đọc runbook trong skill `.codex/skills/<skill_id>/SKILL.md` và thực thi kịch bản kiểm tra bảo mật cho thư mục hiện tại."*

### 🟠 Claude Code
Claude Code đọc các kỹ năng từ thư mục `.claude/skills/` hoặc toàn cục `~/.claude/skills/`:
```bash
# Cài đặt vào workspace Claude Code:
./vas install <skill_id> --target claude --mode link

# Cài đặt toàn cục:
./vas install <skill_id> --target claude --global
```

### ⚡ Cursor IDE
Cursor có thể liên kết trực tiếp các skill vào `.cursor/skills/` và kết hợp với `.cursorrules`:
```bash
./vas install <skill_id> --target cursor --mode link
```
*Gợi ý:* Trong Cursor Composer, bạn chỉ cần gõ `@.cursor/skills/<skill_id>` để đính kèm playbook vào ngữ cảnh.

### 🌊 Windsurf (Codeium)
Windsurf hỗ trợ nạp quy trình làm việc từ thư mục `.windsurf/skills/`:
```bash
./vas install <skill_id> --target windsurf --mode link
```

### 💻 Cline / Roo Code
Dành cho lập trình viên sử dụng extension Cline hoặc Roo Code trên VS Code:
```bash
./vas install <skill_id> --target cline --mode link
```

### 🐙 GitHub Copilot CLI
Tích hợp các kịch bản kiểm thử và CI/CD vào thư mục `.github/skills/`:
```bash
./vas install <skill_id> --target copilot --mode link
```

---

## 6. Cẩm Nang Lệnh CLI (`./vas`)

```text
Cú pháp chung:
  ./vas <sub-command> [arguments] [options]
```

### 1. `search` — Tìm kiếm kỹ năng
```bash
./vas search kubernetes
./vas search "react performance" --limit 15
```

### 2. `list` — Liệt kê kỹ năng có bộ lọc
```bash
./vas list --category ai-ml
./vas list --tag python --limit 20
```

### 3. `show` / `info` — Xem chi tiết & Preview Runbook
Hiển thị metadata, tác giả, rủi ro và xem trước 40 dòng đầu của `SKILL.md`:
```bash
./vas show ui-ux-pro-max
./vas show docker-expert
```

### 4. `install` — Cài đặt cho AI Agent
```bash
# Cài đặt 1 hoặc nhiều skills
./vas install ui-ux-pro-max 007 --target codex

# Cài đặt toàn bộ danh mục devops
./vas install --category devops --target claude

# Cài đặt đồng bộ cho tất cả các AI Agents
./vas install --category security --target all
```

**Các tuỳ chọn của `install`:**
* `--target`: `antigravity`, `codex`, `claude`, `cursor`, `windsurf`, `cline`, `copilot`, `workspace`, `all`.
* `--mode`: `link` (symlink tiết kiệm dung lượng, tự động cập nhật) hoặc `copy` (sao chép độc lập).
* `--global`: Cài đặt vào thư mục home của người dùng thay vì workspace.
* `--dest`: Đường dẫn thư mục tùy biến bất kỳ.

### 5. `uninstall` / `remove` — Gỡ bỏ kỹ năng
```bash
./vas uninstall 007 --target codex
./vas uninstall docker-expert --target all
```

### 6. `status` — Kiểm tra kỹ năng đã cài
```bash
./vas status --target codex
./vas status --target antigravity
```

### 7. `guide` — Hướng dẫn đa nền tảng
```bash
./vas guide
```

---

## 7. Cấu Trúc Chuẩn Của Một Skill

Mỗi kỹ năng trong thư mục `skills/<skill_name>/` tuân thủ nghiêm ngặt chuẩn mở:

```text
skills/<skill_name>/
├── SKILL.md          # [Bắt buộc] YAML Frontmatter + Runbook từng bước
├── scripts/          # [Tuỳ chọn] Script tự động hóa (Python, Bash, JS)
├── examples/         # [Tuỳ chọn] File cấu hình mẫu, input/output tham khảo
└── references/       # [Tuỳ chọn] Checklist chi tiết hoặc tài liệu kỹ thuật
```

### Tiêu chuẩn `SKILL.md`:
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

# Docker Security Hardening

## Step-by-Step Instructions
1. Run static analysis: `scripts/analyze.sh`
2. Verify base image tags and non-root USER directive.
3. Review exposed ports and multi-stage build patterns.
```

---

## 8. Danh Mục Kỹ Năng Nổi Bật

Kho lưu trữ gồm **2,904+ skills** chia theo 115 nhóm ngành. Xem danh mục tại [CATALOG.md](CATALOG.md).

### 🔥 Top 10 Siêu Kỹ Năng Thiết Kế, 3D & Video Mới Nhất Đã Tích Hợp:

| # | Skill ID | Stars | Mô Tả Năng Lực | Lệnh Cài Đặt Nhanh |
| :-: | :--- | :---: | :--- | :--- |
| 1 | `ui-ux-pro-max` | ⭐ 139K | Tạo hệ thống Design System hoàn chỉnh (79 styles, 192 palettes, 74 font pairings) từ mô tả dự án | `./vas install ui-ux-pro-max --target all` |
| 2 | `impeccable` | ⭐ 86K | Chống giao diện "AI-slop" với 62 quy tắc kiểm tra tự động & 30+ chế độ tinh chỉnh thiết kế | `./vas install impeccable --target all` |
| 3 | `hyperframes` | ⭐ 71K | Viết HTML xuất video MP4 chuẩn cho AI Agent; đi kèm `hyperframes-figma`, `motion-doctrine`, `seam-craft` | `./vas install hyperframes --target all` |
| 4 | `remotion` | ⭐ 67K | Bộ 12 kỹ năng chính thức lập trình video bằng React (`remotion-create`, `remotion-render`, `remotion-captions`...) | `./vas install remotion-best-practices --target all` |
| 5 | `penpot` | ⭐ 62K | Kết nối Penpot (Figma mã nguồn mở) qua MCP Server kèm 14 kỹ năng AI Kit (`penpot-build-screen`, `penpot-audit-tokens`...) | `./vas install penpot penpot-router --target all` |
| 6 | `diagram-design` | ⭐ 60K | Xuất 45 loại sơ đồ kiến trúc thành 1 file HTML+SVG độc lập chuẩn màu sắc & font thương hiệu | `./vas install diagram-design --target all` |
| 7 | `blender-mcp` | ⭐ 32K | Kết nối Blender 3D với bất kỳ LLM nào để dựng hình, gán vật liệu, ánh sáng, rigging & animation bằng prompt | `./vas install blender-mcp --target all` |
| 8 | `img2threejs` | ⭐ 19K | Tái tạo đối tượng từ ảnh tham chiếu thành mô hình 3D Three.js thuần code, sẵn sàng diễn hoạt | `./vas install img2threejs --target all` |
| 9 | `video-shotcraft` | ⭐ 13K | Chụp trang thực tế, chọn từ 152 công thức góc máy (shot recipes) và kết xuất video quảng cáo bằng Remotion | `./vas install video-shotcraft --target all` |
| 10 | `lemo-opuscar` | ⭐ 6.5K | Đạo diễn & sản xuất phim ngắn bằng 59 phong cách điện ảnh viết hoàn toàn bằng code, không cần video model | `./vas install lemo-opuscar --target all` |

```text
📊 PHÂN BỔ CÁC DANH MỤC HÀNG ĐẦU:
├── 🛡️  Security              : 267 skills (OWASP, Pentest, Secret Audit, IAM, Hardening)
├── 💻  Development           : 229 skills (Refactoring, Clean Code, Design Patterns, OOP)
├── 📈  Business & Strategy   : 179 skills (Market Research, Financial Models, Growth)
├── ⚙️  DevOps                : 167 skills (Docker, K8s, Terraform, CI/CD, Ansible, SRE)
├── ☁️  Cloud                 : 147 skills (AWS, GCP, Azure, Serverless, Cloud Architecture)
├── 🤖  AI & Machine Learning : 134 skills (RAG, LLM Evaluation, Prompt Engineering)
├── 🎨  Design, 3D & Video    : 120+ skills (Impeccable, UI/UX Pro Max, HyperFrames, Remotion, Penpot, Blender)
├── 🌐  Web & Fullstack       : 113 skills (React, Next.js, Vue, Node.js, FastAPI, Spring)
├── 🧪  Testing & QA          :  50 skills (Playwright, Jest, Pytest, E2E, Chaos Testing)
└── ... và hơn 100+ danh mục chuyên biệt khác.
```

---

## 9. Câu Hỏi Thường Gặp (FAQ)

### Q: Tôi dùng OpenAI Codex thì có cần cấu hình gì thêm không?
**Không cần.** Bạn chỉ cần chạy `./vas install <skill_id> --target codex`. Codex có khả năng đọc Markdown và gọi các script thực thi trực tiếp trong môi trường của bạn.

### Q: Tôi có cần cài đặt Node.js hay npm/npx không?
**Hoàn toàn không.** Dự án được xây dựng theo tiêu chuẩn **Zero-NPX**. Tất cả lệnh tìm kiếm, liệt kê và cài đặt đều chạy bằng Python 3 tích hợp sẵn trên máy qua `./vas`.

### Q: Làm sao để cài đặt một kỹ năng cho TẤT CẢ các AI tools tôi đang dùng?
Chỉ cần chạy:
```bash
./vas install ui-ux-pro-max --target all
```
Lệnh này sẽ tự động tạo symlink vào `.agents/skills`, `.claude/skills`, `.cursor/skills`, `.windsurf/skills`, `.codex/skills`, `.cline/skills`, `.github/skills`.

### Q: Cơ chế Progressive Disclosure tiết kiệm token như thế nào?
Dù bạn cài hàng trăm kỹ năng, các AI agent chỉ quét phần tóm tắt ngắn (YAML frontmatter). Chỉ khi câu hỏi của bạn khớp với chuyên môn của skill, Agent mới nạp toàn bộ nội dung chi tiết vào ngữ cảnh.

---

## 10. Tác Giả & Giấy Phép (Author & License)

* **Tác giả & Duy trì**: **Huy Tran** ([@huytran1120](https://github.com/huytran1120))
* **Email**: `66549585+huytran1120@users.noreply.github.com`
* **Kho lưu trữ chính thức**: [https://github.com/huytran1120/vietnam-agentic-skills](https://github.com/huytran1120/vietnam-agentic-skills)
* **Website Catalog**: [https://huytran1120.github.io/vietnam-agentic-skills/](https://huytran1120.github.io/vietnam-agentic-skills/)
* **Giấy phép**: [MIT License](LICENSE) — Tự do sử dụng cá nhân và thương mại.

---

<p align="center">
  <b>Tự hào phát triển và tối ưu cho cộng đồng AI Agent & Lập trình viên Việt Nam 🇻🇳</b><br>
  <i>Đóng góp ý kiến hoặc yêu cầu kỹ năng mới qua <a href="https://github.com/huytran1120/vietnam-agentic-skills/issues">GitHub Issues</a>.</i>
</p>
