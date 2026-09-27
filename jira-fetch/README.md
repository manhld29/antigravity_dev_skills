# jira-fetch

Tra cứu chi tiết một issue Jira theo **URL** hoặc **key** (ví dụ `PROJ-123`), đọc cấu hình kết nối từ [`.claude/.env`](../../.env), gọi Jira REST API (Cloud v3 hoặc Server/DC v2) **chỉ bằng thư viện chuẩn của Python** (không cần `pip install`) và in ra một bản tóm tắt Markdown dễ đọc.

- **Read-only** — skill này không bao giờ sửa, chuyển trạng thái, hay comment vào issue.
- **Secret-safe** — không bao giờ in `JIRA_API_TOKEN`; lỗi auth được báo mà không lộ token.

## Khi nào dùng

Khi bạn dán một link Jira / một issue key, hoặc nói: "lấy thông tin Jira", "xem ticket Jira", "what's in PROJ-123", "jira-fetch". Đây cũng là **Phase 1** của orchestrator [jira-bugfix](../jira-bugfix/README.md).

## Cấu hình (`.claude/.env`)

| Key | Bắt buộc | Ý nghĩa |
|-----|----------|---------|
| `JIRA_DOMAIN` | có\* | host, **không** kèm scheme — vd `your-company.atlassian.net` hoặc `jira.fci.vn` |
| `JIRA_EMAIL` | với basic | email tài khoản (Cloud) hoặc username (Server/DC dùng password) |
| `JIRA_API_TOKEN` | có | API token (Cloud) hoặc Personal Access Token / password (Server/DC) |
| `JIRA_AUTH_TYPE` | không | `basic` (mặc định, Cloud) hoặc `bearer` (Server/DC PAT) |
| `JIRA_API_VERSION` | không | `3` (mặc định, Cloud) hoặc `2` (Server/DC) |

\* Nếu input là một URL đầy đủ thì host trong URL sẽ **override** `JIRA_DOMAIN`, nên cấu hình chỉ-key vẫn chạy được trên nhiều site Jira.

> `.claude/.env` chứa secret thật → **phải** được git-ignore (đã thêm vào `.gitignore`). Tuyệt đối không in `JIRA_API_TOKEN`.

### Lấy token ở đâu

- **Jira Cloud** (`*.atlassian.net`): tạo token tại <https://id.atlassian.com/manage-profile/security/api-tokens> — đặt `JIRA_AUTH_TYPE=basic`, `JIRA_API_VERSION=3`, `JIRA_EMAIL` = email tài khoản.
- **Jira Server/DC** (vd `jira.fci.vn`): không có trang token của `id.atlassian.com`. Dùng `JIRA_API_VERSION=2` và một trong hai:
  - **Personal Access Token** (avatar → Profile → "Personal Access Tokens" → Create): `JIRA_AUTH_TYPE=bearer`, `JIRA_API_TOKEN=<PAT>`.
  - **Username + password** (Jira cũ): `JIRA_AUTH_TYPE=basic`, `JIRA_EMAIL=<username>`, `JIRA_API_TOKEN=<password>`.

### Ví dụ `.claude/.env`

```dotenv
# Jira Cloud
JIRA_DOMAIN=your-company.atlassian.net
JIRA_EMAIL=you@company.com
JIRA_API_TOKEN=xxxxxxxxxxxxxxxxxxxx
JIRA_AUTH_TYPE=basic
JIRA_API_VERSION=3

# Jira Server/DC (FCI) — dùng PAT
# JIRA_DOMAIN=jira.fci.vn
# JIRA_API_TOKEN=xxxxxxxxxxxxxxxxxxxx
# JIRA_AUTH_TYPE=bearer
# JIRA_API_VERSION=2
```

## Cách dùng

### Qua AI (khuyến nghị)

Dán key hoặc URL và yêu cầu, hoặc gọi slash command:

```
/jira-fetch PROJ-123
/jira-fetch https://your-company.atlassian.net/browse/PROJ-123
```

### Chạy script trực tiếp

Từ thư mục gốc project:

```bash
python .claude/skills/jira-fetch/scripts/jira_fetch.py "<url-or-key>"
```

Các flag:

| Flag | Tác dụng |
|------|----------|
| `--comments` | lấy và in cả comment của issue |
| `--raw` | in JSON thô (khi cần custom field không có trong bản tóm tắt) |
| `--env PATH` | trỏ tới một file `.env` khác (mặc định tự dò ngược từ cwd lên) |

Ví dụ:

```bash
# Bản tóm tắt + comment
python .claude/skills/jira-fetch/scripts/jira_fetch.py PROJ-123 --comments

# JSON thô để lấy custom field
python .claude/skills/jira-fetch/scripts/jira_fetch.py PROJ-123 --raw
```

## Output

Script trích key từ input (bare key / browse URL / REST URL), chọn Basic hoặc Bearer auth, gọi `/rest/api/{version}/issue/{key}`, flatten phần Description (xử lý cả ADF JSON của Cloud v3 lẫn plain text/wiki của Server v2), rồi in:

- Tiêu đề `# KEY: summary`
- Type · Status · Priority · Assignee · Reporter · Parent · Labels · Component · Fix version · Resolution · Created · Updated
- `## Description` (đã flatten)
- `## Comments` (nếu có `--comments`)
- Link `…/browse/KEY`

## Xử lý lỗi

Script in chẩn đoán mà không lộ secret:

- **401 / 403** — token sai hoặc không đủ quyền.
- **404** — sai key hoặc sai domain.
- **URLError** — không kết nối được tới host (mạng/VPN/domain).

Khi gặp lỗi, sửa cấu hình rồi chạy lại — đừng thử lại mù với token khác trừ khi bạn chủ động đổi.

## Ghi chú

- Stdlib-only (`urllib`) — chạy bằng Python sẵn có của project, không cần cài thêm.
- Với nhiều issue trong một lượt, gọi script một lần cho mỗi key thay vì hỏi lại cấu hình.
