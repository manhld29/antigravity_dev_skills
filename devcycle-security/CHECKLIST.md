# Comprehensive Security Checklist — Web, API, Desktop, Mobile & Cloud

Bảng kiểm tra an ninh toàn diện dành cho Red-Team & Senior Security Engineer (DevCycle Phase 6.5).
Mỗi hạng mục bao gồm: **Mã lỗ hổng (CWE/OWASP)**, **Grep pattern / Truy vấn AST**, **Công cụ tự động đề xuất**, **Câu hỏi xác minh Source→Sink**, và **Giải pháp khắc phục**.

> ⚡ **Quy tắc Auto-Setup**: Nếu công cụ chưa có trong môi trường, AI tự động chạy lệnh cài đặt (`pip install`, `npm install -g`, `go install`, `curl/sh`...) trước khi quét.

---

## 1. Command & Code Injection (Critical / High)

| Hạng mục (CWE) | Grep Pattern / AST Pattern | Công cụ tự động | Câu hỏi Source→Sink | Giải pháp triệt để |
|---|---|---|---|---|
| **OS Command Injection** (CWE-78) | `subprocess.*shell=True`, `os.system`, `os.popen`, `child_process.exec`, `exec.Command` | `secscan.py`, `semgrep`, `bandit` | Dữ liệu đầu vào từ user/network/file có nối thẳng vào shell string không? | Dùng `shell=False` + argument list; không bao giờ format chuỗi vào shell |
| **Code Injection / Dynamic Eval** (CWE-94/95) | `\beval\(`, `\bexec\(`, `new Function\(`, `compile\(`, `__import__\(` | `secscan.py`, `semgrep`, `bandit` | Đoạn mã được eval/exec có chứa biến người dùng kiểm soát được không? | Xóa bỏ `eval`/`exec`; chuyển sang AST parser hoặc cấu trúc dữ liệu tường minh |
| **Insecure Deserialization** (CWE-502) | `pickle\.loads?`, `marshal\.loads`, `yaml\.load\([^)]*(?!SafeLoader)`, `unserialize\(` | `secscan.py`, `semgrep`, `bandit` | Dữ liệu deserialize có đến từ nguồn không tin cậy (request body, cookie, socket)? | Dùng `yaml.safe_load`; tuyệt đối không unpickle dữ liệu ngoài — dùng JSON/Protocol Buffers |
| **Template / SSTI Injection** (CWE-1336) | `render_template_string`, `Template\(.*input`, `\.format\(.*\binput` | `semgrep`, `secscan.py` | Chuỗi template có bị ghép với user input trước khi render không? | Truyền biến vào context của template engine, không nối chuỗi template |

---

## 2. Injection vào Data Stores (High)

| Hạng mục (CWE) | Grep Pattern | Công cụ tự động | Câu hỏi Source→Sink | Giải pháp triệt để |
|---|---|---|---|---|
| **SQL Injection** (CWE-89) | `execute\(.*%`, `execute\(.*\+`, `execute\(f"`, `\$queryRawUnsafe`, `QSqlQuery\(.*\+` | `secscan.py`, `semgrep`, `schemathesis` | Câu lệnh SQL có nối chuỗi trực tiếp với biến người dùng? | Dùng Prepared Statements / Parameterized Queries: `cursor.execute(sql, (a, b))` |
| **NoSQL Injection** (CWE-943) | `\$where`, `collection\.find\(\s*\{.*req\.body`, `bson\.M\{` | `semgrep`, `secscan.py` | Query NoSQL có nhận thẳng object từ req.body mà không ép kiểu? | Ép kiểu dữ liệu (string/int), sanitize toán tử `$gt`, `$ne` |
| **Path Traversal** (CWE-22) | `open\(`, `Path\(`, `os\.path\.join\(`, `fs\.readFile\(`, `send_file`, `QFile\(` | `secscan.py`, `semgrep`, `nuclei` | Tên file/đường dẫn có chứa `../` hoặc nhận trực tiếp từ user? | Dùng `Path.resolve()` kiểm tra nằm dưới thư mục gốc cho phép; whitelist filename |
| **XXE / XML Injection** (CWE-611) | `xml\.etree`, `lxml\.etree`, `minidom`, `DocumentBuilderFactory` | `semgrep`, `bandit` | Trình phân tích XML có bật external entities (DTD)? | Dùng `defusedxml` (Python) hoặc vô hiệu hóa DTD/External Entity resolution |

---

## 3. Web & API Security (OWASP Top 10 & DAST)

