---
name: devcycle
description: "Universal autonomous engineering orchestrator that synthesizes the entire devcycle pipeline across any programming language (TypeScript, JavaScript, Python, Go, Rust, Java, PHP, C, C++, Swift, Dart, Ruby, R, C#, Kotlin) and all their frameworks (Web, Fullstack, Backend API, Desktop, Mobile, Embedded, Data/AI, CLI). Drives every phase in order without stopping: Environment Bootstrap (Phase 0) → Dual-Engine Indexing via Graft & Graphify (Phase 0.5) → Anti-Hallucination PRD (Phase 1) → Vertical-Slice Issues with Blast Radius (Phase 2) → TDD Red-Green-Refactor + Strict Lint/SOLID Gates (Phase 3) → E2E/Integration Testing (Phase 4) → Architecture Refinement (Phase 5) → Limitation Audit (Phase 6) → Mandatory Borghei Red-Team Security Review (Phase 6.5) → Final Report (Phase 7). Root causes, E2E failures, and security findings automatically loop back to Phase 1 via docs/debug/root-causes.md ledger. Triggers: \"run the full cycle\", \"ship this feature end to end\", \"devcycle\", \"tự động\", or any feature request."
argument-hint: "What feature or change do you want to ship end to end?"
---

# Devcycle — Universal Software Engineering Lifecycle (Master Orchestrator)

