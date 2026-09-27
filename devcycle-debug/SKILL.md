---
name: devcycle-debug
description: "Disciplined, evidence-first debugging and root-cause diagnosis loop across Web, Backend API, and Desktop applications. Reads runtime logs, server outputs, stack traces, and environment state as primary evidence before touching code. Stage 4 / sub-loop of the devcycle pipeline. Triggers: \"debug this\", \"diagnose\", \"it's broken\", \"investigate failure\", \"devcycle-debug\", \"tìm lỗi\"."
argument-hint: "What's failing or throwing an error?"
---

# Devcycle — Debug (Failure → Evidence → Root Cause Isolation)

Sub-loop of [devcycle](../devcycle/SKILL.md). A rigorous, reproduce-first diagnosis discipline.
**Rule #1**: Never guess a fix without proving the root cause using log evidence.

---

## The 7-Step Evidence-First Loop

```
 1. REPRODUCE   — Establish a deterministic reproduction script or test case.
 2. READ LOGS   — Pull runtime logs, stack traces, HTTP status codes, and server output.
 3. MINIMIZE    — Shrink to the smallest input or payload that still triggers the failure.
 4. HYPOTHESIZE — Formulate ONE falsifiable hypothesis based on concrete evidence.
 5. PROVE       — Inspect code via Graft (graft callers / skeleton) or instrument with logging.
 6. CONFIRM     — Pinpoint the exact line and condition creating the bug.
 7. HAND-OFF    — Pass confirmed root cause to devcycle-bugfix for TDD resolution.
```

---

## Log & Evidence Sources
- **Web / Fullstack**: Dev server console, browser network tab (HTTP response payloads, SSE stream errors, CORS headers).
- **Backend / API**: NestJS / Express / FastAPI runtime logs (`APP_LOG_PATH`, stderr), database queries, Redis/Queue logs.
- **Desktop / CLI**: App log file, system events, STDERR.

---

## Anti-Patterns to Avoid
1. ❌ Changing code randomly hoping it fixes the symptom.
2. ❌ Fixing the downstream cascade exception instead of the original source failure.
3. ❌ Suppressing exceptions with bare `catch (e) {}` or `except: pass`.

---

## Liên Kết Với Các Kỹ Năng Liên Quan (Skill Ecosystem Integration)

- [jira-fetch](../jira-fetch/SKILL.md): Trích xuất báo cáo bug, stack trace và log đính kèm trực tiếp từ Jira ticket làm bằng chứng sơ cấp.
- [devcycle-bugfix](../devcycle-bugfix/SKILL.md): Bàn giao nguyên nhân gốc rễ đã xác minh sang quy trình TDD Bug-Fix 7 bước.
- [jira-bugfix](../jira-bugfix/SKILL.md): Vòng lặp sửa lỗi tổng thể điều phối từ Jira ticket qua các giai đoạn E2E ➔ Debug ➔ TDD Fix.
- [devcycle-index](../devcycle-index/SKILL.md): Sử dụng `graft callers` và `graphify path` để truy vết đường truyền của trạng thái lỗi qua các module.