| Hạng mục (CWE) | Pattern / Bề mặt tấn công | Công cụ kiểm thử | Tiêu chí đánh giá | Khắc phục |
|---|---|---|---|---|
| **API Contract & Fuzzing** | Toàn bộ REST / GraphQL / OpenAPI endpoints | `schemathesis`, `dredd`, `ffuf` | Fuzzing input biên, type mismatch, payload đột biến gây 500 error | Validation strict qua Pydantic / Zod; xử lý exception chuẩn |
| **JWT Vulnerabilities** (CWE-345/347) | Header & signature JWT: `alg:none`, weak secret, key confusion | `jwt_tool`, `secscan.py` | Token có bị giải mã/sửa đổi khi đổi sang alg `none` hoặc dùng public key làm HMAC? | Enforce thuật toán cụ thể (e.g. RS256 hoặc HS256 với secret > 256 bit) |
| **Cross-Site Scripting (XSS)** (CWE-79) | `dangerouslySetInnerHTML`, `v-html`, `innerHTML`, `document.write` | `semgrep`, `eslint-plugin-security`, `nuclei` | Dữ liệu người dùng có được inject trực tiếp vào DOM mà không escape? | Escape HTML hoặc dùng thư viện DOMPurify / textContent |
| **Broken Access Control (IDOR)** (CWE-639) | `GET /api/users/{id}`, `PUT /api/orders/{id}` | `schemathesis`, `OWASP ZAP` | User A có thể truy cập/sửa bản ghi của User B bằng cách thay đổi ID? | Kiểm tra quyền sở hữu bản ghi (Ownership check) tại tầng Service/Repository |
| **CORS Misconfiguration** (CWE-942) | `allow_origins=["*"]` kèm `allow_credentials=True` | `secscan.py`, `nuclei` | Phản hồi header `Access-Control-Allow-Origin: *` khi có mang Cookie/Auth? | Whitelist domain cụ thể; không bao giờ dùng `*` kèm credentials |
| **SSRF** (CWE-918) | `requests\.get\(.*url`, `fetch\(.*userInput`, `urlopen\(` | `semgrep`, `nuclei` | URL đích có thể trỏ tới `127.0.0.1`, `169.254.169.254` (cloud metadata)? | Whitelist IP/domain; chặn private CIDR (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) |

---

## 4. Secrets, Passwords & Thông Tin Nhạy Cảm (High)

| Hạng mục | Pattern / Vị trí | Công cụ tự động | Yêu cầu kiểm tra | Khắc phục |
|---|---|---|---|---|
| **Hardcoded Secrets** (CWE-798) | API key, JWT secret, AWS key, Private key trong code | `gitleaks`, `trufflehog`, `detect-secrets` | Có secret thật nào bị hardcode trong source hoặc git history không? | Đưa vào `.env` (git-ignored) hoặc Secret Manager (Vault, AWS Secrets Manager) |
| **Credentials trong Log** (CWE-532) | `logger\.info\(.*password`, `print\(.*token`, `console\.log` | `secscan.py`, `semgrep` | Log có in password, auth token, thẻ tín dụng không? | Mặt nạ hóa (masking) hoặc loại bỏ trường nhạy cảm trước khi log |
| **Plaintext Storage** (CWE-312) | Lưu token vào `QSettings`, file `.ini`, localStorage | `secscan.py`, grep | Mật khẩu/token có được lưu bằng plaintext trên máy người dùng không? | Sử dụng OS Keyring (DPAPI, macOS Keychain, SecretService) |
| **Weak Password Hash** (CWE-327/328) | `md5`, `sha1`, `sha256` không salt dùng cho password | `secscan.py`, `bandit` | Mật khẩu lưu trong DB có dùng hash nhanh không an toàn? | Chuyển sang Argon2id hoặc bcrypt (cost factor >= 12) |

---

## 5. Desktop Application (PySide6 / Qt / C++ / Electron)

| Hạng mục | Pattern / Bề mặt tấn công | Công cụ kiểm thử | Rủi ro đặc thù | Khắc phục |
|---|---|---|---|---|
| **Local Port & Socket IPC** | Local TCP socket (e.g. `127.0.0.1:9000`), WebSocket | `nmap`, `nc`, `tshark` | Tiến trình khác trên máy có thể gửi lệnh điều khiển trái phép không? | Yêu cầu token xác thực hoặc dùng Named Pipes / Unix domain socket có ACL |
| **Custom URI Scheme** | `fcds://`, `myapp://` đăng ký với hệ điều hành | Grep đăng ký protocol | Kẻ tấn công trên web có thể kích hoạt app với tham số độc hại không? | Parse URL an toàn; không chuyển tham số URL trực tiếp vào shell hoặc exec |
| **DLL / Search Path Hijack** (CWE-427) | `LoadLibrary`, `ctypes.WinDLL` không có đường dẫn tuyệt đối | `Process Monitor`, `x64dbg` | Ứng dụng có thể bị tải mã độc từ DLL cùng thư mục không? | Gọi `SetDefaultDllDirectories` và luôn load DLL theo đường dẫn tuyệt đối |
| **QWebEngineView Remote JS** (CWE-79/94) | `setHtml\(.*\+`, `runJavaScript\(.*\+`, `QWebChannel` | `secscan.py`, code review | XSS trong embedded browser dẫn tới RCE ra ngoài máy host qua QWebChannel | Tắt JavaScript nếu không cần thiết; cô lập context; sanitize mọi payload |
| **Binary Memory & Reversing** | File thực thi (.exe, .so, ELF, Mach-O) | `ghidra`, `strings`, `Detect It Easy` | Có string nhạy cảm, API key hoặc thuật toán giải mã bị lộ trong binary? | Không hardcode key; áp dụng string obfuscation & stripping symbols |