> Canonical end-to-end autonomous engineering workflow for **any software project**
> across **any programming language** (TypeScript, JavaScript, Python, Go, Rust, Java, PHP, C, C++, Swift, Dart, Ruby, R, C#, Kotlin)
> and **all frameworks** (Web, Fullstack, Backend API, Desktop, Mobile, Embedded, Data/AI, CLI).
> 
> This skill is the **Master Driver**: it runs the `devcycle-*` stage skills in sequence,
> passes artifacts between stages, enforces non-negotiable quality & security gates,
> and manages the root-cause convergence loop.

```
[User Request / Feature Idea]
         │
         ▼
 ┌────────────────────────┐  Phase 0: Environment & Tooling Auto-Bootstrap
 │ 0. Tooling Bootstrap   │  (Any Language: TS/JS, Py, Go, Rust, Java, Kotlin,
 └──────────┬─────────────┘   PHP, C/C++, C#, Swift, Dart, Ruby, R + all frameworks)
            ▼
 ┌────────────────────────┐ ◄─────────────────────────────────────────────────┐
 │ 0.5 Dual-Engine Index  │  Graft (@nanonets/graft) + Graphify (graphifyy)    │
 └──────────┬─────────────┘                                                   │
            ▼                                                                 │
 ┌────────────────────────┐  Phase 1: Anti-Hallucination Spec & PRD           │
 │ 1. Spec Generation     │  (Acceptance Criteria, Data & API Contracts)      │
 └──────────┬─────────────┘                                                   │
            ▼                                                                 │
 ┌────────────────────────┐  Phase 2: Vertical-Slice Tracer-Bullet Issues     │
 │ 2. Issues Breakdown    │  (Blast Radius analysis via graft callers / blast)│
 └──────────┬─────────────┘                                                   │
            ▼                                                                 │
 ┌────────────────────────┐  Phase 3: TDD Loop (Matt Pocock Standards)        │
 │ 3. TDD + Code Quality  │  (🔴 Red → 🟢 Green → 🔵 Refactor + Lint + SOLID)  │
 └──────────┬─────────────┘  (Includes devcycle-ui for UI slices)             │
            ▼                                                                 │
 ┌────────────────────────┐  Phase 4: E2E & Integration Verification          │
 │ 4. E2E / Integration   │  (Playwright, Cypress, Supertest, pywinauto, etc) │
 └──────────┬─────────────┘                                                   │
            ▼                                                                 │
 ┌────────────────────────┐  Phase 5: Architecture Refine                     │
 │ 5. Architecture Refine │  (Decouple god-nodes, domain isolation)           │
 └──────────┬─────────────┘                                                   │
            ▼                                                                 │
 ┌────────────────────────┐  Phase 6: Limitation & Traceability Audit         │
 │ 6. Requirement Audit   │  (PRD vs reality gap analysis)                    │
 └──────────┬─────────────┘                                                   │
            ▼                                                                 │
 ┌────────────────────────┐  Phase 6.5: Borghei Red-Team Security Review     │
 │ 6.5 Security Pentest   │  (SAST secscan.py, DAST, OWASP, CWE, PoC)         │
 └──────────┬─────────────┘                                                   │
            │                                                                 │
            ├─► CRITICAL / HIGH FINDINGS OR FAILING TESTS ────────────────────┘
            │   (Log to docs/debug/root-causes.md → Re-enter Phase 1)
            │
            ▼ (When tests PASS + 0 Security Vulnerabilities + Ledger DRY)
 ┌────────────────────────┐  Phase 7: Final Completion & Sign-off
 │ 7. Final Report        │
 └────────────────────────┘
```

---

## 1. Non-Negotiable Hard Gates

1. **Anti-Hallucination Rule (Zero Guessing)**:
   - Ground all architectural choices, types, schemas, and symbol names in real codebase data via `devcycle-index` (`graft map`, `graft skeleton`, `graphify query`).
2. **Environment & Runtime Isolation (Phase 0)**:
   - Always run inside dedicated project environments and package managers:
     - **TypeScript / JavaScript**: `node_modules` (npm, pnpm, yarn, bun)
     - **Python**: `.venv`, poetry, uv, pipenv
     - **Go**: `go.mod` / vendor
     - **Rust**: `Cargo.toml` / target
     - **Java / Kotlin**: Gradle (`build.gradle`, `build.gradle.kts`), Maven (`pom.xml`)
     - **PHP**: Composer (`composer.json`, `vendor/`)
     - **C / C++**: CMake (`CMakeLists.txt`), Makefile, Meson, Conan, vcpkg
     - **C# / .NET**: `.sln`, `.csproj`, dotnet CLI, NuGet
     - **Swift**: SwiftPM (`Package.swift`), Xcode project
     - **Dart**: Pub (`pubspec.yaml`), Flutter CLI
     - **Ruby**: Bundler (`Gemfile`, `Gemfile.lock`)
     - **R**: `renv`, packrat, devtools
3. **Query-First Mandate (Phase 0.5)**:
   - Never grep blindly. Query `graft callers <symbol>` or `graphify query` before modifying code.
4. **Strict TDD & Code-Quality Gate (Phase 3)**:
   - Tests written first (confirm RED failure). Code is not GREEN until tests pass AND project linters/style checks are 100% clean.
5. **Mandatory Security Pentest (Phase 6.5)**:
   - Every feature undergoes a white-box security review (multi-language `secscan.py`, tainted source-to-sink flow, CWE/OWASP triage, local PoC).
6. **Convergence Ledger**:
   - Every root cause or security flaw is recorded in `docs/debug/root-causes.md` and fed back to Phase 1. Phase 7 is reached only when the ledger is empty.

---

## 2. Universal Matrix: All Languages & Frameworks Supported

Devcycle supports **any programming language** and **all frameworks** across the entire lifecycle:

| Language | Ecosystem & Package Managers | Key Supported Frameworks | Test Runner(s) | Linter / Style Gate |
|---|---|---|---|---|
| **TypeScript / JavaScript** | npm, pnpm, yarn, bun, deno | Next.js, React, Vue, Nuxt, Svelte, Angular, Express, NestJS, Fastify, Astro, Electron, React Native | Vitest, Jest, Mocha, Playwright | ESLint, Biome, Prettier, `tsc` |
| **Python** | pip, venv, poetry, uv, pipenv | FastAPI, Django, Flask, PySide6/PyQt, PyTorch, Celery, Streamlit, Starlette | Pytest, Unittest | Ruff, Black, Flake8, Mypy, isort |
| **Go** | go modules (`go.mod`) | Gin, Echo, Fiber, Chi, Cobra, Ent, Gorm, Buffalo, Beego | `go test ./...`, Testify | `golangci-lint`, `go vet`, `gofmt` |
| **Rust** | Cargo (`Cargo.toml`) | Actix-web, Axum, Rocket, Tokio, Tauri, Diesel, SeaORM, Leptos | `cargo test`, Nextest | `cargo clippy`, `cargo fmt` |
| **Java** | Maven (`pom.xml`), Gradle | Spring Boot, Quarkus, Micronaut, Vert.x, JavaFX, Dropwizard | JUnit 5, TestNG, Mockito, AssertJ | Checkstyle, Spotless, PMD, SpotBugs |
| **Kotlin** | Gradle (`build.gradle.kts`), Maven | Android Jetpack Compose, Ktor, Spring Boot, Multiplatform (KMP), Vert.x | JUnit 5, MockK, Kotest | Detekt, Ktlint, Spotless |
| **PHP** | Composer (`composer.json`) | Laravel, Symfony, Slim, WordPress, Yii, CodeIgniter, CakePHP | PHPUnit, Pest | PHP-CS-Fixer, PHPStan, Psalm |
| **C / C++** | CMake, Meson, Makefile, Conan, vcpkg | Qt, Boost, Drogon, POCO, Unreal Engine, ImGui, JUCE, Crow | GoogleTest, Catch2, CTest | `clang-tidy`, `clang-format`, `cppcheck` |
| **C# / .NET** | dotnet CLI, NuGet, MSBuild | ASP.NET Core, MAUI, WPF, WinForms, Blazor, Entity Framework, Unity | xUnit, NUnit, MSTest | Roslyn Analyzers, `dotnet format` |
| **Swift** | SwiftPM (`Package.swift`), Xcode | SwiftUI, UIKit, AppKit, Vapor, Kitura | XCTest, Swift Testing | SwiftLint, `swift-format` |
| **Dart** | Pub (`pubspec.yaml`), Flutter | Flutter (Mobile, Web, Desktop), Shelf, Dart Frog, Serverpod | `dart test`, `flutter test` | `dart analyze`, `flutter analyze` |
| **Ruby** | Bundler (`Gemfile`), gem | Ruby on Rails, Sinatra, Hanami, Sidekiq, Grape, Jekyll | RSpec, Minitest | RuboCop, StandardRB |
| **R** | renv, devtools, packrat | Shiny, Plumber, Tidyverse, Data.table, Bioconductor | `testthat` | `lintr`, `styler` |
| *Any Other Stack* | Dynamic autodetection | All associated web, API, desktop, mobile, CLI, or microservice frameworks | Standard language test runner | Standard ecosystem linter |

---

## 3. Phase-by-Phase Execution Guide

### Phase 0: Tooling & Runtime Bootstrap
- Auto-detect project runtime, package managers, and dependencies across all languages:
  - Check manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `build.gradle.kts`, `pom.xml`, `composer.json`, `CMakeLists.txt`, `*.csproj`, `Package.swift`, `pubspec.yaml`, `Gemfile`, `renv.lock`).
