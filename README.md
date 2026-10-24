# Vietnam Agentic Skills (VAS)

> **Thư viện 2,650+ kỹ năng (agentic skills) chuyên sâu được tối ưu hoá riêng cho Google Antigravity — Hoàn toàn không cần `npx`, không phụ thuộc mạng hay môi trường Node.js.**

[![Google Antigravity](https://img.shields.io/badge/Target-Google%20Antigravity-4285F4?style=for-the-badge&logo=google)](https://github.com/huytran1120/vietnam-agentic-skills)
[![Skills Count](https://img.shields.io/badge/Skills-2%2C650%2B-00C853?style=for-the-badge)](CATALOG.md)
[![Zero NPX](https://img.shields.io/badge/Zero--NPX-Pure%20Python%203-FF6D00?style=for-the-badge)](vas.py)
[![Author: Huy Tran](https://img.shields.io/badge/Author-Huy%20Tran-6200EA?style=for-the-badge)](https://github.com/huytran1120)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

---

## 🇻🇳 Giới Thiệu (Overview)

**Vietnam Agentic Skills (VAS)** là dự án thư viện kỹ năng AI được kế thừa và phát triển từ bộ sưu tập các kỹ năng agentic hàng đầu thế giới, được **Huy Tran** tái cấu trúc và tối ưu hóa chuyên biệt cho **Google Antigravity**.

Khác với các dự án sử dụng `npx` (đòi hỏi runtime Node.js, kéo gói qua NPM registry mỗi lần chạy và phụ thuộc kết nối mạng), **Vietnam Agentic Skills** cung cấp:

1. **Bộ điều khiển nội bộ độc lập (`./vas`)**: Viết hoàn toàn bằng Python 3 chuẩn (Zero-Dependency), chạy trực tiếp trên máy với tốc độ phản hồi tính bằng mili-giây.
2. **Tối ưu hoá tuyệt đối cho Google Antigravity**:
   - Cài đặt chuẩn vào thư mục dự án cục bộ (`.agents/skills/` hoặc `.gemini/skills/`).
   - Cài đặt toàn cục cho mọi dự án (`~/.gemini/antigravity/skills/`).
   - Hỗ trợ chế độ **Symlink (`--mode link`)** giúp tiết kiệm dung lượng ổ đĩa và tự động cập nhật khi repo được nâng cấp.
   - Tuân thủ nguyên lý **Progressive Disclosure** (tiết lộ lũy tiến) giúp Antigravity duy trì context window gọn gàng, chỉ nạp kỹ năng khi thực sự cần.
3. **Đầy đủ 2,650+ Kỹ năng chuẩn**: Bao trùm 115 danh mục từ Bảo mật, DevOps, AI/ML, Fullstack, Cloud đến Tối ưu hóa hiệu năng và Kiểm thử tự động.

---

## 🚀 Cài Đặt Nhanh (Quickstart)

### 1. Tải về máy
```bash
git clone https://github.com/huytran1120/vietnam-agentic-skills.git
cd vietnam-agentic-skills
chmod +x vas
```

### 2. Tìm kiếm kỹ năng
```bash
# Tìm kiếm theo từ khóa
./vas search docker-security

# Xem danh sách theo thể loại
./vas list --category ai-ml --limit 10

# Xem các thể loại có sẵn
./vas categories
```

### 3. Cài đặt kỹ năng vào Antigravity (Zero NPX!)

#### A. Cài đặt vào Dự án Hiện Tại (Workspace Target):
```bash
# Cài đặt dạng symlink (khuyến nghị, tiết kiệm ổ cứng)
./vas install docker-security --target workspace --mode link

# Cài đặt nhiều kỹ năng cùng lúc
./vas install 007 react-performance fastapi-best-practices --target workspace

# Cài đặt trọn bộ theo nhóm chuyên mục
./vas install --category devops --target workspace
```

#### B. Cài đặt Toàn Cục cho Antigravity (Global Target):
```bash
# Kỹ năng sẽ có mặt ở tất cả các dự án bạn mở với Antigravity (~/.gemini/antigravity/skills/)
./vas install 007 --target global
```

### 4. Kiểm tra trạng thái kỹ năng đã cài
```bash
./vas status
```

### 5. Gỡ bỏ kỹ năng
```bash
./vas uninstall docker-security
```

---

## 🛠 Bảng Lệnh CLI (`./vas`)

| Lệnh | Cú pháp | Ý nghĩa |
| :--- | :--- | :--- |
| `search` | `./vas search <keyword>` | Tìm kiếm kỹ năng theo tên, mô tả, từ khóa, rủi ro |
| `list` | `./vas list [-c <cat>] [-t <tag>]` | Liệt kê danh sách kỹ năng có bộ lọc |
| `show` / `info` | `./vas show <skill_id>` | Xem chi tiết metadata và xem trước nội dung `SKILL.md` |
| `categories` | `./vas categories` | Hiển thị toàn bộ 115 danh mục và số lượng kỹ năng |
| `tags` | `./vas tags [--limit 50]` | Hiển thị các tag phổ biến nhất |
| `install` | `./vas install <ids...> [--target workspace\|global] [--mode link\|copy]` | Cài đặt kỹ năng vào Antigravity |
| `uninstall` | `./vas uninstall <ids...> [--target workspace\|global]` | Gỡ cài đặt kỹ năng khỏi Antigravity |
| `status` | `./vas status [--target workspace\|global]` | Xem danh sách các kỹ năng đang được kích hoạt |
| `init` | `./vas init` | Khởi tạo thư mục `.agents/skills` cho bất kỳ project nào |
| `sync` | `./vas sync` | Quét lại thư mục `skills/` và tái tạo `skills_index.json` |
| `guide` | `./vas guide` | Hiển thị tóm tắt kiến trúc Antigravity ngay trong terminal |

---

## 🧠 Cơ Chế Hoạt Động Với Google Antigravity

Antigravity nhận diện các kỹ năng thông qua thứ tự ưu tiên khám phá:

```text
Thứ tự ưu tiên của Antigravity:
1. Thư mục dự án:  <project_root>/.agents/skills/<skill_name>/SKILL.md
2. Cấu hình khai báo: <project_root>/skills.json
3. Khám phá toàn cục: ~/.gemini/antigravity/skills/<skill_name>/SKILL.md
4. Kỹ năng mặc định:  Tích hợp sẵn trong hệ thống Antigravity
```

### Cấu trúc một Skill chuẩn:
```text
skills/<skill_name>/
├── SKILL.md          # Bắt buộc: Chứa YAML frontmatter + Hướng dẫn từng bước
├── scripts/          # Tùy chọn: Shell script hoặc script bổ trợ
├── examples/         # Tùy chọn: Mã nguồn mẫu
└── references/       # Tùy chọn: Tài liệu chuyên sâu hoặc checklist đầy đủ
```

### Tối ưu hoá bộ nhớ (Progressive Disclosure):
Antigravity **không bao giờ nạp toàn bộ 2,650+ file vào bộ nhớ cùng lúc**. 
Khi bạn cài kỹ năng, Antigravity chỉ đọc phần metadata ngắn gọn ở đầu file:
```yaml
---
name: docker-security
description: Harden Dockerfiles and container configurations against privilege escalation and vulnerabilities.
---
```
Chỉ khi yêu cầu của bạn nhắc tới việc *"kiểm tra bảo mật file Dockerfile"*, Antigravity mới nạp toàn bộ tài liệu hướng dẫn vào bộ nhớ.

---

## 📊 Phân Bổ Danh Mục Kỹ Năng

Hơn 2,650 kỹ năng được phân chia trên 115 lĩnh vực chuyên biệt:

- **Security (267 skills)**: Kiểm toán mã nguồn, OWASP, Pentest, Docker/K8s Hardening, IAM, mã hóa dữ liệu.
- **Development (229 skills)**: Thiết kế phần mềm, Clean Code, Refactoring, Design Patterns.
- **Business & Strategy (179 skills)**: Nghiên cứu thị trường, Product Management, Tài chính, Phân tích dự án.
- **DevOps (167 skills)**: CI/CD Pipelines, Docker, Kubernetes, Ansible, Monitoring, SRE.
- **Cloud (147 skills)**: AWS, Google Cloud Platform (GCP), Azure, Serverless, Cloud Security.
- **AI & Machine Learning (134 skills)**: LLM Tuning, RAG, Prompt Engineering, Evaluation, Agentic Frameworks.
- **Web & Fullstack (113+ skills)**: React, Vue, Next.js, Node.js, FastAPI, Spring Boot, GraphQL.
- **Testing & QA (50 skills)**: E2E, Unit testing, Pytest, Playwright, Performance Testing.
- ... và 100+ danh mục chuyên biệt khác trong [CATALOG.md](CATALOG.md).

---

## 👥 Tác Giả & Bản Quyền

- **Tác giả / Duy trì**: **Huy Tran** ([@huytran1120](https://github.com/huytran1120))
- **Dự án**: Vietnam Agentic Skills (VAS)
- **Giấy phép**: [MIT License](LICENSE)
- **Nguồn cảm hứng**: Dựa trên kho dữ liệu mở từ cộng đồng mã nguồn mở agentic thế giới.

---

## 📖 Tài Liệu Tham Khảo Thêm

- [Chi tiết Hướng dẫn Antigravity](docs/ANTIGRAVITY_GUIDE.md)
- [Toàn bộ Danh mục Kỹ năng (CATALOG.md)](CATALOG.md)
- [Quy chuẩn cho AI Agents (AGENTS.md)](AGENTS.md)
