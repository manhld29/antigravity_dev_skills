---
name: devcycle-index
description: "Auto-build and maintain a high-performance, queryable dual-engine code index (knowledge graph) of the codebase combining Graft (@nanonets/graft) and Graphify (graphifyy). Supports 22+ languages (TypeScript, JavaScript, Python, Go, Rust, Java, C/C++, PHP, etc.) with $0 offline Tree-Sitter AST parsing, call-graph wiring, blast radius calculation, API skeletons, GraphRAG semantic queries, and visual explorers. Produces graft/ (wiring graph & cards) and graphify-out/ (graph.json, GRAPH_REPORT.md, graph.html). Use when the user wants to index the codebase, build a code map/graph, query code connections, trace callers/callees, analyze blast radius, inspect API skeletons, navigate an unfamiliar repo, or says \"index the codebase\", \"build the graph\", \"devcycle-index\", \"graft\", \"graphify\", \"blast radius\", \"trace callers\"."
argument-hint: "Path to index (default: current repo) or query/symbol to trace"
---

# Devcycle — Index (Dual-Engine Codebase Intelligence: Graft + Graphify)

Builds and keeps fresh a **dual-engine queryable index of the codebase** so the entire
devcycle pipeline navigates by structured maps instead of blind grepping. Powered by
[Graft](https://github.com/trailhq/Graft) (Tree-Sitter AST wiring, call graph, blast radius,
skeletons, visualizer) and [Graphify](https://github.com/Graphify-Labs/graphify) (GraphRAG,
community clustering, path finding, and callflow HTML).

Both engines index **fully offline** ($0, no API key needed, nothing leaves your machine).

```
                      ┌──────────────────────────────────────────────┐
                      │          Source Code (22+ Languages)         │
                      └──────────────────────┬───────────────────────┘
                                             │
                      ┌──────────────────────┴───────────────────────┐
                      ▼                                              ▼
         ┌─────────────────────────┐                    ┌─────────────────────────┐
         │       GRAFT ENGINE      │                    │     GRAPHIFY ENGINE     │
         │   (@nanonets/graft)     │                    │       (graphifyy)       │
         ├─────────────────────────┤                    ├─────────────────────────┤
         │ • $0 Tree-Sitter AST    │                    │ • Community Clusters    │
         │ • Callers & Callees     │                    │ • GraphRAG Query Engine │
         │ • Blast Radius (`blast`)│                    │ • Shortest Path (`path`)│
         │ • API Skeleton (`skel`) │                    │ • God-Nodes Discovery   │
         │ • Interactive `viz`     │                    │ • Callflow HTML Diagrams│
         │ • Fast live auto-sync   │                    │ • Pre-commit / hooks    │
         └────────────┬────────────┘                    └────────────┬────────────┘
                      │                                              │
                      └──────────────────────┬───────────────────────┘
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │    graft/ + graphify-out/ (Code Maps)        │
                      └──────────────────────────────────────────────┘
```

---

## What You Get

1. **`graft/`** (local cache, auto git-ignored):
   - `.graph/wiring.json`: Full per-symbol call graph & wiring cards across 22+ languages.
   - API signatures and caller/callee relations ready for instant zero-token query.
2. **`graphify-out/`** (committed or cached):
   - `graph.json`: Full graph ready for semantic GraphRAG traversal.
   - `GRAPH_REPORT.md`: Architectural hubs, key modules, surprising connections.
   - `graph.html`: Interactive browser graph.

> **Always-on, Query-first Rule (NON-NEGOTIABLE):**
> Before locating, reading, or reasoning about code in ANY task, query the graph first
> (`graft callers`, `graft skeleton`, `graphify query`, `graphify path`) instead of grepping.
> Fall back to raw search only when the graph has no answer.

---

## 1. Quick Start & Setup

Both tools are installed on the machine:
```bash
graft --version       # @nanonets/graft v0.13+
graphify --version    # graphifyy v0.9+
```

