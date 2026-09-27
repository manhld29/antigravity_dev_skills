"""Load and validate .env.dev for the devcycle desktop E2E harness.

Single source of truth for credentials, launch command, window title, and log
path. Used by tests/e2e/conftest.py and (optionally) devcycle-debug.

Usage as a module:
    from env_loader import load_env, tail_log
    cfg = load_env()                 # dict with validated keys
    print(tail_log(cfg))             # last N lines of APP_LOG_PATH

Usage as a CLI:
    python env_loader.py --check     # validate .env.dev, exit non-zero if bad
    python env_loader.py --tail-log  # print the tail of APP_LOG_PATH
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

REQUIRED = ["APP_LAUNCH_CMD", "APP_WINDOW_TITLE", "APP_USERNAME", "APP_PASSWORD", "APP_LOG_PATH"]
DEFAULTS = {
    "APP_CWD": "",
    "APP_BACKEND": "uia",
    "APP_STARTUP_TIMEOUT": "30",
    "APP_LOG_TAIL_LINES": "200",
    "APP_SANDBOX": "on",
    "APP_SANDBOX_ENV": "",
}
SECRET_KEYS = {"APP_PASSWORD"}


def find_env_file(start: Path | None = None) -> Path:
    """Walk upward from `start` (or CWD) to find .env.dev."""
    here = (start or Path.cwd()).resolve()
    for parent in [here, *here.parents]:
        candidate = parent / ".env.dev"
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        ".env.dev not found. Create it at the repo root (see devcycle/ENV-FORMAT.md)."
    )


def _parse(path: Path) -> dict[str, str]:
    cfg: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        cfg[key.strip()] = value.strip().strip('"').strip("'")
    return cfg


def load_env(start: Path | None = None) -> dict[str, str]:
    """Return a validated config dict, applying defaults for optional keys."""
    path = find_env_file(start)
    cfg = {**DEFAULTS, **_parse(path)}
    missing = [k for k in REQUIRED if not cfg.get(k)]
    if missing:
        raise ValueError(
            f"{path} is missing required keys: {', '.join(missing)}. "
            "See devcycle/ENV-FORMAT.md."
        )
    cfg["_env_path"] = str(path)
    return cfg


def redacted(cfg: dict[str, str]) -> dict[str, str]:
    """A copy safe to print: secrets masked."""
    return {k: ("******" if k in SECRET_KEYS else v) for k, v in cfg.items()}


_WIN_VAR = re.compile(r"%([^%]+)%")
_NIX_VAR = re.compile(r"\$\{([^}]+)\}|\$(\w+)")


def _expand(value: str, environ: dict[str, str]) -> str:
    """Expand %VAR% / $VAR / ${VAR} / ~ against `environ`, WITHOUT touching os.environ.

    The E2E sandbox never mutates the test runner's os.environ, so a log path like
    `%TEMP%\\app.log` must be resolved against the CHILD's environment or the tail
    would come from the host's TEMP — a different (usually stale) file. Substitute by
    lookup rather than swapping the global os.environ in and out: the swap is not
    thread-safe (parallel runners would read a half-wiped environ) and a KeyboardInterrupt
    mid-swap would drop the runner's own environment. Unknown names are left verbatim.
    """
    if value.startswith("~"):
        home = environ.get("USERPROFILE") or environ.get("HOME") or ""
        if home:
            value = home + value[1:]
    value = _WIN_VAR.sub(lambda m: environ.get(m.group(1), m.group(0)), value)
    value = _NIX_VAR.sub(
        lambda m: environ.get(m.group(1) or m.group(2), m.group(0)), value
    )
    return value


# Best-effort masks so a leaked bearer/JWT/OAuth token in the app log never lands
# verbatim in cases.csv actual_result or a test report. Each keeps its label prefix
# (group 1) and blanks the value; the bare-JWT pattern blanks the whole match.
_SECRET_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?i)(bearer\s+)[\w\-.=]+"), r"\1******"),
    (re.compile(r"(?i)((?:access|refresh|id)[_-]?token[\"']?\s*[:=]\s*[\"']?)[\w\-.]+"),
     r"\1******"),
    (re.compile(r"eyJ[\w\-]+\.[\w\-]+\.[\w\-]+"), "******"),  # bare JWT
]


def _mask_secrets(line: str, extra: str = "") -> str:
    """Redact known-secret shapes (plus `extra`, e.g. the plaintext password)."""
    if extra:
        line = line.replace(extra, "******")
    for pattern, repl in _SECRET_PATTERNS:
        line = pattern.sub(repl, line)
    return line


def tail_log(
    cfg: dict[str, str] | None = None,
    lines: int | None = None,
    environ: dict[str, str] | None = None,
) -> str:
    """Return the last N lines of APP_LOG_PATH (file, or newest file in a dir).

    Pass `environ` (e.g. the E2E sandbox's child env) to resolve a log path that
    references redirected variables such as %TEMP%.
    """
    cfg = cfg or load_env()
    n = lines if lines is not None else int(cfg.get("APP_LOG_TAIL_LINES", "200"))
    log_path = Path(_expand(cfg["APP_LOG_PATH"], environ or dict(os.environ)))
    if log_path.is_dir():
        logs = sorted(log_path.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not logs:
            return f"(no .log files in {log_path})"
        log_path = logs[0]
    if not log_path.is_file():
        return f"(log not found: {log_path})"
    content = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    secret = (cfg.get("APP_PASSWORD") or "").strip()
    tail = [_mask_secrets(ln, secret) for ln in content[-n:]]
    return f"# tail -{n} of {log_path}\n" + "\n".join(tail)


def main() -> int:
    ap = argparse.ArgumentParser(description="devcycle .env.dev loader")
    ap.add_argument("--check", action="store_true", help="validate .env.dev")
    ap.add_argument("--tail-log", action="store_true", help="print tail of APP_LOG_PATH")
    args = ap.parse_args()
    try:
        cfg = load_env()
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if args.tail_log:
        print(tail_log(cfg))
    else:  # default / --check
        print("OK: .env.dev valid")
        for k, v in redacted(cfg).items():
            if not k.startswith("_"):
                print(f"  {k}={v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