- Verify test runners and install missing CLI dependencies / SDK tools.
- Ensure the build environment can cleanly compile and test before writing any feature code.

### Phase 0.5: Dual-Engine Indexing (`devcycle-index`)
- Run `python .../devcycle-index/scripts/index_codebase.py .` to ensure `graft/` and `graphify-out/` are fresh.
- Graft supports Tree-Sitter AST parsing across 22+ languages for call graph extraction and blast radius computation.

### Phase 1: Specification Engineering (`devcycle-spec`)
- Interrogate requirements, define measurable Acceptance Criteria (AC), data schemas, API contracts, and security remediation specs.
- Output: `docs/prd/<feature-slug>.md`.

### Phase 2: Vertical-Slice Breakdown (`devcycle-issues`)
- Break the PRD into independent tracer-bullet issues.
- Measure blast radius using `graft callers <symbol> -d 2` or `graft blast`.
- Output: `docs/issues/<feature-slug>/issue-*.md`.

### Phase 3: TDD Implementation (`devcycle-tdd` & `devcycle-ui`)
- Enforce the 3-step Red-Green-Refactor loop in the project's native language & framework:
  1. 🔴 Write failing unit/component test with the framework's native runner. Verify FAIL.
  2. 🟢 Write minimal code to pass test. Verify PASS.
  3. 🔵 Refactor for clean architecture (SOLID) and run polyglot linter (`lint.py` or framework linter).
- If building UI: Invoke `devcycle-ui` for modern design tokens, micro-animations, and visual rendering across Web (React, Vue, Svelte, Vanilla CSS), Mobile (Compose, SwiftUI, Flutter, React Native), or Desktop (Qt, PySide, WPF, MAUI).

### Phase 4: E2E & Integration Testing (`devcycle-e2e`)
- Validate the integrated feature against the real system:
  - **Web**: Playwright, Cypress
  - **Backend API**: Supertest, Newman, curl, HTTP client test harnesses
  - **Desktop / Mobile**: pywinauto, Appium, Maestro, Flutter driver, Qt Test
- Record results in `tests/e2e/cases.csv` or framework-native test artifacts.

### Phase 5: Architecture Refinement (`devcycle-refine`)
- Deepen modules, separate business logic from presentation/infrastructure layer, eliminate tight coupling.

### Phase 6: Requirements & Limitation Audit (`devcycle-audit`)
- Trace every AC in the original PRD to its verifying test.
- Document limitations, performance boundaries, and edge cases in `docs/audit/<feature-slug>.md`.

### Phase 6.5: Red-Team Security Review (`devcycle-security`)
- Auto-detect and install required security tools on demand (`semgrep`, `bandit`, `gitleaks`, `trivy`, `schemathesis`...).
- Multi-layer security testing: Fast Pass (secscan, secrets, SCA) ➔ Deep SAST & API Fuzzing ➔ DAST & Containers ➔ Architecture-specific (Desktop/Mobile/Cloud).
- Trace untrusted inputs from sources to sinks across any language stack.
- Verify vulnerabilities with minimal local PoCs.
- If Critical/High flaws exist: Log to `docs/debug/root-causes.md` and loop back to Phase 1 (`devcycle-spec`).
- 0 Vulnerabilities: Produce security report in `docs/security/` and advance to Phase 7.