### Build the Dual-Engine Index (First Time)
Run the bundled indexer from the repo root:
```bash
# Option A: One-command dual indexing (Graft + Graphify)
python ~/.gemini/config/skills/devcycle-index/scripts/index_codebase.py .

# Option B: Run each tool directly
graft build .                # builds graft/ wiring graph ($0, no key)
graphify . --code-only       # builds graphify-out/graph.json ($0, offline AST)
```

---

## 2. Query & Navigation Commands

### A. Graft Commands (Fast Call Graph, Blast Radius, Skeletons)
```bash
# Repo orientation (directory clusters, hubs, hotspots)
graft map

# View API signatures of a file without reading full body (90% token savings)
graft skeleton path/to/file.ts

# Who calls / references a symbol (inbound dependencies)
graft callers FunctionName
graft callers ClassName

# What a symbol calls / depends on (outbound dependencies)
graft callers FunctionName --direction out

# Transitive blast radius (depth N)
graft callers FunctionName -d 2

# Blast radius of Git changes / PR diff
graft blast --base origin/main --format markdown

# Interactive Visualizer (opens browser on localhost)
graft viz --no-open --port 5000
```

### B. Graphify Commands (GraphRAG, Paths, Communities)
```bash
# Query the architecture / concept relationships
graphify query "how does authentication flow from controller to database?"

# Find the shortest path between two modules/classes
graphify path "AuthController" "PrismaService"

# Explain a specific node and its entire connected neighborhood
graphify explain "AuthService"

# List god-nodes (architectural hubs and high-coupling hotspots)
graphify god-nodes --top 10

# Export Mermaid call-flow HTML diagrams
graphify export callflow-html
```

---

## 3. Always-On Automation (Hooks & Freshness)

The index maintains zero-drift automatically:

1. **On Project Open (Background)**:
   - `scripts/session_index.py` checks if `graft/` or `graphify-out/` is missing and launches background indexing without blocking session startup.
2. **On Every Git Commit (Pre-commit, Background)**:
   - Install non-blocking background hook:
   ```bash
   python ~/.gemini/config/skills/devcycle-index/scripts/install_precommit.py
   ```
3. **Freshness Drift Check**:
   ```bash
   graft check   # exits 0 if fresh, exits 1 if code moved ahead of graph
   ```

---

## 4. Where this fits in the DevCycle Pipeline

| DevCycle Phase | How it leverages the Dual-Engine Index |
|---|---|
| **Phase 0.5 (Index)** | Runs `index_codebase.py` to ensure `graft/` and `graphify-out/` are fresh. |
| **Phase 1 (Spec)** | Queries `graphify query` and `graft map` to ground PRD in exact existing module names. |
| **Phase 2 (Issues)** | Uses `graft callers <symbol> -d 2` and `graft blast` to calculate blast radius per slice. |
| **Phase 3 (TDD)** | Uses `graft skeleton <file>` to inspect interfaces before implementing unit tests. |
| **Phase 5 (Refine)** | Uses `graphify god-nodes` and `graft callers` to isolate high-coupling points. |
| **Phase 6 (Audit)** | Traces requirements to concrete AST symbols as proof of implementation. |

---

## 5. Liên Kết Với Các Kỹ Năng Liên Quan (Skill Ecosystem Integration)

- [devcycle](../devcycle/SKILL.md): Master orchestrator điều phối luồng phát triển dựa trên tri thức index.
- [senior-dev-pipeline](../senior-dev-pipeline/SKILL.md): Nền tảng tri thức cho giai đoạn chống ảo giác & xác minh thực tế 100%.
- [devcycle-spec](../devcycle-spec/SKILL.md): Cung cấp schema, API signatures và module maps để sinh PRD chuẩn xác.
- [devcycle-issues](../devcycle-issues/SKILL.md): Cung cấp tính toán Blast Radius (`graft callers`, `graft blast`) khi phân rã task.
- [devcycle-refine](../devcycle-refine/SKILL.md): Sử dụng `graphify god-nodes` để xác định các điểm nghẽn kiến trúc cần tái cấu trúc.
- [output-skill](../output-skill/SKILL.md): Đảm bảo báo cáo đồ thị kiến trúc và sơ đồ callflow được xuất đầy đủ không bị cắt ngắn.
