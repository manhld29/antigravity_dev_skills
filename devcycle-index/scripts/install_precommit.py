#!/usr/bin/env python3
"""Install a git **pre-commit** hook that rebuilds both Graft and Graphify code index
in the **background**.

Fires on `pre-commit` and detaches the build (`graft build &` and `graphify . --code-only &`)
so the commit returns immediately — the index never blocks committing. The hook is
path-independent and append-safe: it inserts a marked block into `.git/hooks/pre-commit`,
preserving any existing hook content.

Usage (run from the target app's repo root):
    python install_precommit.py              # install
    python install_precommit.py --status     # check
    python install_precommit.py --uninstall  # remove
"""
from __future__ import annotations

import argparse
import os
import stat
import subprocess
import sys
from pathlib import Path

BEGIN = "# >>> devcycle-index (pre-commit, background: graft + graphify) >>>"
END = "# <<< devcycle-index (pre-commit, background: graft + graphify) <<<"

BLOCK = f"""{BEGIN}
# Rebuild the Graft and Graphify code index in the background (never blocks commit).
if command -v graft >/dev/null 2>&1; then
  ( graft build . >/dev/null 2>&1 & ) >/dev/null 2>&1
fi
if command -v graphify >/dev/null 2>&1; then
  ( graphify . --code-only >/dev/null 2>&1 & ) >/dev/null 2>&1
fi
{END}"""

SHEBANG = "#!/bin/sh"


def _git_root() -> Path:
    start = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=start,
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(out.stdout.strip()).resolve()
    except Exception:
        sys.exit("error: not inside a git repository (run from the app repo root).")


def _hook_path(root: Path) -> Path:
    try:
        out = subprocess.run(
            ["git", "config", "--get", "core.hooksPath"],
            cwd=root,
            capture_output=True,
            text=True,
        )
        hooks_dir = out.stdout.strip()
    except Exception:
        hooks_dir = ""
    base = (root / hooks_dir) if hooks_dir else (root / ".git" / "hooks")
    base.mkdir(parents=True, exist_ok=True)
    return base / "pre-commit"


def _make_executable(path: Path) -> None:
    try:
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except Exception:
        pass


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def install(path: Path) -> None:
    content = _read(path)
    if BEGIN in content:
        print(f"devcycle-index pre-commit hook already installed: {path}")
        return
    if not content.strip():
        new = f"{SHEBANG}\n\n{BLOCK}\n"
    else:
        if not content.startswith("#!"):
            content = f"{SHEBANG}\n{content}"
        sep = "" if content.endswith("\n") else "\n"
        new = f"{content}{sep}\n{BLOCK}\n"
    path.write_text(new, encoding="utf-8")
    _make_executable(path)
    print(f"installed devcycle-index dual pre-commit hook: {path}")


def uninstall(path: Path) -> None:
    content = _read(path)
    if BEGIN not in content or END not in content:
        print(f"no devcycle-index pre-commit hook found: {path}")
        return
    pre, _, rest = content.partition(BEGIN)
    _, _, post = rest.partition(END)
    cleaned = (pre.rstrip() + "\n" + post.lstrip()).strip()
    if cleaned in ("", SHEBANG):
        path.unlink(missing_ok=True)
        print(f"removed devcycle-index pre-commit hook (file deleted): {path}")
    else:
        path.write_text(cleaned + "\n", encoding="utf-8")
        print(f"removed devcycle-index pre-commit hook block: {path}")


def status(path: Path) -> None:
    state = "installed" if BEGIN in _read(path) else "not installed"
    print(f"devcycle-index pre-commit hook: {state} ({path})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--uninstall", action="store_true", help="remove the hook")
    group.add_argument("--status", action="store_true", help="report install state")
    args = parser.parse_args()

    path = _hook_path(_git_root())
    if args.uninstall:
        uninstall(path)
    elif args.status:
        status(path)
    else:
        install(path)


if __name__ == "__main__":
    main()
