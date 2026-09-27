---
name: devcycle-tdd
description: "Universal Test-Driven Development (TDD) skill based on Matt Pocock standards and clean architecture. Enforces strict Red-Green-Refactor cycles across any programming language (TypeScript, JavaScript, Python, Go, Rust, Java, PHP, C, C++, Swift, Dart, Ruby, R, C#, Kotlin) and all their frameworks, type safety, SOLID principles, and clean linter gates. Stage 3 of the devcycle pipeline. Triggers: \"implement issue\", \"write test and code\", \"TDD\", \"devcycle-tdd\", \"lập trình TDD\"."
argument-hint: "Which issue are we building test-first?"
---

# Devcycle — TDD (Issue → Test First → Minimal Code → Refactor)

Stage 3 of [devcycle](../devcycle/SKILL.md). Implements an issue by executing the
strict **Red-Green-Refactor loop** (Matt Pocock standards). Business logic is tested
through public interfaces and decoupled from presentation frameworks.

---

## 1. Tooling & Environment Auto-Setup

Before writing tests, verify the test runner across any language and framework:
- **TypeScript / JavaScript** (React, Next.js, Vue, Node, etc.): `vitest`, `jest`, `mocha` (`npm test`)
- **Python** (FastAPI, Django, Flask, PySide6, etc.): `pytest` (`pytest -v`)
- **Go** (Gin, Echo, Chi, etc.): `go test ./...`
- **Rust** (Actix, Axum, Tokio, etc.): `cargo test`
- **Java** (Spring Boot, Quarkus, etc.): `./mvnw test` or `./gradlew test` (JUnit 5)
- **Kotlin** (Android Compose, Ktor, etc.): `./gradlew test` (JUnit 5, MockK, Kotest)
- **PHP** (Laravel, Symfony, etc.): `vendor/bin/phpunit` or `pest`
- **C / C++** (Qt, Boost, etc.): `ctest`, `./build/bin/tests` (GoogleTest, Catch2)
- **C# / .NET** (ASP.NET, MAUI, etc.): `dotnet test` (xUnit, NUnit)
- **Swift** (SwiftUI, Vapor, etc.): `swift test` (XCTest, Swift Testing)
- **Dart** (Flutter, Shelf, etc.): `dart test` or `flutter test`
- **Ruby** (Rails, Sinatra, etc.): `bundle exec rspec`
- **R** (Shiny, Plumber, etc.): `Rscript -e "testthat::test_dir('tests')"`

If missing, install development dependencies automatically before proceeding.

---

## 2. The 3-Step Red-Green-Refactor Loop

```
 ┌────────────────────────┐
 │ 1. 🔴 RED              │ Viết Test trước, chạy lệnh và xác nhận test FAIL.
 └──────────┬─────────────┘
            ▼
 ┌────────────────────────┐
 │ 2. 🟢 GREEN            │ Viết code tối thiểu để test PASS. Không over-engineer.
 └──────────┬─────────────┘
            ▼
 ┌────────────────────────┐
 │ 3. 🔵 REFACTOR & LINT  │ Tối ưu code (SOLID), chạy lint.py gate.
 └────────────────────────┘
```

### Step 1: 🔴 RED (Failing Test First)
- Write test case corresponding to the issue's Acceptance Criteria.
- Run the test command.
- **MANDATORY CHECK**: Test must FAIL for the expected reason (e.g. function missing or assertion failed). Never proceed if the test passes prematurely.

### Step 2: 🟢 GREEN (Minimal Code)
- Write only the code required to satisfy the failing test.
- Run the test command and verify test PASSES.

### Step 3: 🔵 REFACTOR & Code Quality Gate
- Refactor for readability, eliminate duplication, and enforce SOLID principles:
  - **Single Responsibility**: Each class/service handles one concern.
  - **Dependency Inversion**: High-level modules depend on abstractions/interfaces.
- Run the polyglot linter gate:
  ```bash
  python ~/.gemini/config/skills/devcycle-tdd/scripts/lint.py .
  ```
- The cycle is **NOT green** until both test suite passes AND linters are clean.

---

## 3. UI Slices Integration
If the issue includes UI work (Web components or Desktop views):
- Consult `devcycle-ui` for modern design tokens, layout hierarchy, and micro-animations.
- Keep business logic isolated in models/services so it remains unit-testable without a DOM or window.

---

## 4. Liên Kết Với Các Kỹ Năng Liên Quan (Skill Ecosystem Integration)

- [tdd-development](../tdd-development/SKILL.md): Chuẩn mực kỹ nghệ TDD Matt Pocock, type-level testing, và kiến trúc Clean Architecture tách biệt domain với I/O.
- [devcycle-ui](../devcycle-ui/SKILL.md): Thiết kế và tạo kiểu các component UI/UX, kiểm thử tương tác state và micro-animations test-first.
- [output-skill](../output-skill/SKILL.md): Bắt buộc sinh toàn bộ mã test và implementation hoàn chỉnh 100%, nghiêm cấm cắt xén, viết tắt hay dùng code placeholder.
- [write-swift](../write-swift/SKILL.md): Chuyên sâu ngôn ngữ Swift hiện đại — Swift Testing framework (`@Test`, `#expect`), Swift 6 concurrency, value types và ARC optimizations.
- [devcycle-debug](../devcycle-debug/SKILL.md) & [devcycle-bugfix](../devcycle-bugfix/SKILL.md): Cơ chế viết regression test bắt buộc trước khi vá bất kỳ lỗi runtime nào.
- [devcycle-e2e](../devcycle-e2e/SKILL.md): Bước tiếp nối sau khi toàn bộ unit test các issue đều đã GREEN để kiểm thử hành trình tích hợp E2E.
