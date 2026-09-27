---
name: devcycle-e2e
description: "Universal End-to-End (E2E) and Integration Testing skill supporting Web (Playwright/Cypress), Backend APIs (Supertest/Newman/curl), and Desktop applications (pywinauto/pytest-qt). CSV-driven or spec-driven test execution with persistent reporting, error screenshot capture, and masked credential protection. Stage 4 of the devcycle pipeline. Triggers: \"run e2e\", \"generate e2e tests\", \"integration test\", \"devcycle-e2e\", \"kiểm thử E2E\"."
argument-hint: "Which user journey or API flow should the E2E cover?"
---

# Devcycle — E2E & Integration Testing (Universal & CSV-Driven)

Stage 4 of [devcycle](../devcycle/SKILL.md). Validates the entire user journey against
the live system environment. Runs in 3 structured phases:

```
 1. GENERATE CASES → Build test matrix in tests/e2e/cases.csv from PRD Acceptance Criteria.
 2. GENERATE CODE  → Read source selectors/routes via Graft, write step-by-step E2E tests.
 3. RUN & RECORD   → Execute tests in an isolated sandbox, record PASS/FAIL in cases.csv.
```

---

## 1. Stack-Specific Testing Engines

| Project Type | Preferred E2E Tooling | Artifacts Captured |
|---|---|---|
| **Web / Fullstack** | Playwright (`npx playwright test`), Cypress | Screenshots, Videos, Network HAR traces |
| **Backend / REST API** | Supertest, Vitest, Newman, pytest | Response bodies, Latency, Status codes |
| **Desktop GUI** | pywinauto, pytest-qt (Qt/QML/QSS) | Window screenshots (`tests/e2e/_artifacts/`) |
| **CLI Tools** | Python subprocess, Bash assertions | STDOUT / STDERR captures |

---

## 2. CSV-Driven Reporting (`tests/e2e/cases.csv`)

The CSV format maintains an audit-proof, persisted record of test runs:

| case_id | feature | scenario | route_steps | expected_result | status | screenshot_path |
|---|---|---|---|---|---|---|
| TC-01 | Auth | User logs in with valid credentials | /login -> fill form -> submit | Dashboard rendered with user profile | PASS | _artifacts/TC-01.png |
| TC-02 | Auth | User attempts login with wrong password | /login -> invalid pass -> submit | Error toast 'Invalid credentials' | PASS | _artifacts/TC-02.png |

---

## 3. Security & Isolation Rules
- **Environment**: Read credentials only from `.env.dev` or `.env.local` (never commit real secrets).
- **Masking**: Passwords and authorization tokens are automatically masked in logs and CSV outputs.
- **Sandbox**: Run with isolated temporary profiles/directories so runs leave no host state dirty.

---

## 4. Liên Kết Với Các Kỹ Năng Liên Quan (Skill Ecosystem Integration)

- [mobile-native](../mobile-native/SKILL.md): Kiểm thử E2E giao diện di động — viewport responsiveness, touch gestures, tap targets và mobile keyboard behavior.
- [ask-sonner](../ask-sonner/SKILL.md): Kiểm chứng các trạng thái phản hồi toast (loading, success, error) và khả năng tương tác của người dùng.
- [devcycle-debug](../devcycle-debug/SKILL.md): Tự động chuyển giao kết quả E2E thất bại kèm screenshots và HAR traces để chẩn đoán nguyên nhân gốc rễ.
- [jira-bugfix](../jira-bugfix/SKILL.md): Viết E2E regression / reproduction tests cho các lỗi được mô tả từ Jira ticket.
- [output-skill](../output-skill/SKILL.md): Đảm bảo các script Playwright/Cypress/Supertest và bảng `cases.csv` được sinh hoàn chỉnh 100%.
