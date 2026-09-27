#!/usr/bin/env python3
"""Unified Query Dispatcher for Graft + Graphify.

Dispatches code inquiries to the right engine:
  - Concept/Flow questions -> graphify query "<q>"
  - Caller/Callee tracing  -> graft callers <symbol>
  - API signatures         -> graft skeleton <file>
  - Shortest path          -> graphify path <A> <B>
  - Blast radius           -> graft blast / graft callers -d 2
  - Hubs & hotspots        -> graphify god-nodes / graft map

Usage:
    python query_graph.py query "how does auth work"
    python query_graph.py callers SymbolName [--direction out] [--depth N]
    python query_graph.py skeleton path/to/file
    python query_graph.py path NodeA NodeB
    python query_graph.py map
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="subcommand", help="Query subcommand")

    # query
    p_query = subparsers.add_parser("query", help="Semantic GraphRAG query (Graphify / Graft)")
    p_query.add_argument("text", help="Question or query string")
    p_query.add_argument("--budget", type=int, default=2000, help="Token budget")

    # callers
    p_callers = subparsers.add_parser("callers", help="Trace callers/callees (Graft)")
    p_callers.add_argument("symbol", help="Function, class, or type symbol")
    p_callers.add_argument("--direction", choices=["in", "out"], default="in", help="in: who calls it, out: what it calls")
    p_callers.add_argument("-d", "--depth", default="1", help="Traversal depth (default: 1, or 'all')")

    # skeleton
    p_skel = subparsers.add_parser("skeleton", help="View file API skeleton without body (Graft)")
    p_skel.add_argument("file", help="File path")

    # path
    p_path = subparsers.add_parser("path", help="Shortest path between two nodes (Graphify)")
    p_path.add_argument("source", help="Source node")
    p_path.add_argument("target", help="Target node")

    # map
    subparsers.add_parser("map", help="Repo orientation map (Graft)")

    args = parser.parse_args()

    if not args.subcommand:
        parser.print_help()
        sys.exit(1)

    graft_bin = shutil.which("graft")
    graphify_bin = shutil.which("graphify")

    if args.subcommand == "query":
        if graphify_bin:
            cmd = [graphify_bin, "query", args.text, "--budget", str(args.budget)]
            subprocess.run(cmd)
        elif graft_bin:
            cmd = [graft_bin, "ask", args.text]
            subprocess.run(cmd)
        else:
            sys.exit("Neither graphify nor graft found on PATH.")

    elif args.subcommand == "callers":
        if graft_bin:
            cmd = [graft_bin, "callers", args.symbol]
            if args.direction == "out":
                cmd.extend(["--direction", "out"])
            if args.depth != "1":
                cmd.extend(["-d", str(args.depth)])
            subprocess.run(cmd)
        elif graphify_bin:
            cmd = [graphify_bin, "explain", args.symbol]
            subprocess.run(cmd)
        else:
            sys.exit("Neither graft nor graphify found on PATH.")

    elif args.subcommand == "skeleton":
        if graft_bin:
            cmd = [graft_bin, "skeleton", args.file]
            subprocess.run(cmd)
        else:
            sys.exit("graft is required for skeleton view.")

    elif args.subcommand == "path":
        if graphify_bin:
            cmd = [graphify_bin, "path", args.source, args.target]
            subprocess.run(cmd)
        else:
            sys.exit("graphify is required for path queries.")

    elif args.subcommand == "map":
        if graft_bin:
            cmd = [graft_bin, "map"]
            subprocess.run(cmd)
        elif graphify_bin:
            cmd = [graphify_bin, "god-nodes"]
            subprocess.run(cmd)
        else:
            sys.exit("Neither graft nor graphify found on PATH.")


if __name__ == "__main__":
    main()
