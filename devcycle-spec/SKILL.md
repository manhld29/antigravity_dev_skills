---
name: devcycle-spec
description: "Turn raw requirements or feature ideas into a crystal-clear, testable Product Requirements Document (PRD) with anti-hallucination validation, schema definitions, and explicit acceptance criteria. Grounded in the codebase via Graft & Graphify. Stage 1 of the devcycle pipeline. Also handles Security Remediation Specs when looped back from Phase 6.5. Triggers: \"spec this\", \"write a PRD\", \"devcycle-spec\", \"tạo spec\", \"lập tài liệu yêu cầu\"."
argument-hint: "What's the idea or feature requirement?"
---

# Devcycle — Spec (Idea / Requirement → Testable PRD)

Stage 1 of [devcycle](../devcycle/SKILL.md). Converts raw user ideas or security remediation
demands into a formal, anti-hallucination **Product Requirements Document (PRD)**.

## Core Principles
1. **Zero Hallucination**: Every module name, API path, database model, or UI component mentioned must be grounded in the active codebase via `devcycle-index` (`graft map`, `graft skeleton`, `graphify query`).
2. **Measurable Acceptance Criteria**: Every criterion must be a verifiable assertion that maps directly to a unit test or E2E test case.
3. **Security by Design**: Explicitly define input validation, authentication/authorization boundaries, and data sanitization upfront.

---

## Process

### 1. Capture Intent & Context Grounding
- Extract verbatim:
  - **User Goal**: What problem does this solve and what outcome is expected?
  - **Codebase Grounding**: Query the index to discover existing patterns:
    ```bash
    graphify query "<feature topic>"
    graft map
    graft skeleton path/to/relevant_file
    ```

### 2. Auto-Inference & Decision Resolution (Auto Mode)
- In autonomous/auto mode, reason out technical decisions based on existing conventions:
  - Architecture alignment (follow existing service, controller, repository, or component patterns).
  - Safety default: Validate inputs strictly, fail closed, enforce principle of least privilege.
  - Log all inferences in `## Assumptions (auto mode)`.

### 3. Generate PRD Document (`docs/prd/<feature-slug>.md`)

```markdown
# PRD: [Feature Name]

## 1. Overview & Purpose
- **Problem Statement**: What problem is being solved?
- **Desired Outcome**: What changes once this ships?
- **Target Audience**: Who uses or interacts with this?

## 2. Scope
- **In Scope**: Exact capabilities included in this iteration.
- **Out of Scope**: Explicit boundaries deferred to future work.

## 3. Architecture & Tech Stack
- **Affected Services / Components**: (Traced via Graft/Graphify)
- **Data Model & Schemas**: (Entities, DTOs, migrations, sanitization rules)
- **API Contracts**: (Endpoints, request/response payloads, status codes, auth rules)
- **UI / UX Flow**: (Screens, interactions, states, micro-animations if applicable)

## 4. Testable Acceptance Criteria (AC)
- [ ] **AC-1**: Given [context], when [action], then [expected result]. *(Test mapping: unit/e2e)*
- [ ] **AC-2**: Given [invalid input], when [action], then [error handled securely].
- [ ] **AC-3**: Given [auth boundary], when [unauthorized], then [reject with 401/403].

## 5. Security & Non-Functional Requirements
- **Sanitization & Validation**: (Zod, class-validator, pydantic, OWASP rules)
- **Rate Limiting & Abuse Prevention**:
- **Performance Budget**: (latency, payload size)

## 6. Assumptions & Inferences (Auto Mode)
- [List any inferred defaults or decisions with rationale]
```

### 4. Verification & Hand-off to Phase 2
- Validate that every Acceptance Criterion is unambiguous and testable.
- Handoff the PRD path to `devcycle-issues` (`Phase 2`).

---

## 5. Liên Kết Với Các Kỹ Năng Liên Quan (Skill Ecosystem Integration)

- [spec-engineering](../spec-engineering/SKILL.md): Kỹ nghệ đặc tả phần mềm & vòng lặp kiểm chứng zero-hallucination (Phase 1 & 2 Master Pipeline).
- [jira-fetch](../jira-fetch/SKILL.md): Trích xuất yêu cầu, acceptance criteria và file đính kèm trực tiếp từ Jira ticket vào PRD.
- [brandkit](../brandkit/SKILL.md): Định hình hệ thống thương hiệu, design tokens, color palette và phong cách thẩm mỹ trong tài liệu đặc tả.
- [devcycle-index](../devcycle-index/SKILL.md): Neo chặt các thực thể, API routes và models vào codebase thực tế qua Graft & Graphify.
- [devcycle-issues](../devcycle-issues/SKILL.md): Tiếp nhận PRD hoàn thiện để phân rã thành các issue tracer-bullet kèm blast radius.
- [output-skill](../output-skill/SKILL.md): Đảm bảo văn bản PRD, schema đặc tả và tiêu chí nghiệm thu được xuất đầy đủ 100% không bị cắt cụt.
