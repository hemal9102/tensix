# Codebase Graph Skill

A stack-agnostic, dependency-free (stdlib-only Python) skill for building and
querying a file-level import graph of a local codebase. Works with JS/JSX/TS/TSX,
Python, and PHP out of the box — mix and match in the same repo.

## Install
Drop this whole folder into your project, e.g.:

    your-project/
    ├── .agents/skills/codebase-graph/   <-- this folder (Antigravity/Claude Code style)
    │   ├── SKILL.md
    │   ├── README.md
    │   └── scripts/
    │       ├── build_graph.py
    │       └── query_graph.py

No pip install needed — pure Python 3.8+ standard library.

## Quick start
    cd your-project
    python3 .agents/skills/codebase-graph/scripts/build_graph.py --root . --out .graph
    python3 .agents/skills/codebase-graph/scripts/query_graph.py stats

See SKILL.md for the full command list and for how an AI agent (Antigravity,
Claude Code, etc.) should invoke this automatically when asked architecture
questions.

## What it does
- Scans the repo, extracts imports/requires for JS/TS/Python/PHP
- Resolves them to real files inside the repo (external packages are counted,
  not expanded)
- Detects circular dependencies
- Flags likely dead code (zero incoming internal imports, minus entrypoint
  heuristics)
- Auto-categorizes files (route/controller/service/model/component/page/
  hook/middleware/test/config/script/other) by folder convention
- Outputs JSON (machine-queryable) + Mermaid diagram + Markdown report

## What it deliberately does NOT do
- Expand external npm/pip/composer packages into their own graphs
- Track runtime call graphs (function-level, not just file-level) — that
  needs a real AST/tree-sitter pass per language; this is the fast,
  zero-dependency first layer. Extend `build_graph.py` per SKILL.md's
  "Extending" section if you need that depth for JS or PHP.
- Resolve bundler path aliases (`@/components/...`) automatically — add a
  small alias map to `resolve_js()` if your repo uses `tsconfig.json` paths.
