---
name: devcycle-bugfix
description: "Disciplined 7-phase TDD bug-fix loop for any software project (reproduce → isolate root cause via devcycle-debug → write FAILING regression test → minimal fix → test pass → refactor → update root-cause convergence ledger). Sub-loop of devcycle Phases 3–4. Use when a known bug must be fixed test-first. Triggers: \"fix this bug\", \"sửa lỗi\", \"có bug\", \"regression\", \"devcycle-bugfix\"."
argument-hint: "Which bug are we fixing (symptom / failing case)?"
---

# Devcycle — Bug-fix (Reproduce → Failing Test → Minimal Fix → Regress)

Disciplined **TDD bug-fix sub-loop** of [devcycle](../devcycle/SKILL.md). Fixes a known bug
test-first across 7 explicit phases, ensuring the bug can never silently regress.

---

## The 7-Phase Bugfix Discipline

```
 ┌───────────────────────────┐
 │ 1. Reproduce              │ Minimal script or curl/payload reproducing the issue.
 ├───────────────────────────┤
 │ 2. Isolate Root Cause     │ Consult devcycle-debug: pinpoint exact source file:line.
 ├───────────────────────────┤
 │ 3. Write Regression Test  │ 🔴 RED: Add a unit/E2E test that FAILS on current code.
 ├───────────────────────────┤
 │ 4. Minimal Code Fix       │ 🟢 GREEN: Apply the smallest change fixing the root cause.
 ├───────────────────────────┤
 │ 5. Verify Tests Pass      │ Run test suite; confirm test is now GREEN.
 ├───────────────────────────┤
 │ 6. Refactor & Lint        │ 🔵 REFACTOR: Run lint.py and verify SOLID compliance.
 ├───────────────────────────┤
 │ 7. Record in Ledger       │ Log entry in docs/debug/root-causes.md (Convergence).
 └───────────────────────────┘
```

---

## The Convergence Ledger (`docs/debug/root-causes.md`)

Every confirmed bugfix must be documented in the repository ledger:

```markdown
### [BUG-YYYYMMDD-N] Title
- **Symptom**: User saw error X when doing Y.
- **Root Cause**: Missing validation in `service.ts:L45` allowing null payload.
- **Regression Test**: `tests/unit/service.spec.ts` (`should reject null payload`).
- **Fix**: Added guard clause and sanitized DTO.
- **Blast Radius**: Checked via `graft callers TargetFunction` (0 downstream impacts).
- **Status**: CLOSED
```

If the bug represents a requirement violation, add a corresponding Acceptance Criterion in `docs/prd/` so it remains part of the permanent specification.

---

## Liên Kết Với Các Kỹ Năng Liên Quan (Skill Ecosystem Integration)

- [jira-bugfix](../jira-bugfix/SKILL.md): Master workflow xử lý vòng đời bug toàn diện bắt đầu từ Jira ticket đến khi đóng ticket.
- [jira-fetch](../jira-fetch/SKILL.md): Tự động kéo mô tả chi tiết, crash logs và tài liệu đính kèm từ Jira REST API.
- [devcycle-debug](../devcycle-debug/SKILL.md): Xác minh bằng chứng thực tế và cô lập chính xác dòng code gây lỗi trước khi viết test.
- [tdd-development](../tdd-development/SKILL.md): Áp dụng chuẩn Matt Pocock để viết failing regression test bắt buộc trước khi chạm vào mã nguồn logic.
- [output-skill](../output-skill/SKILL.md): Đảm bảo mã sửa lỗi, test regression và cập nhật sổ cái `root-causes.md` được viết đầy đủ, không rút gọn.
