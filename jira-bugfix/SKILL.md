---
name: jira-bugfix
description: "Jira-driven, test-first bug-fix orchestrator for any software project. Runs 8 gated phases: Ingest Jira ticket Description & Attachments (jira-fetch) → Reproduce with E2E/Integration test (devcycle-e2e) → Isolate root cause from logs (devcycle-debug) → Write failing unit regression test + minimal fix (devcycle-bugfix) → Re-run E2E to verify → Review security (devcycle-security) → Audit limitations (devcycle-audit). Triggers: \"fix this Jira bug\", \"sửa bug theo ticket\", \"fix PROJ-123\", \"jira-bugfix\"."
argument-hint: "<bug symptom> + Jira key (e.g. \"auth error PROJ-123\")"
---

# Jira Bug-fix — Ticket → Reproduce → TDD Fix → Verify → Secure → Audit

> **Jira-driven orchestrator** over the devcycle skills. Invokes [jira-fetch](../jira-fetch/SKILL.md),
> [devcycle-e2e](../devcycle-e2e/SKILL.md), [devcycle-debug](../devcycle-debug/SKILL.md),
> [devcycle-bugfix](../devcycle-bugfix/SKILL.md), [devcycle-security](../devcycle-security/SKILL.md),
> and [devcycle-audit](../devcycle-audit/SKILL.md), passing artifacts between phases.

---

## 8-Phase Ticket-Driven Lifecycle

```
 ┌───────────────────────────────────┐
 │ 1. Ingest Ticket & Attachments   │ jira-fetch: description, screenshots, logs, stack traces.
 ├───────────────────────────────────┤
 │ 2. Reproduce with E2E Test       │ devcycle-e2e: failing end-to-end or integration test case.
 ├───────────────────────────────────┤
 │ 3. Isolate Proven Root Cause     │ devcycle-debug: pinpoint exact source file:line from logs.
 ├───────────────────────────────────┤
 │ 4. Write Regression Test         │ 🔴 RED: unit test fails on current code.
 ├───────────────────────────────────┤
 │ 5. Implement Minimal Fix         │ 🟢 GREEN: minimal code change, verify tests PASS.
 ├───────────────────────────────────┤
 │ 6. Re-run E2E Verification       │ devcycle-e2e: verify full user journey passes GREEN.
 ├───────────────────────────────────┤
 │ 7. Security Impact Review        │ devcycle-security: ensure fix introduced 0 vulnerabilities.
 ├───────────────────────────────────┤
 │ 8. Audit & Ledger Convergence    │ devcycle-audit: update docs/debug/root-causes.md.
 └───────────────────────────────────┘
```

---

## Core Mandate
1. **Never guess without reproduction**: Every bug must be proven with a failing test case before writing production code.
2. **Analyze attachments**: If the ticket has screenshots, HAR files, or server logs, download them via `jira-fetch` and inspect them as primary evidence.
3. **Guard against regressions**: The regression unit test must stay permanently in the test suite.
