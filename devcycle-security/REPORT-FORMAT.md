# Security Report Format & Severity Rubric (DevCycle Phase 6.5)

Bản tài liệu quy chuẩn kết quả đánh giá an ninh mạng: `docs/security/<YYYY-MM-DD>-report.md`.
Được thiết kế để lãnh đạo có thể nắm bắt bức tranh toàn cảnh, kỹ sư phát triển có thể sửa chữa ngay lập tức với đầy đủ bằng chứng thực tế và mã khai thác PoC.

---

## 1. Tiêu Chuẩn Phân Loại Mức Độ Nghiêm Trọng (Severity Rubric)

Dựa trên tác động thực tế tới tính Bảo mật (Confidentiality), Toàn vẹn (Integrity), Sẵn sàng (Availability) và tính khả thi trong môi trường thực:

| Mức độ | Ý nghĩa kỹ thuật | Ví dụ thực tế |
|---|---|---|
| **Critical** | RCE, chiếm quyền kiểm soát toàn bộ server/client, bypass hoàn toàn xác thực không cần điều kiện tiên quyết | RCE qua deserialization `pickle.loads`; hardcoded private key/token admin trong binary/code; SQLi đọc toàn bộ dữ liệu |
| **High** | Chiếm quyền nghiêm trọng hoặc đọc/sửa dữ liệu người dùng khác, có đường dẫn khai thác rõ ràng | SQLi có filter nhẹ; IDOR sửa đổi dữ liệu user khác; tắt xác thực TLS trên kết nối nhạy cảm; path traversal đọc file server |
| **Medium** | Rủi ro có thật nhưng bị giới hạn phạm vi hoặc đòi hỏi điều kiện tiên quyết khó xảy ra | Path traversal bị chặn trong thư mục sandbox; thuật toán băm yếu cho dữ liệu không phải mật khẩu; lộ token trong log cục bộ |
| **Low** | Vấn đề nhỏ, vi phạm nguyên tắc phòng thủ theo chiều sâu (Defense-in-Depth) | Tên file tạm dễ đoán; hiển thị thông báo lỗi chi tiết ra UI dialog; thiếu security header phụ |
| **Info** | Khuyến nghị tối ưu hóa kiến trúc an toàn | Cập nhật phiên bản thư viện chưa có CVE exploit; bổ sung CSP header nghiêm ngặt hơn |

### Mức độ Tin cậy (Confidence Level):
- **Confirmed**: Đã có mã khai thác PoC tối thiểu chạy thành công trên môi trường dev nội bộ, hoặc bằng chứng phân tích mã nguồn rõ ràng 100%.
- **Suspected**: Mẫu code hoặc log có dấu hiệu rủi ro cao nhưng cần thêm điều kiện môi trường để kích hoạt hoàn toàn.

---

## 2. Mẫu Báo Cáo Chuẩn (Security Review Report Template)

```markdown
# Báo Cáo Đánh Giá An Ninh — <Tên Dự Án> — <YYYY-MM-DD>

**Đơn vị đánh giá:** DevCycle Red-Team Security Assessment (Phase 6.5)
**Phạm vi (Scope):** <Đường dẫn hoặc toàn bộ repository> · **Commit:** <git hash>
**Môi trường:** White-box source review + Local dynamic verification

---

## I. Tóm Tắt Dành Cho Lãnh Đạo (Executive Summary)

<3-5 câu tóm lược tình trạng an ninh tổng thể, lỗ hổng nguy hiểm nhất được phát hiện và hành động ưu tiên cần khắc phục ngay.>

### Bảng Thống Kê Lỗ Hổng
| Mức độ (Severity) | Số lượng | Trạng thái (Open / Resolved / Risk-Accepted) |
|---|---|---|
| 🔴 **Critical** | 0 | 0 Open |
| 🟠 **High** | 0 | 0 Open |
| 🟡 **Medium** | 0 | 0 Open |
| 🔵 **Low** | 0 | 0 Open |
| ⚪ **Info** | 0 | 0 Open |

---

## II. Phương Pháp & Công Cụ Kiểm Thử (Methodology & Tooling)

### Danh Mục Công Cụ Đã Kích Hoạt (Auto-Setup & Execution):
- [x] **SAST (Static Analysis):** `secscan.py` (v1.0), `semgrep` (vX.X), `bandit` (vX.X)
- [x] **Secret Scanning:** `gitleaks` (vX.X) / `detect-secrets`
- [x] **Dependency & Supply Chain (SCA):** `pip-audit` / `npm audit` / `trivy`
- [x] **API & DAST Fuzzing:** `schemathesis` / `nuclei` / `jwt_tool`
- [x] **Container / IaC:** `hadolint` / `checkov`
- [x] **Desktop / Mobile / Network:** `strings`, `nmap`

---

## III. Danh Sách Lỗ Hổng Chi Tiết (Detailed Findings)

### SEC-001: <Tiêu Đề Ngắn Gọn Lỗ Hổng>
- **Mức độ:** `CRITICAL` / `HIGH` / `MEDIUM` / `LOW`
- **Mức độ tin cậy:** `Confirmed` (PoC verified)
- **Mã định danh:** `CWE-XXX` · `OWASP A0X:2021` · `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H (9.8)`
- **Vị trí phát hiện:** `src/api/auth.py:84` (Sink) ➔ Nguồn kích hoạt từ `src/api/routes.py:32` (Source)

#### 1. Mô tả chi tiết:
<Giải thích rõ nguyên nhân kỹ thuật gây ra lỗ hổng, tại sao dữ liệu người dùng không an toàn đi vào điểm sink.>

#### 2. Tác động thực tế (Impact):
<Kẻ tấn công có thể làm gì? Đánh cắp cơ sở dữ liệu, thực thi mã từ xa, mạo danh tài khoản quản trị hay làm sập dịch vụ?>

#### 3. Kịch bản & Bằng chứng Khai thác (Proof of Concept - PoC):
```bash
# Lệnh hoặc mã Python tái hiện lỗi an toàn trên môi trường dev:
curl -X POST http://127.0.0.1:8000/api/v1/auth/reset \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com'\'' OR '\''1'\''='\''1"}'
```

#### 4. Giải pháp khắc phục (Remediation):
```diff
- cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
+ cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
```

#### 5. Tài liệu tham khảo:
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)

---

## IV. Kế Hoạch Khắc Phục Ưu Tiên (Remediation Action Plan)

| Thứ tự | Mã Lỗ Hổng | Hành động cụ thể | Giai đoạn phụ trách | Trách nhiệm |
|---|---|---|---|---|
| 1 | **SEC-001** | Tạo Security Remediation Spec & TDD Regression Test | Phase 1 (`devcycle-spec`) | Backend Lead |
| 2 | **SEC-002** | Cập nhật phiên bản thư viện an toàn | Phase 3 (`devcycle-tdd`) | DevOps |

---

## V. Vòng Lặp Phản Hồi Bảo Mật (Closing the Feedback Loop)

Mọi phát hiện mức **Critical / High** bắt buộc phải:
1. Ghi nhận nguyên nhân gốc rễ vào `docs/debug/root-causes.md`.
2. Tạo issue và regression test trong `devcycle-tdd` (Test phải FAIL khi chưa sửa và PASS sau khi sửa).
3. Tái kiểm thử lại toàn bộ công cụ bảo mật trước khi bàn giao sang Phase 7 (Final Report).
```
