---
name: devcycle-issues
description: "Break a PRD into vertical-slice, tracer-bullet issues with explicit test strategies and blast radius estimation (via Graft callers & blast). Stage 2 of the devcycle pipeline. Use when you have a PRD and need actionable, independently shippable implementation tasks. Triggers: \"break into issues\", \"create issues from PRD\", \"devcycle-issues\", \"phân rã task\"."
argument-hint: "Path to the PRD (e.g. docs/prd/feature.md)"
---

# Devcycle — Issues (PRD → Vertical-Slice Tracer-Bullet Issues)

Stage 2 of [devcycle](../devcycle/SKILL.md). Decomposes a PRD into **independently shippable,
tracer-bullet vertical slices**. Each slice cuts across all necessary layers (Data → Logic → API/UI)
and includes an explicit **Test Strategy** and **Blast Radius Assessment**.

---

## 1. Tracer-Bullet Vertical Slices

Each issue must:
1. **Span end-to-end**: Not horizontal layering (e.g., avoid "Issue 1: build DB, Issue 2: build UI"). Instead: "Issue 1: Tracer bullet for minimal viable user flow end-to-end".
2. **Be independently testable**: Must have named unit tests and integration/E2E test criteria.
3. **Carry Blast Radius Analysis**: Use Graft to compute who depends on the symbols touched.

---

## 2. Blast Radius Calculation (Powered by Graft)

Before locking down an issue's scope, query Graft to discover potential impact:
```bash
# Check who calls or depends on the target symbol
graft callers TargetSymbolName -d 2

# Inspect the API skeleton of target files
graft skeleton path/to/target_file.ts
```

If the touched symbol is a high-degree hub (e.g. `AuthService`, `JwtAuthGuard`), note its dependents so regression tests guard all callers.

---

## 3. Issue Template (`docs/issues/<feature-slug>/issue-<N>.md`)

```markdown
# Issue [N]: [Slice Title]

## Goal
Short description of what capability this slice adds.

## Acceptance Criteria Covered
- Traces back to **AC-X** and **AC-Y** in the PRD.

## Blast Radius & Dependencies
- **Target Files/Symbols**: `src/...`, `components/...`
- **Dependents (via graft callers)**: [List of callers identified]
- **Risk Level**: Low / Medium / High

## Implementation Plan
1. Data / DTO / Schema updates
2. Core Business Logic (domain service)
3. Interface / Controller / View wiring

## Test Strategy (MANDATORY)
- **Unit Test File**: `tests/.../my-test.spec.ts` (test specific ACs)
- **Integration / E2E Case**: `tests/e2e/...`
- **Lint & SOLID Check**: Must pass clean code quality gate in Phase 3.
```

---

## 4. Ordering & Hand-off to Phase 3
- Slices are ordered sequentially by dependency (Tracer bullet first, followed by edge cases and secondary flows).
- Hand off `issue-1.md` to `devcycle-tdd` (`Phase 3`).

---

## 5. Liên Kết Với Các Kỹ Năng Liên Quan (Skill Ecosystem Integration)

- [devcycle-spec](../devcycle-spec/SKILL.md): Nguồn PRD chứa danh sách Acceptance Criteria cần ánh xạ trực tiếp vào từng issue.
- [spec-engineering](../spec-engineering/SKILL.md): Kiểm chứng tính khả thi và loại bỏ mâu thuẫn phụ thuộc giữa các issue.
- [jira-fetch](../jira-fetch/SKILL.md) & [jira-bugfix](../jira-bugfix/SKILL.md): Phân rã trực tiếp các yêu cầu/bug từ Jira ticket thành các slice có thể ship độc lập.
- [devcycle-index](../devcycle-index/SKILL.md): Đo lường Blast Radius chính xác qua `graft callers` và sơ đồ phụ thuộc AST.
- [devcycle-tdd](../devcycle-tdd/SKILL.md): Điểm đến trực tiếp của từng issue để thực thi lập trình Test-Driven Development.
- [output-skill](../output-skill/SKILL.md): Xuất trọn vẹn toàn bộ các issue slices mà không bỏ sót bất kỳ chi tiết kỹ thuật hay test strategy nào.
