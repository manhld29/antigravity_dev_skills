#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""devcycle-ui search — PySide6/QML/QSS design intelligence CLI.

Usage:
    python search.py "<query>" [--domain <domain>] [-n <max>]
    python search.py "<query>" --stack <qml|qss> [-n <max>]
    python search.py "<query>" --design-system [-p "Project"]

Domains: style, color, typography, component, ux, layout
Stacks:  qml, qss

Adapted from ui-ux-pro-max (MIT). Standard library only.
"""

import argparse
import io
import sys

from core import (CSV_CONFIG, AVAILABLE_STACKS, MAX_RESULTS, search,
                  search_stack)

# Force UTF-8 stdout so QSS/QML snippets and arrows survive a cp1252 console.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


def format_output(result):
    if "error" in result:
        return f"Error: {result['error']}"
    out = []
    if result.get("stack"):
        out.append("## devcycle-ui — Stack Guidelines")
        out.append(f"**Stack:** {result['stack']} | **Query:** {result['query']}")
    else:
        out.append("## devcycle-ui — Search Results")
        out.append(f"**Domain:** {result['domain']} | **Query:** {result['query']}")
    out.append(f"**Source:** {result['file']} | **Found:** {result['count']}\n")
    for i, row in enumerate(result["results"], 1):
        out.append(f"### Result {i}")
        for key, value in row.items():
            v = str(value)
            if len(v) > 400:
                v = v[:400] + "..."
            out.append(f"- **{key}:** {v}")
        out.append("")
    if result["count"] == 0:
        out.append("_No matches. Try broader keywords or another --domain._")
    return "\n".join(out)


def design_system(query, project, max_results=2):
    """Lightweight aggregator: style + color + typography + key components."""
    head = f"# devcycle-ui Design System — {project or query}\n"
    sections = [
        ("Recommended style", search(query, "style", 1)),
        ("Color palette", search(query, "color", 1)),
        ("Typography", search(query, "typography", 1)),
        ("Core components", search(query + " button dialog form", "component", max_results)),
        ("UX must-haves", search(query + " accessibility focus feedback", "ux", max_results)),
    ]
    blocks = [head]
    for title, res in sections:
        blocks.append(f"## {title}")
        blocks.append(format_output(res).split("\n", 3)[-1] if res.get("count") else "_none_")
    blocks.append("\n> Next: `--stack qml` or `--stack qss` for implementation guidelines.")
    return "\n".join(blocks)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="devcycle-ui design search (PySide6/QML/QSS)")
    p.add_argument("query", help="search query")
    p.add_argument("--domain", "-d", choices=list(CSV_CONFIG.keys()), help="search domain")
    p.add_argument("--stack", "-s", choices=AVAILABLE_STACKS, help="qml or qss guidelines")
    p.add_argument("--max-results", "-n", type=int, default=MAX_RESULTS)
    p.add_argument("--design-system", "-ds", action="store_true",
                   help="aggregate style+color+typography+components+ux")
    p.add_argument("--project-name", "-p", default=None)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.design_system:
        print(design_system(args.query, args.project_name, args.max_results))
    elif args.stack:
        res = search_stack(args.query, args.stack, args.max_results)
        if args.json:
            import json
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print(format_output(res))
    else:
        res = search(args.query, args.domain, args.max_results)
        if args.json:
            import json
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print(format_output(res))
