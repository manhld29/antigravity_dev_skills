#!/usr/bin/env python3
"""Unified Codebase Indexer: Graft + Graphify Dual-Engine Runner.

Runs both Graft (@nanonets/graft) and Graphify (graphifyy) in parallel or sequence,
ensuring the target project has both:
  1. graft/            (Tree-Sitter AST call graph, skeletons, blast radius)
  2. graphify-out/     (Semantic GraphRAG, community map, query/path/explain)

Usage:
    python index_codebase.py [DIR] [--code-only] [--deep] [--no-reuse] [--viz]

Examples:
    python index_codebase.py .
    python index_codebase.py /path/to/project --code-only
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


def check_tool(name: str) -> str | None:
    return shutil.which(name)


def run_cmd(cmd: list[str], cwd: Path, name: str) -> bool:
    print(f"[{name}] Running: {' '.join(cmd)}")
    start = time.time()
    res = subprocess.run(cmd, cwd=cwd)
    duration = time.time() - start
    if res.returncode == 0:
        print(f"[{name}] ✓ Completed successfully in {duration:.2f}s")
        return True
    else:
        print(f"[{name}] ✗ Failed with exit code {res.returncode}")
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dir", nargs="?", default=".", help="Project root directory")
    parser.add_argument("--deep", action="store_true", help="Run graft with --deep LLM pass")
    parser.add_argument("--code-only", action="store_true", default=True, help="Index code files offline (default: True)")
    parser.add_argument("--no-reuse", action="store_true", help="Force cold re-parse in graft")
    args = parser.parse_args()

    project_dir = Path(args.dir).resolve()
    print(f"=== DevCycle Dual-Engine Codebase Indexer ===")
    print(f"Target Directory: {project_dir}\n")

    graft_bin = check_tool("graft")
    graphify_bin = check_tool("graphify")

    if not graft_bin and not graphify_bin:
        sys.exit("Error: Neither 'graft' nor 'graphify' was found on PATH. Please install them.")

    success_count = 0

    # 1. Run Graft
    if graft_bin:
        graft_cmd = [graft_bin, "build"]
        if args.deep:
            graft_cmd.append("--deep")
        if args.no_reuse:
            graft_cmd.append("--no-reuse")
        graft_cmd.append(str(project_dir))

        if run_cmd(graft_cmd, cwd=project_dir, name="Graft"):
            success_count += 1
    else:
        print("[Graft] Warning: 'graft' not found on PATH. Skipping.")

    print()

    # 2. Run Graphify
    if graphify_bin:
        graphify_cmd = [graphify_bin, str(project_dir)]
        if args.code_only:
            graphify_cmd.append("--code-only")

        if run_cmd(graphify_cmd, cwd=project_dir, name="Graphify"):
            success_count += 1
    else:
        print("[Graphify] Warning: 'graphify' not found on PATH. Skipping.")

    print()
    print(f"=== Dual-Engine Index Summary ===")
    print(f"Engines completed: {success_count}/2")
    if (project_dir / "graft").exists():
        print(f"✓ graft/ ready (use: graft callers <symbol>, graft skeleton <file>, graft map)")
    if (project_dir / "graphify-out" / "graph.json").exists():
        print(f"✓ graphify-out/ ready (use: graphify query '<question>', graphify path <A> <B>)")


if __name__ == "__main__":
    main()
