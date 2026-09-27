---
name: devcycle-security
description: "Act as a 15-year Senior Red-Team Penetration Tester & Security Architect (Borghei Red-Team standards). Conducts comprehensive security audits across Web, API, Desktop, Mobile, Cloud, Containers, and Supply-Chain: SAST (Semgrep, Bandit, gosec, secscan.py), DAST (OWASP ZAP, Nuclei, Nikto), API Fuzzing (Schemathesis, JWT Tool, ffuf), Secrets (Gitleaks, TruffleHog), SCA/SBOM (Trivy, Grype, pip-audit, npm audit), IaC (Checkov, Hadolint), Network (Nmap, RustScan), and Desktop/Mobile inspection (Ghidra, Frida, JADX). AI is fully authorized to auto-install missing tools on demand. Flaws loop back to Phase 1 via docs/debug/root-causes.md. Stage 6.5 of devcycle. Triggers: \"security review\", \"find vulnerabilities\", \"pentest codebase\", \"devcycle-security\", \"kiểm tra bảo mật\"."
argument-hint: "Scope: whole repo or path to review, e.g. . or ./backend"
---

# Devcycle — Security (Borghei 15-Year Senior Red-Team & Comprehensive Security Testing)

Stage 6.5 of [devcycle](../devcycle/SKILL.md). A **mandatory white-box & gray-box security audit** conducted before any feature is marked complete. Evaluates the application through the lens of an elite attacker with source access, API access, and runtime capability.

---

## ⚡ MANDATORY RULE: Autonomous Tooling Auto-Setup (Zero Friction)

> **QUY TẮC CỐT LÕI VỀ CÔNG CỤ**:
> Khi tiến hành kiểm thử bảo mật, **nếu công cụ nào được sử dụng tới mà chưa được cài đặt trong môi trường, AI CÓ TOÀN QUYỀN TỰ ĐỘNG THỰC THI LỆNH CÀI ĐẶT NGAY LẬP TỨC** (`pip install`, `npm install -g`, `go install`, `cargo install`, `curl/sh`, `apt-get`...) mà không cần phải chờ đợi hay dừng pipeline.

### Quick Auto-Install Reference:
```bash
# SAST & Code Security
which semgrep >/dev/null 2>&1 || pip install semgrep
which bandit >/dev/null 2>&1 || pip install bandit
which bearer >/dev/null 2>&1 || curl -sfL https://raw.githubusercontent.com/Bearer/bearer/main/contrib/install.sh | sh

# Secrets & Leakage
which gitleaks >/dev/null 2>&1 || (curl -sSfL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks-linux-x64.tar.gz | tar -xz -C /usr/local/bin 2>/dev/null || pip install detect-secrets)
which trufflehog >/dev/null 2>&1 || curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /tmp

# SCA / Dependencies & Containers
which trivy >/dev/null 2>&1 || (curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /tmp 2>/dev/null || true)
which pip-audit >/dev/null 2>&1 || pip install pip-audit
which grype >/dev/null 2>&1 || curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /tmp
which syft >/dev/null 2>&1 || curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /tmp
which hadolint >/dev/null 2>&1 || (curl -sSfL https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64 -o /tmp/hadolint && chmod +x /tmp/hadolint)
which checkov >/dev/null 2>&1 || pip install checkov

# API & Web DAST / Fuzzing
which schemathesis >/dev/null 2>&1 || pip install schemathesis
which nuclei >/dev/null 2>&1 || (go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest 2>/dev/null || true)
which ffuf >/dev/null 2>&1 || (go install github.com/ffuf/ffuf/v2@latest 2>/dev/null || true)
which nikto >/dev/null 2>&1 || (sudo apt-get update && sudo apt-get install -y nikto 2>/dev/null || true)
which jwt_tool >/dev/null 2>&1 || pip install pyjwt cryptography requests

# Cloud & Network
which nmap >/dev/null 2>&1 || (sudo apt-get update && sudo apt-get install -y nmap 2>/dev/null || true)
which prowler >/dev/null 2>&1 || pip install prowler
```

---

## 1. Danh Mục Toàn Diện Các Công Cụ Kiểm Thử Bảo Mật

Bộ công cụ được chia theo từng lớp phòng thủ và bề mặt tấn công thực tế:

### 1. Web Application Security (DAST & Web Scanner)
| Công cụ | Loại | Mục đích & Điểm mạnh | Lệnh kích hoạt |
|---|---|---|---|
| **Burp Suite** | GUI / Proxy | Intercept HTTP/HTTPS, fuzzing, auth bypass, SQLi/XSS | Manual / Proxy mode |
| **OWASP ZAP** | CLI / DAST | DAST quét lỗ hổng tự động, baseline web scan | `zap-baseline.py -t <URL>` / docker zap |
| **Nikto** | CLI | Quét web server, cấu hình nguy hiểm, file mặc định | `nikto -h <URL>` |
| **Nuclei** | CLI | Template-based vulnerability scanner (cực nhanh, CVE mới nhất) | `nuclei -u <URL>` |
| **Wapiti** | CLI | Black-box web vulnerability scanner | `wapiti -u <URL>` (`pip install wapiti3`) |
| **w3af** | CLI/GUI | Framework tấn công và kiểm toán web application | Python audit |
| **ffuf** | CLI | Fuzzing URL path, directory, parameter, virtual host | `ffuf -u <URL>/FUZZ -w <wordlist>` |
| **Gobuster** | CLI | Enumeration thư mục, file, subdomains, VHost | `gobuster dir -u <URL> -w <wordlist>` |
| **Feroxbuster** | CLI | Content discovery tốc độ cao viết bằng Rust | `feroxbuster -u <URL>` |

### 2. API Security & Specification Fuzzing
| Công cụ | Mục đích | Lệnh kích hoạt |
|---|---|---|
| **Schemathesis** | Fuzzing API tự động dựa trên OpenAPI/Swagger/GraphQL | `schemathesis run <openapi_url_or_json>` |
| **Dredd** | Kiểm thử API contracts & specs | `dredd <api_desc> <api_url>` |
| **Kiterunner** | Discovery endpoint và route API ẩn | `kr scan <URL> -w routes.kite` |
| **JWT Tool** | Phân tích, giả mạo token JWT (`alg:none`, key confusion, brute-force) | `python jwt_tool.py <token>` |
| **ffuf** | Parameter fuzzing, JSON body injection fuzzing | `ffuf -u <URL> -X POST -d '{"param":"FUZZ"}'` |
| **OWASP ZAP API** | Quét tự động API endpoints từ OpenAPI schema | `zap-api-scan.py -t openapi.json -f openapi` |

### 3. Network & Infrastructure Security
| Công cụ | Mục đích | Lệnh kích hoạt |
|---|---|---|
| **Nmap** | Quét cổng, nhận diện service, OS detection, chạy NSE scripts | `nmap -sV -sC -p- <TARGET>` |
| **Masscan / RustScan** | Quét cổng quy mô lớn với tốc độ cực cao | `rustscan -a <TARGET> -- -sC -sV` |
| **Wireshark / tshark** | Bắt và phân tích packet mạng sâu | `tshark -i any -f "tcp port 8000 or 9000"` |
| **tcpdump** | Packet capture CLI gọn nhẹ | `tcpdump -nn -i lo port 8000` |
| **Netcat (`nc`)** | Kiểm tra kết nối TCP/UDP socket, banner grabbing | `nc -zv <HOST> <PORT>` |
| **OpenVAS / Nessus** | Quét lỗ hổng hạ tầng và server chuyên sâu | Enterprise scan |

### 4. Source Code Security (SAST)
| Công cụ | Ngôn ngữ / Mục tiêu | Lệnh kích hoạt |
|---|---|---|
| **secscan.py** | Universal (Python, JS/TS, Go, Rust, Java, SQL) - zero dependency | `python scripts/secscan.py . --format md` |
| **Semgrep** | Universal AST SAST, rules OWASP & CVE | `semgrep scan --config auto .` |
| **Bandit** | Python AST security linter (injection, pickle, exec) | `bandit -r . -ll` |
| **gosec** | Go security static analysis | `gosec ./...` |
| **Brakeman** | Ruby on Rails security scanner | `brakeman` |
| **ESLint Security** | JavaScript / TypeScript security plugin | `npx eslint --plugin security .` |
| **SpotBugs + FindSecBugs** | Java bytecode security analyzer | Maven/Gradle plugin |
| **PHPStan / Psalm** | PHP static analysis & type safety | `vendor/bin/phpstan analyse` |
| **Bearer** | Data security & sensitive data flow analysis | `bearer scan .` |
| **SonarQube / CodeQL** | Enterprise deep static analysis | CI/CD pipeline |