### Phase 7: Final Completion & Sign-off
- Produce comprehensive deliverable report (tests executed, tokens saved via Graft, security status, and artifacts created).

---

## 4. Bản Đồ Tích Hợp Toàn Bộ Sub-Skills & Hệ Sinh Thái Kỹ Năng (Sub-Skills Ecosystem Map)

| Giai Đoạn / Sub-Skill | Mục Đích Trọng Tâm | Kỹ Năng Liên Quan Được Tích Hợp Trong Project |
|---|---|---|
| **Phase 0.5**: [devcycle-index](../devcycle-index/SKILL.md) | Chỉ mục kép AST + Semantic GraphRAG | [senior-dev-pipeline](../senior-dev-pipeline/SKILL.md), [output-skill](../output-skill/SKILL.md) |
| **Phase 1**: [devcycle-spec](../devcycle-spec/SKILL.md) | Đặc tả PRD & Acceptance Criteria chống ảo giác | [spec-engineering](../spec-engineering/SKILL.md), [jira-fetch](../jira-fetch/SKILL.md), [brandkit](../brandkit/SKILL.md), [output-skill](../output-skill/SKILL.md) |
| **Phase 2**: [devcycle-issues](../devcycle-issues/SKILL.md) | Phân rã tracer-bullet slices & Blast Radius | [spec-engineering](../spec-engineering/SKILL.md), [jira-bugfix](../jira-bugfix/SKILL.md), [jira-fetch](../jira-fetch/SKILL.md), [output-skill](../output-skill/SKILL.md) |
| **Phase 3**: [devcycle-tdd](../devcycle-tdd/SKILL.md) | Lập trình Red-Green-Refactor + Linter gate | [tdd-development](../tdd-development/SKILL.md), [write-swift](../write-swift/SKILL.md), [output-skill](../output-skill/SKILL.md) |
| **Phase 3 (UI)**: [devcycle-ui](../devcycle-ui/SKILL.md) | UI/UX Pro Max, Micro-motion, Design Tokens | [ui-ux-pro-max](../ui-ux-pro-max/SKILL.md), [impeccable-design](../impeccable-design/SKILL.md), [taste-skill-web](../taste-skill-web/SKILL.md), [animate](../animate/SKILL.md), [apple-design](../apple-design/SKILL.md), [emil-design-eng](../emil-design-eng/SKILL.md), [mobile-native](../mobile-native/SKILL.md), [ask-sonner](../ask-sonner/SKILL.md), [gpt-tasteskill](../gpt-tasteskill/SKILL.md), [image-to-code-skill](../image-to-code-skill/SKILL.md) |
| **Phase 4**: [devcycle-e2e](../devcycle-e2e/SKILL.md) | Kiểm thử đầu cuối E2E & CSV Case Matrix | [mobile-native](../mobile-native/SKILL.md), [ask-sonner](../ask-sonner/SKILL.md), [devcycle-debug](../devcycle-debug/SKILL.md), [jira-bugfix](../jira-bugfix/SKILL.md) |
| **Sub-loop**: [devcycle-debug](../devcycle-debug/SKILL.md) | Chẩn đoán & cô lập nguyên nhân gốc rễ theo bằng chứng | [jira-fetch](../jira-fetch/SKILL.md), [devcycle-bugfix](../devcycle-bugfix/SKILL.md), [jira-bugfix](../jira-bugfix/SKILL.md) |
| **Sub-loop**: [devcycle-bugfix](../devcycle-bugfix/SKILL.md) | Sửa lỗi 7 bước TDD test-first & Convergence Ledger | [jira-bugfix](../jira-bugfix/SKILL.md), [jira-fetch](../jira-fetch/SKILL.md), [tdd-development](../tdd-development/SKILL.md), [output-skill](../output-skill/SKILL.md) |
| **Phase 5**: [devcycle-refine](../devcycle-refine/SKILL.md) | Tinh chỉnh kiến trúc, khử god-nodes, decoupling | [senior-dev-pipeline](../senior-dev-pipeline/SKILL.md), [tdd-development](../tdd-development/SKILL.md), [impeccable-design](../impeccable-design/SKILL.md) |
| **Phase 6**: [devcycle-audit](../devcycle-audit/SKILL.md) | Kiểm toán Traceability Matrix & Giới hạn kỹ thuật | [spec-engineering](../spec-engineering/SKILL.md), [senior-dev-pipeline](../senior-dev-pipeline/SKILL.md), [output-skill](../output-skill/SKILL.md) |
| **Phase 6.5**: [devcycle-security](../devcycle-security/SKILL.md) | Đánh giá an ninh Red-Team đa tầng & Auto-Setup | [redteam-security](../redteam-security/SKILL.md), [senior-dev-pipeline](../senior-dev-pipeline/SKILL.md) |
