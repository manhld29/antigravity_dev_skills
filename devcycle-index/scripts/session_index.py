#!/usr/bin/env python3
"""SessionStart hook for devcycle-index.

Kicks off both Graft and Graphify code-index builds automatically when a project is opened,
so the rest of the devcycle pipeline can query the map instead of grepping. The
builds are launched **in the background** (fully detached child processes) so they
never block session startup — the hook returns immediately and the rebuilt
``graft/`` and ``graphify-out/`` land a few seconds later.

Behaviour is controlled by the ``DEVCYCLE_INDEX_ON_START`` env var:
    missing  (default) start a background build only if indices are absent
    always             start a background rebuild on every session open
    off                do nothing
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def _project_dir() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()


def _emit(context: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": context,
                }
            }
        )
    )
    sys.exit(0)


def _spawn_background(cmd: list[str], project: Path) -> None:
    kwargs = dict(
        cwd=str(project),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if os.name == "nt":
        creationflags = 0x00000008 | 0x00000200
        subprocess.Popen(cmd, creationflags=creationflags, **kwargs)
    else:
        subprocess.Popen(cmd, start_new_session=True, **kwargs)


def main() -> None:
    mode = os.environ.get("DEVCYCLE_INDEX_ON_START", "missing").strip().lower()
    if mode == "off":
        sys.exit(0)

    project = _project_dir()
    graft_wiring = project / "graft" / ".graph" / "wiring.json"
    graph_json = project / "graphify-out" / "graph.json"
    index_present = graft_wiring.is_file() and graph_json.is_file()

    if mode != "always" and index_present:
        _emit(
            "devcycle-index: dual code maps present (graft/ and graphify-out/). "
            "Query with `graft callers <symbol>`, `graft skeleton <file>`, or `graphify query '<q>'`."
        )

    graft_bin = shutil.which("graft")
    graphify_bin = shutil.which("graphify")

    if graft_bin:
        try:
            _spawn_background([graft_bin, "build", str(project)], project)
        except Exception:
            pass

    if graphify_bin:
        try:
            _spawn_background([graphify_bin, str(project), "--code-only"], project)
        except Exception:
            pass

    _emit(
        "devcycle-index: started background dual indexing (Graft + Graphify) on open. "
        "Maps will refresh shortly. Query with `graft callers` or `graphify query`."
    )


if __name__ == "__main__":
    main()
