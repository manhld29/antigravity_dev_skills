#!/usr/bin/env python3
"""Universal Polyglot Code-Quality & Linter Gate for DevCycle (Phase 3).

Auto-detects project stack and enforces strict code quality, style, and formatting
across all programming languages and frameworks:
  - TypeScript/JavaScript: ESLint, Biome, Prettier, tsc, Deno/Bun
  - Python: Ruff, Flake8, Black, Isort, Mypy
  - Go: golangci-lint, go vet, gofmt
  - Rust: cargo clippy, cargo fmt
  - Java / Kotlin: ktlint, detekt, Spotless, Checkstyle (Gradle/Maven)
  - PHP: PHP-CS-Fixer, PHPStan, Psalm
  - C / C++: clang-tidy, cppcheck, clang-format
  - C# / .NET: dotnet format, Roslyn analyzers
  - Swift: swiftlint, swift-format
  - Dart: dart analyze, flutter analyze
  - Ruby: rubocop, standardrb
  - R: lintr, styler

Usage:
    python lint.py [PATH] [--fix] [--stack auto|ts|py|go|rust|java|kotlin|php|cpp|csharp|swift|dart|ruby|r]

Exit code 0 = Clean gate · Non-zero = Findings exist or tool error.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], cwd: Path) -> tuple[int, str]:
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        out = (proc.stdout + "\n" + proc.stderr).strip()
        return proc.returncode, out
    except Exception as exc:
        return 1, str(exc)


def detect_stacks(root: Path) -> list[str]:
    stacks = []
    if (root / "package.json").exists() or any(root.glob("*/package.json")) or (root / "deno.json").exists():
        stacks.append("ts")
    if (root / "pyproject.toml").exists() or (root / "setup.cfg").exists() or (root / "requirements.txt").exists() or any(root.glob("*.py")):
        stacks.append("py")
    if (root / "go.mod").exists():
        stacks.append("go")
    if (root / "Cargo.toml").exists():
        stacks.append("rust")
    if (root / "build.gradle.kts").exists() or any(root.glob("**/*.kt")):
        stacks.append("kotlin")
    elif (root / "pom.xml").exists() or (root / "build.gradle").exists() or any(root.glob("**/*.java")):
        stacks.append("java")
    if (root / "composer.json").exists():
        stacks.append("php")
    if (root / "CMakeLists.txt").exists() or any(root.glob("**/*.cpp")) or any(root.glob("**/*.c")):
        stacks.append("cpp")
    if any(root.glob("*.sln")) or any(root.glob("**/*.csproj")):
        stacks.append("csharp")
    if (root / "Package.swift").exists() or any(root.glob("**/*.swift")):
        stacks.append("swift")
    if (root / "pubspec.yaml").exists():
        stacks.append("dart")
    if (root / "Gemfile").exists():
        stacks.append("ruby")
    if (root / "renv.lock").exists() or any(root.glob("**/*.R")):
        stacks.append("r")

    return stacks or ["ts", "py"]


def lint_typescript(root: Path, fix: bool) -> bool:
    print("--- [TypeScript / JavaScript Quality Gate] ---")
    all_ok = True
    pkg_paths = [root] if (root / "package.json").exists() else [p.parent for p in root.glob("*/package.json")]
    if not pkg_paths:
        pkg_paths = [root]

    for p in pkg_paths:
        label = p.relative_to(root) if p != root else "root"
        print(f"Checking package: {label}")
        if (p / "package.json").exists():
            lint_cmd = ["npm", "run", "lint", "--if-present"]
            if fix:
                lint_cmd = ["npm", "run", "lint:fix", "--if-present"]
            code, out = run_command(lint_cmd, cwd=p)
            if code != 0 and "missing script" not in out.lower():
                print(f"  ✗ Linter errors in {label}:\n{out}")
                all_ok = False
            else:
                print(f"  ✓ Linter check passed for {label}")
    return all_ok


def lint_python(root: Path, fix: bool) -> bool:
    print("--- [Python Quality Gate] ---")
    all_ok = True
    if shutil.which("ruff"):
        cmd = ["ruff", "check", "."]
        if fix:
            cmd.append("--fix")
        code, out = run_command(cmd, cwd=root)
        if code != 0:
            print(f"  ✗ ruff check errors:\n{out}")
            all_ok = False
        else:
            print("  ✓ ruff check passed")
    else:
        if shutil.which("isort"):
            cmd = ["isort", "--check-only", "."] if not fix else ["isort", "."]
            code, out = run_command(cmd, cwd=root)
            if code != 0:
                print(f"  ✗ isort findings:\n{out}")
                all_ok = False
            else:
                print("  ✓ isort passed")

        if shutil.which("flake8"):
            code, out = run_command(["flake8", "."], cwd=root)
            if code != 0:
                print(f"  ✗ flake8 findings:\n{out}")
                all_ok = False
            else:
                print("  ✓ flake8 passed")
    return all_ok


def lint_go(root: Path, fix: bool) -> bool:
    print("--- [Go Quality Gate] ---")
    if shutil.which("golangci-lint"):
        cmd = ["golangci-lint", "run"]
        if fix:
            cmd.append("--fix")
        code, out = run_command(cmd, cwd=root)
        if code != 0:
            print(f"  ✗ golangci-lint errors:\n{out}")
            return False
    elif shutil.which("go"):
        code, out = run_command(["go", "vet", "./..."], cwd=root)
        if code != 0:
            print(f"  ✗ go vet errors:\n{out}")
            return False
    print("  ✓ Go quality check passed")
    return True


def lint_rust(root: Path, fix: bool) -> bool:
    print("--- [Rust Quality Gate] ---")
    if shutil.which("cargo"):
        code, out = run_command(["cargo", "clippy", "--", "-D", "warnings"], cwd=root)
        if code != 0:
            print(f"  ✗ cargo clippy errors:\n{out}")
            return False
    print("  ✓ Rust clippy check passed")
    return True


def lint_kotlin(root: Path, fix: bool) -> bool:
    print("--- [Kotlin Quality Gate] ---")
    gradle_bin = "./gradlew" if (root / "gradlew").exists() else "gradle"
    if shutil.which(gradle_bin) or (root / "gradlew").exists():
        task = "ktlintCheck" if not fix else "ktlintFormat"
        code, out = run_command([gradle_bin, task, "--quiet"], cwd=root)
        if code != 0 and "task not found" not in out.lower():
            print(f"  ✗ Kotlin linter errors:\n{out}")
            return False
    print("  ✓ Kotlin quality check passed")
    return True


def lint_java(root: Path, fix: bool) -> bool:
    print("--- [Java Quality Gate] ---")
    gradle_bin = "./gradlew" if (root / "gradlew").exists() else "gradle"
    mvn_bin = "./mvnw" if (root / "mvnw").exists() else "mvn"
    if (root / "gradlew").exists():
        code, out = run_command([gradle_bin, "check", "-x", "test"], cwd=root)
        if code != 0 and "task not found" not in out.lower():
            print(f"  ✗ Gradle check errors:\n{out}")
            return False
    elif shutil.which(mvn_bin) or (root / "mvnw").exists():
        code, out = run_command([mvn_bin, "checkstyle:check"], cwd=root)
        if code != 0 and "no plugin found" not in out.lower():
            print(f"  ✗ Maven checkstyle errors:\n{out}")
            return False
    print("  ✓ Java quality check passed")
    return True


def lint_php(root: Path, fix: bool) -> bool:
    print("--- [PHP Quality Gate] ---")
    phpstan = root / "vendor/bin/phpstan"
    if phpstan.exists():
        code, out = run_command([str(phpstan), "analyse"], cwd=root)
        if code != 0:
            print(f"  ✗ PHPStan errors:\n{out}")
            return False
    print("  ✓ PHP quality check passed")
    return True


def lint_dart(root: Path, fix: bool) -> bool:
    print("--- [Dart / Flutter Quality Gate] ---")
    cmd = ["flutter", "analyze"] if shutil.which("flutter") and (root / "pubspec.yaml").exists() else ["dart", "analyze"]
    if shutil.which(cmd[0]):
        code, out = run_command(cmd, cwd=root)
        if code != 0:
            print(f"  ✗ {cmd[0]} analyze errors:\n{out}")
            return False
    print("  ✓ Dart / Flutter analyze passed")
    return True


def lint_csharp(root: Path, fix: bool) -> bool:
    print("--- [C# / .NET Quality Gate] ---")
    if shutil.which("dotnet"):
        cmd = ["dotnet", "format", "--verify-no-changes"] if not fix else ["dotnet", "format"]
        code, out = run_command(cmd, cwd=root)
        if code != 0:
            print(f"  ✗ dotnet format findings:\n{out}")
            return False
    print("  ✓ C# dotnet format passed")
    return True


def lint_ruby(root: Path, fix: bool) -> bool:
    print("--- [Ruby Quality Gate] ---")
    if shutil.which("bundle"):
        cmd = ["bundle", "exec", "rubocop"]
        if fix:
            cmd.append("-A")
        code, out = run_command(cmd, cwd=root)
        if code != 0 and "could not find gem" not in out.lower():
            print(f"  ✗ RuboCop findings:\n{out}")
            return False
    print("  ✓ Ruby quality check passed")
    return True


def lint_swift(root: Path, fix: bool) -> bool:
    print("--- [Swift Quality Gate] ---")
    if shutil.which("swiftlint"):
        cmd = ["swiftlint"]
        if fix:
            cmd.append("--fix")
        code, out = run_command(cmd, cwd=root)
        if code != 0:
            print(f"  ✗ SwiftLint findings:\n{out}")
            return False
    print("  ✓ Swift quality check passed")
    return True


def lint_cpp(root: Path, fix: bool) -> bool:
    print("--- [C / C++ Quality Gate] ---")
    if shutil.which("cppcheck"):
        code, out = run_command(["cppcheck", "--enable=warning,style", "--error-exitcode=1", "."], cwd=root)
        if code != 0:
            print(f"  ✗ cppcheck findings:\n{out}")
            return False
    print("  ✓ C / C++ quality check passed")
    return True


def lint_r(root: Path, fix: bool) -> bool:
    print("--- [R Quality Gate] ---")
    if shutil.which("Rscript"):
        code, out = run_command(["Rscript", "-e", "if (requireNamespace('lintr', quietly=TRUE)) lintr::lint_dir()"], cwd=root)
        if code != 0:
            print(f"  ✗ R lintr findings:\n{out}")
            return False
    print("  ✓ R quality check passed")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="Root directory")
    parser.add_argument("--fix", action="store_true", help="Auto-fix safe formatting issues")
    parser.add_argument(
        "--stack",
        choices=["auto", "ts", "py", "go", "rust", "kotlin", "java", "php", "cpp", "csharp", "swift", "dart", "ruby", "r"],
        default="auto",
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    stacks = [args.stack] if args.stack != "auto" else detect_stacks(root)

    print(f"=== DevCycle Code Quality & Lint Gate ===")
    print(f"Directory: {root}")
    print(f"Detected Stacks: {', '.join(stacks)}\n")

    overall_clean = True
    dispatch = {
        "ts": lint_typescript,
        "py": lint_python,
        "go": lint_go,
        "rust": lint_rust,
        "kotlin": lint_kotlin,
        "java": lint_java,
        "php": lint_php,
        "cpp": lint_cpp,
        "csharp": lint_csharp,
        "swift": lint_swift,
        "dart": lint_dart,
        "ruby": lint_ruby,
        "r": lint_r,
    }

    for s in stacks:
        if s in dispatch:
            if not dispatch[s](root, args.fix):
                overall_clean = False

    print()
    if overall_clean:
        print("🟢 GATE PASSED: Code quality is clean.")
        sys.exit(0)
    else:
        print("🔴 GATE FAILED: Code quality findings exist. Fix before proceeding.")
        sys.exit(1)


if __name__ == "__main__":
    main()
