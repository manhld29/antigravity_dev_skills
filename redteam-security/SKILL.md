---
name: redteam-security
description: "Phase 4 Security Skill based on Borghei Red-Team standards: security auditing, SAST (Semgrep, Bandit, gosec), DAST (OWASP ZAP, Nuclei, Nikto), API Fuzzing (Schemathesis, JWT Tool, ffuf), secret scanning (Gitleaks, TruffleHog), dependency & container check (Trivy, Grype, pip-audit, npm audit, Checkov), and desktop/mobile analysis (Ghidra, Frida, JADX). AI is authorized to auto-install missing security tools on demand. Flaws loop back to Phase 1 via docs/debug/root-causes.md."
---

# Red-Team Security & Pentesting Skill — Borghei Standards

Skill này chịu trách nhiệm cho **Giai đoạn 4 (Security Audit & Red Team Testing)** trong quy trình chuẩn 15 năm kinh nghiệm, đảm bảo phần mềm không chỉ hoạt động đúng mà còn miễn nhiễm trước các cuộc tấn công bảo mật.

---

## ⚡ 1. Tự Động Kiểm Tra & Cài Đặt Công Cụ Security (Tooling Auto-Setup Mandate)

> **QUY TẮC CỐT LÕI**: AI có toàn quyền và nghĩa vụ **tự động phát hiện và thực thi lệnh cài đặt bất kỳ công cụ nào cần thiết** (`pip install`, `npm install -g`, `go install`, `cargo install`, `curl/sh`...) khi công cụ đó chưa có sẵn trong môi trường máy chủ/máy trạm.

### Lệnh Auto-Install nhanh theo nhóm:
```bash
# 1. SAST & Static Code
which semgrep >/dev/null 2>&1 || pip install semgrep
which bandit >/dev/null 2>&1 || pip install bandit
which bearer >/dev/null 2>&1 || curl -sfL https://raw.githubusercontent.com/Bearer/bearer/main/contrib/install.sh | sh

# 2. Secrets & Leakage
which gitleaks >/dev/null 2>&1 || (curl -sSfL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks-linux-x64.tar.gz | tar -xz -C /usr/local/bin 2>/dev/null || pip install detect-secrets)
which trufflehog >/dev/null 2>&1 || curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /tmp

# 3. Dependencies, SBOM & Containers
which trivy >/dev/null 2>&1 || (curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /tmp 2>/dev/null || true)
which pip-audit >/dev/null 2>&1 || pip install pip-audit
which grype >/dev/null 2>&1 || curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /tmp
which syft >/dev/null 2>&1 || curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /tmp
which hadolint >/dev/null 2>&1 || (curl -sSfL https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64 -o /tmp/hadolint && chmod +x /tmp/hadolint)
which checkov >/dev/null 2>&1 || pip install checkov

# 4. API & Web DAST Fuzzing
which schemathesis >/dev/null 2>&1 || pip install schemathesis
which nuclei >/dev/null 2>&1 || (go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest 2>/dev/null || true)
which ffuf >/dev/null 2>&1 || (go install github.com/ffuf/ffuf/v2@latest 2>/dev/null || true)
which nikto >/dev/null 2>&1 || (sudo apt-get update && sudo apt-get install -y nikto 2>/dev/null || true)
which jwt_tool >/dev/null 2>&1 || pip install pyjwt cryptography requests

# 5. Network & Infrastructure
which nmap >/dev/null 2>&1 || (sudo apt-get update && sudo apt-get install -y nmap 2>/dev/null || true)
which prowler >/dev/null 2>&1 || pip install prowler
```

---

## 2. Danh Mục Công Cụ Kiểm Thử Bảo Mật Toàn Diện