### 5. Dependency & Supply-Chain Security (SCA & SBOM)
| Công cụ | Phạm vi | Lệnh kích hoạt |
|---|---|---|
| **Trivy** | Filesystem, dependencies, containers, IaC | `trivy fs --severity HIGH,CRITICAL .` |
| **Grype** | Vulnerability scanner cho source/image/SBOM | `grype .` |
| **Syft** | Sinh Software Bill of Materials (SBOM) | `syft . -o json > sbom.json` |
| **pip-audit** | Kiểm tra CVE trong Python packages (`requirements.txt`, `pyproject.toml`) | `pip-audit` |
| **npm audit** | Kiểm tra CVE trong Node.js `package-lock.json` | `npm audit` |
| **cargo audit** | Quét lỗ hổng Rust crates trong `Cargo.lock` | `cargo audit` |
| **govulncheck** | Quét lỗ hổng chính thức của Go dependencies | `govulncheck ./...` |
| **OWASP Dependency-Check**| Quét dependencies đa ngôn ngữ đối chiếu NVD CVE | `dependency-check --project <P> --scan .` |

### 6. Container, Docker, Kubernetes & IaC Security
| Công cụ | Mục đích | Lệnh kích hoạt |
|---|---|---|
| **Trivy Image Scan** | Quét lỗ hổng base image và layer Docker | `trivy image <IMAGE_TAG>` |
| **Hadolint** | Linter bảo mật và best practice cho Dockerfile | `hadolint Dockerfile` |
| **Checkov** | Quét bảo mật IaC (Terraform, Dockerfile, K8s, CloudFormation) | `checkov -d .` |
| **Terrascan** | Static code analyzer cho Terraform/IaC | `terrascan scan` |
| **Kube-bench / Kube-hunter**| Kiểm tra CIS benchmark và an ninh Kubernetes cluster | `kube-bench` / `kube-hunter` |

### 7. Authentication, Session & Password Auditing
| Công cụ | Mục đích | Lưu ý |
|---|---|---|
| **JWT Tool** | Khai thác lỗi JWT (`alg:none`, key tampering, weak secret brute) | Chỉ test trên môi trường dev nội bộ |
| **Hydra / Medusa** | Kiểm tra khả năng chống tấn công brute-force authentication | Cần rate-limiting guard |
| **John the Ripper / Hashcat**| Kiểm tra độ mạnh của password hash (MD5, SHA1, bcrypt) | Phát hiện weak salt/rounds |
| **CrackMapExec / NetExec**| Đánh giá môi trường mạng Active Directory / SMB / WinRM | Môi trường enterprise |

### 8. Mobile Application Security (Android / iOS)
| Công cụ | Mục đích | Luồng kiểm thử chuẩn |
|---|---|---|
| **MobSF** | Mobile Security Framework (Static & Dynamic APK analyzer) | Quét tự động APK / IPA |
| **JADX / apktool** | Decompile file APK về mã nguồn Java/Smali | Phân tích hardcoded secrets, endpoints |
| **Frida / Objection** | Dynamic instrumentation, hook hàm, bypass SSL pinning | Runtime analysis trên emulator/thiết bị |
| **adb** | Android debug bridge, kiểm tra logcat, intent, storage | `adb logcat \| grep -E "secret\|token"` |
| **mitmproxy / Burp** | Bắt và kiểm tra toàn bộ traffic HTTP/HTTPS của app | Kiểm tra TLS pinning & payload |

