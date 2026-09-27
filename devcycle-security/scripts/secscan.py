#!/usr/bin/env python3
"""secscan — Universal Multi-Language Static Security Scanner (DevCycle Phase 6.5).

Scans codebases across TypeScript, JavaScript, Python, Go, Rust, Java, and SQL
for high-signal security vulnerabilities, tainted sinks, and hardcoded secrets.
STATIC ONLY: never imports or executes project code, makes no network calls,
and automatically redacts sensitive secret values.

Usage:
    python secscan.py [PATH] [--format md|json] [--out FILE]

Examples:
    python secscan.py .
    python secscan.py ./backend --format json --out findings.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

# Format: (rule_id, severity, category, regex_pattern, is_secret)
RULES: list[tuple[str, str, str, str, bool]] = [
    # --- A. Command & Code Injection (CWE-78, CWE-94) ---
    (
        "py-subprocess-shell",
        "HIGH",
        "Command Injection (CWE-78)",
        r"subprocess\.\w+\([^)]*shell\s*=\s*True",
        False,
    ),
    (
        "py-os-system",
        "HIGH",
        "Command Injection (CWE-78)",
        r"\bos\.(system|popen)\s*\(",
        False,
    ),
    (
        "js-child-process-exec",
        "HIGH",
        "Command Injection (CWE-78)",
        r"\b(child_process\.(exec|execSync)|exec\s*\([^)]*[\$\+`])",
        False,
    ),
    (
        "universal-eval",
        "CRITICAL",
        "Code Injection (CWE-94)",
        r"(?<![a-zA-Z0-9_\.])(eval|window\.eval|global\.eval)\s*\(",
        False,
    ),
    (
        "js-new-function",
        "HIGH",
        "Dynamic Code Evaluation (CWE-94)",
        r"new\s+Function\s*\(",
        False,
    ),
    (
        "py-pickle-load",
        "CRITICAL",
        "Insecure Deserialization (CWE-502)",
        r"\bpickle\.(loads?|Unpickler)\b",
        False,
    ),
    (
        "py-yaml-unsafe",
        "HIGH",
        "Insecure YAML Loading (CWE-502)",
        r"\byaml\.(unsafe_load|load\([^)]*Loader\s*=\s*yaml\.(Unsafe)?Loader\b)",
        False,
    ),

    # --- B. SQL & Database Injection (CWE-89) ---
    (
        "sql-py-fstring",
        "HIGH",
        "SQL Injection via F-string (CWE-89)",
        r"""(execute|raw)\s*\(\s*f["'][^"']*(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER)\b""",
        False,
    ),
    (
        "sql-js-template-literal",
        "HIGH",
        "SQL Injection via String Interpolation (CWE-89)",
        r"""(\$queryRawUnsafe|query|execute)\s*\(\s*`[^`]*(SELECT|INSERT|UPDATE|DELETE|DROP)\s+[^`]*\$\{""",
        False,
    ),
    (
        "sql-concat",
        "HIGH",
        "SQL Injection via String Concatenation (CWE-89)",
        r"""(execute|query)\s*\([^)]*\+\s*['"][^'"]*(SELECT|INSERT|UPDATE|DELETE)\b""",
        False,
    ),

    # --- C. Cross-Site Scripting & HTML Injection (CWE-79) ---
    (
        "react-dangerously-set-html",
        "MEDIUM",
        "Dangerous Inner HTML Injection (CWE-79)",
        r"dangerouslySetInnerHTML\s*=",
        False,
    ),
    (
        "js-inner-html",
        "MEDIUM",
        "Direct innerHTML Assignment (CWE-79)",
        r"(?<![a-zA-Z0-9_])\.innerHTML\s*=\s*",
        False,
    ),

    # --- D. Cryptography, TLS & JWT Misconfigurations (CWE-327, CWE-295) ---
    (
        "crypto-md5-sha1",
        "LOW",
        "Weak Hash Function (CWE-327)",
        r"(hashlib\.(md5|sha1)|crypto\.createHash\(['\"](md5|sha1)['\"]\))",
        False,
    ),
    (
        "tls-insecure-verify",
        "HIGH",
        "Insecure TLS Verification (CWE-295)",
        r"(verify\s*=\s*False|NODE_TLS_REJECT_UNAUTHORIZED\s*=\s*['\"]?0|InsecureSkipVerify\s*:\s*true|rejectUnauthorized\s*:\s*false)",
        False,
    ),
    (
        "jwt-none-algorithm",
        "CRITICAL",
        "Insecure JWT Algorithm None (CWE-327)",
        r"['\"]algorithms?['\"]\s*:\s*\[\s*['\"]none['\"]",
        False,
    ),

    # --- E. Hardcoded Secrets & Credentials (CWE-798) ---
    (
        "secret-private-key",
        "CRITICAL",
        "Hardcoded Private Key (CWE-798)",
        r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----",
        True,
    ),
    (
        "secret-aws-key",
        "HIGH",
        "Hardcoded AWS Access Key (CWE-798)",
        r"\b(AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}\b",
        True,
    ),
    (
        "secret-generic-api-key",
        "HIGH",
        "Hardcoded API Key/Token (CWE-798)",
        r"""(?i)(api[_-]?key|jwt[_-]?secret|auth[_-]?token|app[_-]?secret)\s*[:=]\s*["'][a-zA-Z0-9_\-\.]{20,}["']""",
        True,
    ),
    (
        "secret-bearer-token",
        "HIGH",
        "Hardcoded Bearer Token (CWE-798)",
        r"""Bearer\s+[a-zA-Z0-9_\-\.]{32,}""",
        True,
    ),
]

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".cache",
    ".venv",
    "venv",
    "__pycache__",
    "graft",
    "graphify-out",
    "coverage",
    ".turbo",
    ".agents",
    ".gemini",
    ".claude",
}

