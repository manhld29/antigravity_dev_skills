---
name: devcycle-refine
description: "Improve software architecture after a feature slice lands: decouple god-nodes, separate presentation from business logic, and reduce cognitive complexity under green tests. Stage 5 of the devcycle pipeline. Leverages Graphify god-nodes and Graft callers to pinpoint coupling. Triggers: \"refactor\", \"clean this up\", \"improve architecture\", \"devcycle-refine\", \"tinh chỉnh kiến trúc\"."
argument-hint: "Which module or area to refine?"
---

# Devcycle — Refine (Post-Slice Architectural Deepening & Decoupling)

Stage 5 of [devcycle](../devcycle/SKILL.md). Executes **under green tests** to prevent
architectural decay and pay down technical debt before it compounds.

---

## 1. Discovering Refactoring Targets (Powered by Graft & Graphify)

```bash
# 1. Identify high-coupling god-nodes
graphify god-nodes --top 10

# 2. Check dependents and blast radius
graft callers TargetClass -d 2

# 3. View structural API skeleton
graft skeleton path/to/target.ts
```

---

## 2. Key Refactoring Patterns

1. **Decouple Business Logic from UI / Frameworks**:
   - Web: Move state and business calculations from React/Vue components into standalone pure functions, custom hooks, or domain services.
   - Desktop: Move logic out of QWidgets into pure services.
2. **Deep Modules vs Shallow Interfaces**:
   - Strive for deep modules (rich capability behind a concise, minimal API surface).
3. **Eliminate Information Leakage**:
   - Centralize duplicate formatters, constants, and validation rules into a single authority.
4. **Enforce Dependency Inversion**:
   - Use interfaces/abstract contracts rather than tight concrete coupling.

---

## 3. The Golden Rule of Refactoring
- **Never change behavior during refinement**: All unit and E2E tests must remain GREEN before, during, and after refactoring. If behavior must change, that is a new feature requirement → re-enter Phase 1.

---

## 4. Liên Kết Với Các Kỹ Năng Liên Quan (Skill Ecosystem Integration)

- [devcycle-index](../devcycle-index/SKILL.md): Công cụ cốt lõi để phát hiện god-nodes (`graphify god-nodes`) và kiểm tra callers (`graft callers`) trước khi tách module.
- [tdd-development](../tdd-development/SKILL.md): Tiêu chuẩn thiết kế Clean Architecture, áp dụng SOLID principles dưới sự bảo vệ của test suite tự động.
- [senior-dev-pipeline](../senior-dev-pipeline/SKILL.md): Định hướng kiến trúc phần mềm chuẩn mực Senior 15 năm kinh nghiệm thực chiến.
- [impeccable-design](../impeccable-design/SKILL.md): Tinh chỉnh và tái cấu trúc các component giao diện người dùng, tách rời presentation khỏi state management.
