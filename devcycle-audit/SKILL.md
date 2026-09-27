---
name: devcycle-audit
description: "Audit completed features against original PRD Acceptance Criteria, generate an objective traceability matrix, verify test coverage, and document technical limitations and edge cases. Stage 6 of the devcycle pipeline. Triggers: \"audit this\", \"check limitations vs PRD\", \"gap analysis\", \"devcycle-audit\", \"kiểm toán yêu cầu\"."
argument-hint: "Path to the PRD to audit against"
---

# Devcycle — Audit (Requirements Traceability & Limitation Analysis)

Stage 6 of [devcycle](../devcycle/SKILL.md). Steps back to answer one fundamental question:
**Does the implemented feature actually satisfy what was originally specified in the PRD, and where are the real technical boundaries?**

---

## 1. Traceability Matrix (`docs/audit/<feature-slug>-audit.md`)

Maps every Acceptance Criterion (AC) in the original PRD to the exact test file proving it:

| Criterion ID | Requirement Summary | Verifying Test / Evidence | Status |
|---|---|---|---|
| **AC-1** | Valid user login produces JWT | `auth.service.spec.ts:L45` / `TC-01` | **MET** |
| **AC-2** | Reject password < 8 chars | `auth.dto.spec.ts:L12` / `TC-02` | **MET** |
| **AC-3** | Lockout after 5 failed attempts | Untested in unit suite | **UNMET** (Gap) |

Status categories: `MET`, `PARTIAL`, `UNMET`, `DEVIATED`.

---

## 2. Technical Limitations & Boundary Report

Document explicit limitations introduced or discovered:
- **Concurrency & Rate Limits**: Maximum concurrent requests, queue capacity.
- **Edge Cases**: Empty datasets, network timeout behavior, unicode handling.
- **Security & Data Retention**: Token expiration, cleanup cron schedules.
- **OS / Browser Scope**: Supported browser versions, screen resolutions.

---

## 3. Exit Condition
- If any critical AC is `UNMET` or `DEVIATED` without explicit approval: Log to `docs/debug/root-causes.md` and loop back to Phase 1.
- If clean: Advance to Phase 6.5 (`devcycle-security`).

---

## 4. Liên Kết Với Các Kỹ Năng Liên Quan (Skill Ecosystem Integration)

- [devcycle-spec](../devcycle-spec/SKILL.md): Đối chiếu trực tiếp với PRD gốc để xây dựng bảng Traceability Matrix cho từng Acceptance Criterion.
- [spec-engineering](../spec-engineering/SKILL.md): Đánh giá khoảng cách giữa spec và thực tế triển khai (Gap Analysis), kiểm chứng độ hoàn thiện của hệ thống.
- [senior-dev-pipeline](../senior-dev-pipeline/SKILL.md): Cổng kiểm soát chất lượng kỹ nghệ trước khi chuyển giao sang pentest bảo mật.
- [output-skill](../output-skill/SKILL.md): Xuất toàn vẹn ma trận kiểm toán, danh sách ranh giới kỹ thuật và edge cases không bị cắt ngắn.
- [devcycle-security](../devcycle-security/SKILL.md): Giai đoạn tiếp theo sau khi kiểm toán chức năng hoàn tất (Phase 6 ➔ Phase 6.5).
