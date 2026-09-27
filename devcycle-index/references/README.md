# Bundled references

These `*.md` files are copied verbatim from **graphify** and loaded on demand by
[../SKILL.md](../SKILL.md) (progressive disclosure).

- Source: https://github.com/safishamsi/graphify (branch `v8`,
  `graphify/skills/claude/references/`)
- License: MIT, © 2026 Safi Shamsi
- CLI/package: command `graphify`, PyPI package `graphifyy`

| File | Load when |
|------|-----------|
| [hooks.md](hooks.md) | installing the post-commit hook or wiring graphify into CLAUDE.md |
| [update.md](update.md) | running an incremental `--update` (re-extract only changed files) |
| [query.md](query.md) | querying the graph (`query` / `path` / `explain`) — includes vocab expansion |
| [add-watch.md](add-watch.md) | watching a folder for auto-update, or adding a URL to the corpus |
| [exports.md](exports.md) | exporting to Neo4j / SVG / GraphML / wiki, or serving the graph over MCP |

Upstream also ships `extraction-spec.md` (semantic extraction for doc/paper/image
corpora), `transcribe.md` (video/audio), and `github-and-merge.md` (PR workflow),
which are not needed to index a pure-code PySide6/Qt project.