1. **Web Application Security**: Burp Suite, OWASP ZAP, Nikto, Nuclei, Wapiti, w3af, ffuf, Gobuster, Feroxbuster.
2. **API Security**: Schemathesis, Dredd, Kiterunner, JWT Tool, ffuf, OWASP ZAP API scan, Postman/Newman.
3. **Network & Port Security**: Nmap, Masscan, RustScan, Wireshark/tshark, tcpdump, Netcat, OpenVAS.
4. **Source Code / SAST**: Semgrep, Bandit, gosec, Brakeman, SpotBugs/FindSecBugs, ESLint Security, PHPStan/Psalm, Bearer, secscan.py.
5. **Dependency & Supply Chain (SCA & SBOM)**: Trivy, Grype, Syft, pip-audit, npm audit, cargo audit, govulncheck, OWASP Dependency-Check.
6. **Container & IaC Security**: Trivy, Grype, Docker Scout, Hadolint, Checkov, Terrascan, Kube-bench, Kube-hunter.
7. **Authentication & Credential Testing**: JWT Tool, Hydra, Medusa, Hashcat, John the Ripper, CrackMapExec/NetExec.
8. **Mobile Application (Android/iOS)**: MobSF, Frida, Objection, JADX, apktool, Ghidra, adb, mitmproxy.
9. **Desktop Application (PySide6/Qt/C++/Electron)**: Ghidra, IDA Free, x64dbg, Process Monitor, Process Explorer, Wireshark, Frida, strings, Detect It Easy, YARA (Kiểm tra QSettings, local TCP 9000, URI protocol schemes, DLL hijack).
10. **Secrets & Leakage**: Gitleaks, TruffleHog, GitGuardian, detect-secrets.
11. **Cloud Security**: Prowler, ScoutSuite, CloudSploit, Trivy, Checkov, Pacu.

---

## 3. Quy Trình 4 Bước Red-Team Penetration Testing

### Bước 1: Quét Mã Nguồn Tĩnh & Bí Mật (SAST & Secret Scanning)
- Tự động chạy Gitleaks / detect-secrets quét toàn bộ repo và git log.
- Chạy Semgrep / Bandit / gosec / secscan.py phát hiện: SQLi (CWE-89), Command Injection (CWE-78), Code Injection `eval` (CWE-94), Deserialization (CWE-502), Path Traversal (CWE-22).

### Bước 2: Kiểm Tra Thư Viện & Chuỗi Cung Ứng (SCA & Containers)
- Tự động chạy `pip-audit`, `npm audit`, `cargo audit`, `govulncheck`, hoặc `trivy fs .`.
- Quét Dockerfile bằng `hadolint` và IaC bằng `checkov`.

### Bước 3: Phân Tích Lỗ Hổng OWASP Top 10 & API Fuzzing (DAST)
- Chạy Schemathesis fuzzing API từ OpenAPI/Swagger specification.
- Quét DAST endpoint cục bộ với Nuclei / ZAP / Nikto.
- Kiểm tra tính bảo mật của JWT tokens bằng `jwt_tool`.
- Đánh giá OWASP Top 10: Broken Access Control (IDOR), Insecure Design, Security Misconfiguration (CORS, CSP, TLS).

### Bước 4: Đánh Giá Kết Quả & Vòng Lặp Phản Hồi Về Spec (Security Feedback Loop)
- **NẾU PHÁT HIỆN LỖ HỔNG (Critical / High)**:
  1. Lập báo cáo chi tiết vào `docs/security/<date>-report.md` và `docs/debug/root-causes.md`.
  2. **TUYỆT ĐỐI KHÔNG ĐƯỢC VÁ SỬA TÙY TIỆN**.
  3. **CHUYỂN GIAO VỀ GIAI ĐOẠN 1 (`spec-engineering`)**:
     - Cập nhật tài liệu Spec phát triển với phần *Security Remediation Spec*.
     - Verify Spec (Phase 2) ➔ TDD Fix Code (Phase 3 - viết test tái hiện trước) ➔ Red-Team Pentest lại (Phase 4).
- **NẾU ĐẠT 0 VULNERABILITIES**:
  - Xuất báo cáo chứng nhận an toàn Red-Team Borghei và hoàn thành nhiệm vụ.

---

## 4. Bản Nguyên Tắc An Toàn Khi Pentest
- "Chỉ thực hiện pentest và kiểm thử an ninh trong phạm vi dự án được cho phép."
- "Không để lại backdoor hoặc mã khai thác thử nghiệm trong sản phẩm cuối."
- "Báo cáo trung thực 100% kết quả từ log công cụ quét thực tế."
- "Mọi lỗ hổng tìm thấy đều phải qua quy trình Spec ➔ Verify ➔ TDD để sửa triệt để."