---

## 6. Mobile Application (Android / iOS)

| Hạng mục | Bề mặt kiểm thử | Công cụ | Rủi ro | Khắc phục |
|---|---|---|---|---|
| **Decompilation & Hardcoded Secrets** | File APK / AAB | `jadx`, `apktool`, `MobSF` | API keys, endpoint admin bị trích xuất từ bytecode/smali | Đưa logic bí mật về backend; áp dụng ProGuard/R8 |
| **Runtime Tampering & Hooking** | Hàm auth, check root, SSL pinning | `frida`, `objection` | Kẻ tấn công hook hàm trả về `true` để vượt qua xác thực | Triển khai root/tamper detection đa lớp; không phụ thuộc client-side |
| **Insecure Data Storage** | SharedPreferences, SQLite, External storage | `adb shell`, `MobSF` | Token/passphrase lưu plaintext trong file app data | Dùng Android EncryptedSharedPreferences / Keystore |
| **Cleartext HTTP Traffic** | `android:usesCleartextTraffic="true"` | `MobSF`, `mitmproxy` | Traffic gửi qua HTTP thường bị nghe lén (MitM) | Bắt buộc HTTPS; cấu hình Network Security Config chỉ cho phép TLS |

---

## 7. Container, Docker & Supply Chain (SCA / IaC)

| Hạng mục | Đối tượng quét | Lệnh công cụ tự động | Rủi ro | Khắc phục |
|---|---|---|---|---|
| **Dependency CVEs (SCA)** | `requirements.txt`, `package.json`, `Cargo.lock`, `go.mod` | `pip-audit`, `npm audit`, `cargo audit`, `govulncheck`, `trivy fs .` | Sử dụng thư viện bên ngoài có lỗ hổng RCE / DoS đã công bố | Cập nhật version an toàn; loại bỏ package unmaintained |
| **Container Image CVEs** | Docker base image, layers | `trivy image <IMAGE>`, `grype <IMAGE>` | Base image cũ (e.g. Alpine 3.12, Debian 10) chứa hàng chục CVE Critical | Dùng base image distroless hoặc phiên bản mới nhất có hỗ trợ LTS |
| **Dockerfile Security** | `Dockerfile` | `hadolint Dockerfile` | Chạy quyền root (`USER root`), cài package không pin version | Thêm non-root user (`USER appuser`); tối ưu multi-stage build |
| **IaC Misconfiguration** | Terraform (`.tf`), Kubernetes (`.yaml`), CloudFormation | `checkov -d .`, `terrascan scan` | Bucket S3 public, open security group (0.0.0.0/0 port 22/3389) | Áp dụng nguyên tắc Least Privilege; chặn public access mặc định |

---

## 8. Network & Port Security

| Hạng mục | Phạm vi | Lệnh kích hoạt | Mục tiêu kiểm tra |
|---|---|---|---|
| **Port Discovery & Service Detection** | Server / Container / Host | `nmap -sV -sC -p- <TARGET>` hoặc `rustscan -a <TARGET>` | Phát hiện port mở không cần thiết (debug port, redis không pass) |
| **Network Traffic Inspection** | Card mạng cục bộ / Socket | `tshark -i any -f "port 8000 or 9000"` | Đảm bảo dữ liệu nhạy cảm truyền qua mạng được mã hóa (TLS) |

---

## Tóm Tắt Quy Trình Thực Thi:
1. **Kiểm tra công cụ**: Chạy `which <tool>` -> Nếu thiếu: Chạy lệnh tự động cài đặt.
2. **Quét tự động**: Thu thập leads từ các công cụ (secscan.py, semgrep, gitleaks, schemathesis...).
3. **Xác minh Source→Sink**: Kiểm chứng luồng dữ liệu độc hại có thực sự kích hoạt được sink hay không.
4. **Viết PoC an toàn**: Tạo minimal PoC chứng minh lỗ hổng trên môi trường dev.
5. **Ghi nhận & Loopback**: Ghi vào `docs/security/<date>-report.md` và chuyển giao về Phase 1 (`devcycle-spec`) để tạo TDD test và sửa triệt để.