### 9. Desktop Application Security (PySide6 / C++ / Qt / Electron / Native)
Đối với ứng dụng desktop (như PySide6/Qt, Electron, C++):
| Công cụ | Mục đích |
|---|---|
| **Ghidra / IDA Free** | Reverse engineering và phân tích binary (.exe, .so, .dll) |
| **x64dbg / GDB** | Debug runtime, kiểm tra bộ nhớ, memory tampering |
| **Process Monitor (ProcMon)** | Giám sát file, registry, process creation, IPC |
| **Process Explorer** | Phân tích DLLs, handles, token permissions |
| **Wireshark / mitmproxy** | Bắt gói tin socket nội bộ (e.g. TCP 9000, IPC, WebSocket) |
| **Frida** | Runtime function hooking (hook hàm xác thực, scrambler, token) |
| **strings / Detect It Easy (DIE)** | Trích xuất chuỗi nhạy cảm, phát hiện packer/compiler |
| **YARA** | Viết rule quét pattern mã độc hoặc token format |

> **Bề mặt tấn công đặc thù Desktop**:
> - Token & Credential Storage: Có lưu vào `QSettings`, file INI, plaintext hay OS Keyring? (CWE-312)
> - IPC & Local Sockets: Local port (e.g. 127.0.0.1:9000) có xác thực nguồn gửi không?
> - Custom URI Schemes: Giao thức tùy biến (e.g. `myapp://` / `fcds://`) có bị injection tham số không?
> - DLL Hijacking: Có tải thư viện DLL bằng đường dẫn tương đối không? (CWE-427)
> - QWebEngineView: Có render HTML không an toàn hoặc inject JS trực tiếp không? (CWE-79/CWE-94)

### 10. Secrets & Credential Leakage
| Công cụ | Mục đích | Lệnh kích hoạt |
|---|---|---|
| **Gitleaks** | Quét lịch sử git và thư mục tìm API keys, private keys, passwords | `gitleaks detect --source . -v` |
| **TruffleHog** | Tìm kiếm secret entropy cao trong repo và filesystem | `trufflehog filesystem .` |
| **detect-secrets** | Tool của Yelp nhận diện credential patterns | `detect-secrets scan` |
| **GitGuardian CLI** | Quét secret chuyên sâu trước khi push | `ggshield secret scan path .` |

### 11. Cloud Security & Posture Management
| Công cụ | Phạm vi | Lệnh kích hoạt |
|---|---|---|
| **Prowler** | Đánh giá an ninh AWS/Azure/GCP theo chuẩn CIS, ISO 27001 | `prowler aws` |
| **ScoutSuite** | Multi-cloud security auditing tool | `scout aws` |
| **Checkov / Trivy** | Quét cấu hình Cloud IaC (S3 public, open security groups) | `checkov -d ./terraform` |
| **Pacu** | AWS exploitation & post-exploitation framework | Audit AWS IAM policies |

---

## 2. Quy Trình Thực Thi Kiểm Thử 4 Tầng Chuẩn Hóa

Khi chạy `devcycle-security` trên một dự án, AI tự động thực hiện 4 tầng kiểm thử:

