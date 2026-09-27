# ⚡ Universal DevCycle & Engineering Skills Suite

Bộ sưu tập kỹ năng toàn diện (**Full Skills Suite**) chuẩn **Senior Principal Software Engineer & Red-Team Security Architect** dành cho **Google Antigravity AI Assistant**.

Toàn bộ **46 skills** đều là các **thư mục thực độc lập (100% Real Directories - Zero Symlinks)**, chứa đầy đủ mã nguồn, tài liệu hướng dẫn (`SKILL.md`), scripts thực thi và các asset tương ứng được đồng bộ trực tiếp từ các repository chính thức trên GitHub.

Hỗ trợ **tất cả các ngôn ngữ lập trình** (*TypeScript, JavaScript, Python, Go, Rust, Java, PHP, C, C++, Swift, Dart, Ruby, R, C#, Kotlin*) và **toàn bộ các framework** tương ứng.

---

## 🚀 Cài Đặt Tự Động Đa Nền Tảng (Windows & Ubuntu / Linux)

### Cách chạy:
- **Trên Ubuntu / Linux / macOS / WSL:**
  ```bash
  cd dev_skills
  ./install.sh
  ```
- **Trên Windows (qua Git Bash, MSYS2 hoặc WSL):**
  ```bash
  cd dev_skills
  bash install.sh
  ```

### Các tùy chọn nâng cao:
```bash
./install.sh --help            # Xem trợ giúp
./install.sh --update          # Cập nhật bộ skills: kéo Git mới nhất & force update ghi đè toàn bộ kỹ năng (chỉ tác động skills)
./install.sh --upgrade         # Tương tự --update: đồng bộ và cập nhật lại toàn bộ bộ skills (không đụng môi trường runtime)
./install.sh --force           # Cài đặt lại và ghi đè toàn bộ kỹ năng
./install.sh --security-tools  # Cài đặt sẵn bộ công cụ an ninh (semgrep, bandit, pip-audit, detect-secrets, schemathesis, checkov)
./install.sh --link            # Dùng symbolic link thay vì copy
./install.sh --target <DIR>    # Chỉ định thư mục lưu skill tùy chỉnh
```

### Script `install.sh` tự động thực hiện:
1. **Kiểm tra môi trường & Đường dẫn Antigravity:** Tự động phát hiện OS (Ubuntu `~/.gemini/config/skills` hoặc Windows `%USERPROFILE%/.gemini/config/skills`), kiểm tra Python (`python3`/`python`/`py`), Node.js, npm, git.
2. **Cài đặt công cụ bắt buộc:**
   - ⚡ **Graft** (`@nanonets/graft` qua npm): AST call graph, API skeleton, blast radius.
   - 🧠 **Graphify** (`graphifyy` qua uv/pipx/pip): Semantic GraphRAG, kiến trúc đồ thị dự án.
   - 🧹 **Ruff** (hoặc linter tương ứng): Kiểm tra code quality siêu tốc.
3. **Kiểm tra thông minh & Triển khai siêu tốc:**
   - **Đã có trên Antigravity:** Tự động bỏ qua (skip) giúp việc chạy lại chỉ mất chưa đầy 1 giây.
   - **Chưa có trên Antigravity:**
     + Nếu đã có trong thư mục này: Thực hiện cài luôn tức thì.
     + Nếu chưa có trong thư mục: Tự động clone từ GitHub nguồn (`emilkowalski/skills`, `taste-skill`, `impeccable`) và triển khai.
4. **Cấp quyền thực thi:** Gán `chmod +x` cho toàn bộ các script (`secscan.py`, `lint.py`, `index_codebase.py`, v.v.).

---

## 🌐 Nguồn Gốc GitHub Của Các Bộ Skill (GitHub Sources)

Tất cả các skill đã được trích xuất thành các thư mục độc lập từ các repository uy tín hàng đầu:

| Nhóm Skill | Repository Nguồn Trên GitHub | Tác giả / Bản quyền |
|---|---|---|
| **DevCycle Suite** | DevCycle Master Lifecycle | Senior Principal Architect |
| **Animation & Interaction** | [emilkowalski/skills](https://github.com/emilkowalski/skills.git) | Emil Kowalski |
| **Aesthetic & Taste Design** | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill.git) | Leonxlnx |
| **Impeccable Design System** | [pbakaus/impeccable](https://github.com/pbakaus/impeccable.git) | Paul Bakaus |

---

## 📦 Danh Mục 46 Skills Độc Lập

### 1. DevCycle Lifecycle Suite (14 Skills)
- `devcycle`: Master Driver điều phối 8 phase tự động từ ý tưởng đến bàn giao.
- `devcycle-index`: Đánh chỉ mục kép bằng Graft + Graphify (AST + Semantic GraphRAG).
- `devcycle-spec`: Soạn thảo PRD & Acceptance Criteria chống ảo giác 100%.
- `devcycle-issues`: Phân rã tính năng thành vertical tracer-bullet issues kèm đo lường Blast Radius.
- `devcycle-tdd`: Lập trình Test-Driven Development chuẩn Matt Pocock (Red-Green-Refactor + Polyglot Lint).
- `devcycle-ui`: Thiết kế và tích hợp UI/UX hiện đại, responsive, micro-animations cho Web & Desktop.
- `devcycle-e2e`: Kiểm thử tích hợp & đầu cuối E2E (Playwright, Cypress, API Supertest, pywinauto).
- `devcycle-debug`: Điều tra và chẩn đoán lỗi dựa trên bằng chứng log runtime thực tế.
- `devcycle-bugfix`: Quy trình sửa lỗi 7 bước kèm sổ cái hội tụ nguyên nhân gốc rễ (`root-causes.md`).
- `devcycle-refine`: Tinh chỉnh kiến trúc sau khi pass test: khử god-nodes, tách domain khỏi UI.
- `devcycle-security`: Đánh giá bảo mật toàn diện đa tầng chuẩn Borghei Red-Team (SAST, DAST, API Fuzzing, Secrets, SCA, Container, Desktop, Mobile, Cloud) kèm cơ chế tự động cài đặt công cụ on-demand.
- `devcycle-audit`: Kiểm toán khoảng cách giữa PRD và thực tế mã nguồn sau triển khai.
- `jira-fetch`: Đọc thông tin ticket, mô tả và file đính kèm từ Jira REST API.
- `jira-bugfix`: Quy trình sửa lỗi test-first điều phối bởi Jira ticket.

### 2. UI/UX, Animation & Design Intelligence (28 Skills)
- `animate`, `animate-expo`, `animation-vocabulary`, `apple-design`, `emil-design-eng`, `find-animation-opportunities`, `improve-animations`, `review-animations`, `pick-ui-library`, `ask-sonner`, `mobile-native`, `prototype`, `write-swift` *(từ emilkowalski/skills)*.
- `taste-skill-web`, `taste-skill-v1`, `brutalist-skill`, `minimalist-skill`, `output-skill`, `redesign-skill`, `soft-skill`, `stitch-skill`, `brandkit`, `gpt-tasteskill`, `imagegen-frontend-mobile`, `imagegen-frontend-web`, `image-to-code-skill` *(từ Leonxlnx/taste-skill)*.
- `impeccable-design` *(từ pbakaus/impeccable)*.
- `ui-ux-pro-max` *(Design Intelligence System)*.

### 3. Core Senior Engineering Skills (4 Skills)
- `senior-dev-pipeline`: Master pipeline 4 giai đoạn chuẩn Senior 15 năm kinh nghiệm.
- `spec-engineering`: Kỹ nghệ đặc tả phần mềm & kiểm chứng ràng buộc kỹ thuật.
- `tdd-development`: Lập trình TDD chuẩn Matt Pocock & Clean Architecture.
- `redteam-security`: Đánh giá bảo mật, rà quét lỗ hổng và kiểm thử xâm nhập chuyên sâu.

---

## 💡 Hướng Dẫn Sử Dụng Nhanh (Cheat Sheet)

```bash
# 1. Chạy toàn bộ chu trình phát triển cho 1 tính năng mới:
/devcycle "Tích hợp tính năng lịch âm và nhắc nhở ngày hoàng đạo"

# 2. Đánh chỉ mục codebase dự án hiện tại:
python ~/.gemini/config/skills/devcycle-index/scripts/index_codebase.py .

# 3. Lập trình TDD cho 1 task cụ thể:
/devcycle-tdd "Tạo service tính toán can chi ngày tháng"

# 4. Quét bảo mật toàn diện dự án:
/devcycle-security .

# 5. Kiểm tra chất lượng code & linter đa ngôn ngữ:
python ~/.gemini/config/skills/devcycle-tdd/scripts/lint.py .
```