IGNORE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp",
    ".pdf", ".zip", ".tar", ".gz", ".lock", ".min.js", ".min.css",
    ".map", ".woff", ".woff2", ".ttf", ".eot", ".md"
}


def mask_secret(line: str) -> str:
    return re.sub(r'["\'][a-zA-Z0-9_\-\.]{8,}["\']', '"***REDACTED***"', line)


def scan_file(path: Path, root: Path) -> list[dict]:
    findings = []
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    rel_path = str(path.relative_to(root))
    lines = content.splitlines()

    for line_idx, line in enumerate(lines, start=1):
        if len(line) > 500:
            continue
        for rule_id, severity, category, pattern, is_sec in RULES:
            if re.search(pattern, line):
                sample = mask_secret(line.strip()) if is_sec else line.strip()
                findings.append({
                    "rule_id": rule_id,
                    "severity": severity,
                    "category": category,
                    "file": rel_path,
                    "line": line_idx,
                    "code_snippet": sample,
                })
    return findings


def scan_directory(root: Path) -> list[dict]:
    all_findings = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in IGNORE_EXTENSIONS:
                continue
            fpath = Path(dirpath) / f
            all_findings.extend(scan_file(fpath, root))
    return all_findings


def format_markdown(findings: list[dict], root: Path) -> str:
    out = [
        "# DevCycle Security Static Analysis Report (secscan)",
        f"**Target Directory:** `{root}`",
        f"**Total Findings:** {len(findings)}\n",
    ]

    by_sev = {"CRITICAL": [], "HIGH": [], "MEDIUM": [], "LOW": []}
    for f in findings:
        by_sev.get(f["severity"], by_sev["LOW"]).append(f)

    out.append("## Summary by Severity")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        out.append(f"- **{sev}**: {len(by_sev[sev])}")
    out.append("")

    if not findings:
        out.append("🟢 **Result:** No static security vulnerabilities detected.")
        return "\n".join(out)

    out.append("## Detailed Findings\n")
    out.append("| Severity | Category | File & Line | Code Snippet | Rule ID |")
    out.append("|---|---|---|---|---|")
    for f in findings:
        code_esc = f["code_snippet"].replace("|", "\\|")
        out.append(f"| **{f['severity']}** | {f['category']} | `{f['file']}:{f['line']}` | `{code_esc}` | `{f['rule_id']}` |")

    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="Root directory to scan")
    parser.add_argument("--format", choices=["md", "json"], default="md", help="Output format")
    parser.add_argument("--out", help="Write output to file")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    findings = scan_directory(root)

    if args.format == "json":
        output = json.dumps({"findings": findings, "count": len(findings)}, indent=2)
    else:
        output = format_markdown(findings, root)

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Report written to: {args.out}")
    else:
        print(output)

    has_crit_or_high = any(f["severity"] in ("CRITICAL", "HIGH") for f in findings)
    sys.exit(1 if has_crit_or_high else 0)


if __name__ == "__main__":
    main()