```
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 1: QUÉT NHANH (Fast Developer Pass - < 30s)                       │
│ 1. Tự cài & chạy secscan.py (Built-in static rules)                    │
│ 2. Tự cài & chạy Gitleaks / detect-secrets (Chống lộ secret, API key)  │
│ 3. Tự cài & chạy pip-audit / npm audit / cargo audit (SCA dependencies)│
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 2: SAST & API FUZZING CHUYÊN SÂU (Deep Analysis Pass)             │
│ 1. Tự cài & chạy Semgrep / Bandit / gosec (AST rule-based)             │
│ 2. Fuzzing API với Schemathesis (Nếu dự án có OpenAPI/FastAPI/REST)    │
│ 3. Quét cấu hình IaC/Dockerfile với Hadolint / Checkov                 │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 3: DAST, CONTAINER & NETWORK PASS (Runtime Verification)          │
│ 1. Quét DAST endpoint cục bộ với Nuclei / OWASP ZAP / Nikto           │
│ 2. Quét Docker container base image với Trivy / Grype                  │
│ 3. Kiểm tra cổng mạng mở và dịch vụ nội bộ với Nmap / netcat           │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TẦNG 4: CHUYÊN BIỆT THEO KIẾN TRÚC (Desktop / Mobile / Cloud)         │
│ - Desktop (PySide6): Check QSettings, local TCP 9000, URI handlers    │
│ - Mobile (Android): Check MobSF, JADX decompilation, intent filters   │
│ - Cloud: Check S3 permissions, IAM roles qua Checkov / Prowler        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. High-Priority Threat Categories (OWASP Top 10 & CWE)

1. **A01: Broken Access Control (CWE-284/CWE-862)**: IDOR, thiếu auth middleware, path traversal (`../`).
2. **A02: Cryptographic Failures (CWE-327/CWE-798)**: Hardcoded secrets, JWT `alg:none`, MD5/SHA1 cho mật khẩu.
3. **A03: Injection (CWE-89/CWE-78/CWE-94)**: SQL concatenation, OS command injection (`subprocess shell=True`), `eval()`, template injection.
4. **A04: Insecure Design & Rate Limiting**: Thiếu rate limit cho login/OTP, không kiểm tra captcha.
5. **A05: Security Misconfiguration (CWE-16)**: Debug mode bật ở production, CORS `*` với credentials, thiếu security headers (`HSTS`, `CSP`).
6. **A06: Vulnerable and Outdated Components (CWE-1104)**: Dependencies chứa CVE Critical/High trong NVD.
7. **A07: Identification & Auth Failures (CWE-384/CWE-613)**: Session fixation, token không hết hạn, weak password policy.
8. **A08: Software & Data Integrity Failures (CWE-502)**: Insecure deserialization (`pickle.loads`, `yaml.unsafe_load`).
9. **A09: Security Logging & Monitoring Failures (CWE-532)**: Ghi log chứa mật khẩu, token, hoặc không ghi nhận auth failure.
10. **A10: Server-Side Request Forgery (SSRF - CWE-918)**: Đọc URL do người dùng truyền vào mà không whitelist host.

---

## 4. Vòng Lặp Phản Hồi Bảo Mật (Remediation Feedback Loop)

```
Phát hiện Lỗ hổng (Critical / High)
               │
               ▼
┌────────────────────────────────────────┐
│ 1. Ghi nhận vào docs/security/report   │
│ 2. Ghi nhận vào docs/debug/root-causes │
└──────────────┬─────────────────────────┘
               │
               ▼
┌────────────────────────────────────────┐
│ 3. Viết Security Remediation Spec      │
│ 4. Quay lại Phase 1 (devcycle-spec)    │
└──────────────┬─────────────────────────┘
               │
               ▼
┌────────────────────────────────────────┐
│ 5. TDD Red-Green-Refactor (Phase 3)    │
│    (Viết test tái hiện lỗ hổng trước)  │
└──────────────┬─────────────────────────┘
               │
               ▼
┌────────────────────────────────────────┐
│ 6. Quét Pentest lại (Phase 6.5)        │
└──────────────┬─────────────────────────┘
               │
   0 Vulnerabilities? ──► [ 🟢 Bàn giao Phase 7 ]
```

- **Khi còn lỗ hổng**: Tuyệt đối không vá nóng tùy tiện. Phải đưa về Phase 1 để tạo Spec ➔ TDD Regression Test ➔ Fix.
- **Khi đạt 0 Vulnerabilities**: Xuất báo cáo theo mẫu [REPORT-FORMAT.md](./REPORT-FORMAT.md) và kết thúc đánh giá.

---

## 5. Liên Kết Với Các Kỹ Năng Liên Quan (Skill Ecosystem Integration)

- [redteam-security](../redteam-security/SKILL.md): Bản quy chuẩn an ninh và kiểm thử xâm nhập chuyên sâu theo chuẩn Borghei Red-Team trong Master Pipeline.
- [senior-dev-pipeline](../senior-dev-pipeline/SKILL.md): Cổng kiểm soát bảo mật bắt buộc (Phase 4 / 6.5) bảo đảm không bàn giao sản phẩm còn lỗ hổng.
- [devcycle-spec](../devcycle-spec/SKILL.md): Điểm hồi chuyển (Loopback) để soạn thảo *Security Remediation Spec* khi phát hiện lỗ hổng mức Critical / High.
- [devcycle-tdd](../devcycle-tdd/SKILL.md): Lập trình TDD sửa lỗi bảo mật — bắt buộc có test case tái hiện lỗ hổng (FAIL) trước khi vá code (GREEN).
- [devcycle-audit](../devcycle-audit/SKILL.md): Cung cấp dữ liệu kiểm toán an ninh để tích hợp vào báo cáo nghiệm thu và phân tích giới hạn kỹ thuật.
