#!/usr/bin/env python3
"""
build_graph.py — builds a file-level import/dependency graph for a local codebase.

Zero third-party dependencies (stdlib only), so it runs anywhere Python 3.8+ runs.

Usage:
    python3 build_graph.py --root . --out .graph
    python3 build_graph.py --root . --out .graph --incremental
"""

import argparse
import ast
import json
import os
import re
import sys
import time
from collections import defaultdict

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

IGNORE_DIRS = {
    "node_modules", ".git", ".next", "dist", "build", "__pycache__",
    ".venv", "venv", ".graph", "coverage", ".turbo", "vendor",
    ".cache", "out", "target",
}

JS_EXTS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}
PY_EXTS = {".py"}
PHP_EXTS = {".php"}
ALL_TRACKED_EXTS = JS_EXTS | PY_EXTS | PHP_EXTS

# (pattern list, folder/name hints) -> category. Checked top to bottom, first match wins.
CATEGORY_RULES = [
    ("test", re.compile(r"(\.test\.|\.spec\.|__tests__|/tests?/)", re.I)),
    ("route", re.compile(r"(/routes?/|/api/|/pages/api/)", re.I)),
    ("controller", re.compile(r"(/controllers?/)", re.I)),
    ("middleware", re.compile(r"(/middlewares?/)", re.I)),
    ("service", re.compile(r"(/services?/)", re.I)),
    ("model", re.compile(r"(/models?/|schema\.prisma$)", re.I)),
    ("hook", re.compile(r"(/hooks?/|^use[A-Z])", re.I)),
    ("component", re.compile(r"(/components?/)", re.I)),
    ("page", re.compile(r"(/pages/|/app/.*page\.[jt]sx?$)", re.I)),
    ("config", re.compile(r"(config|\.env|tsconfig|next\.config|webpack)", re.I)),
    ("script", re.compile(r"(/scripts?/)", re.I)),
]


def categorize(rel_path: str) -> str:
    for label, pattern in CATEGORY_RULES:
        if pattern.search(rel_path):
            return label
    return "other"


# ----------------------------------------------------------------------------
# Import extraction per language
# ----------------------------------------------------------------------------

JS_IMPORT_RE = re.compile(
    r"""(?:
        import\s+(?:[\w*{}\s,]+\s+from\s+)?['"]([^'"]+)['"]   # import X from '...'
        |require\(\s*['"]([^'"]+)['"]\s*\)                    # require('...')
        |export\s+(?:[\w*{}\s,]+\s+from\s+)?['"]([^'"]+)['"]  # export ... from '...'
        |import\(\s*['"]([^'"]+)['"]\s*\)                     # dynamic import('...')
    )""",
    re.VERBOSE,
)


def extract_imports_js(content: str):
    raw = []
    for m in JS_IMPORT_RE.finditer(content):
        target = next(g for g in m.groups() if g)
        raw.append(target)
    return raw


def extract_imports_py(content: str, filepath: str):
    raw = []
    try:
        tree = ast.parse(content, filename=filepath)
    except SyntaxError:
        return raw
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                raw.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            dots = "." * (node.level or 0)
            mod = node.module or ""
            raw.append(f"{dots}{mod}")
    return raw


PHP_IMPORT_RE = re.compile(
    r"""(?:require|require_once|include|include_once)\s*\(?\s*(?:__DIR__|dirname\(__FILE__\))?\s*\.?\s*['"]([^'"]+)['"]""",
)

HTML_SCRIPT_RE = re.compile(
    r"""<script\s+[^>]*src=['"]([^'"]+)['"]""",
    re.I,
)


def extract_imports_php(content: str):
    php_imports = [m.lstrip("/\\") for m in PHP_IMPORT_RE.findall(content)]
    script_imports = [m.split("?")[0].lstrip("/\\") for m in HTML_SCRIPT_RE.findall(content) if not m.startswith("http")]
    return php_imports + script_imports


LANGUAGE_EXTRACTORS = {
    **{ext: ("js", extract_imports_js) for ext in JS_EXTS},
    **{ext: ("py", extract_imports_py) for ext in PY_EXTS},
    **{ext: ("php", extract_imports_php) for ext in PHP_EXTS},
}


# ----------------------------------------------------------------------------
# Resolution: raw import string -> actual file in repo (or None if external)
# ----------------------------------------------------------------------------

def build_file_index(all_files, root):
    """Map every possible resolvable key (no-ext path, with common suffixes) to real file."""
    index = {}
    for f in all_files:
        rel = os.path.relpath(f, root)
        no_ext, _ = os.path.splitext(rel)
        keys = {rel, no_ext, no_ext.replace(os.sep, "/"), rel.replace(os.sep, "/")}
        # index.js / index.ts style folder imports
        base = os.path.basename(no_ext)
        if base == "index":
            folder = os.path.dirname(no_ext)
            keys.add(folder)
            keys.add(folder.replace(os.sep, "/"))
        for k in keys:
            index[k] = f
    return index


def resolve_js(current_file, raw, root, file_index):
    if not raw.startswith("."):
        return None  # bare specifier -> external package (or path alias we don't resolve here)
    base_dir = os.path.dirname(current_file)
    candidate = os.path.normpath(os.path.join(base_dir, raw))
    rel_candidate = os.path.relpath(candidate, root).replace(os.sep, "/")
    for suffix_key in (rel_candidate, rel_candidate):
        if suffix_key in file_index:
            return file_index[suffix_key]
    # try with extensions / index files already covered by file_index keys
    return None


def resolve_py(current_file, raw, root, file_index):
    if raw.startswith("."):
        # relative import
        base_dir = os.path.dirname(current_file)
        dots = len(raw) - len(raw.lstrip("."))
        mod = raw[dots:]
        up_dir = base_dir
        for _ in range(dots - 1):
            up_dir = os.path.dirname(up_dir)
        candidate = os.path.normpath(os.path.join(up_dir, mod.replace(".", os.sep)))
        rel_candidate = os.path.relpath(candidate, root).replace(os.sep, "/")
        return file_index.get(rel_candidate)
    else:
        # absolute import — only resolve if it maps to a top-level module in this repo
        candidate = raw.replace(".", "/")
        return file_index.get(candidate)


def resolve_php(current_file, raw, root, file_index):
    base_dir = os.path.dirname(current_file)
    candidate = os.path.normpath(os.path.join(base_dir, raw))
    rel_candidate = os.path.relpath(candidate, root).replace(os.sep, "/")
    if rel_candidate in file_index:
        return file_index[rel_candidate]
    raw_rel = raw.lstrip("/\\").replace(os.sep, "/")
    return file_index.get(raw_rel)


RESOLVERS = {"js": resolve_js, "py": resolve_py, "php": resolve_php}


# ----------------------------------------------------------------------------
# Walk repo
# ----------------------------------------------------------------------------

def walk_repo(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".")]
        for fn in filenames:
            ext = os.path.splitext(fn)[1]
            if ext in ALL_TRACKED_EXTS:
                files.append(os.path.join(dirpath, fn))
    return files


# ----------------------------------------------------------------------------
# Cycle detection (DFS-based, on internal edges only)
# ----------------------------------------------------------------------------

def find_cycles(adj):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(int)
    cycles = []
    path_stack = []

    def dfs(node):
        color[node] = GRAY
        path_stack.append(node)
        for nxt in adj.get(node, []):
            if color[nxt] == GRAY:
                idx = path_stack.index(nxt)
                cycles.append(path_stack[idx:] + [nxt])
            elif color[nxt] == WHITE:
                dfs(nxt)
        path_stack.pop()
        color[node] = BLACK

    for node in list(adj.keys()):
        if color[node] == WHITE:
            dfs(node)
    # dedupe cycles (rotations of the same cycle look different otherwise)
    seen = set()
    unique = []
    for c in cycles:
        key = frozenset(c)
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique


ENTRYPOINT_HINTS = re.compile(
    r"(^|/)(index|main|app|server|_app|_document|layout|middleware)\.[a-z]+$|"
    r"/pages/|/app/.*page\.[jt]sx?$|/api/",
    re.I,
)


def find_dead_code(nodes, incoming_count):
    dead = []
    for rel, meta in nodes.items():
        if meta["category"] == "test":
            continue
        if ENTRYPOINT_HINTS.search(rel):
            continue
        if incoming_count.get(rel, 0) == 0:
            dead.append(rel)
    return sorted(dead)


# ----------------------------------------------------------------------------
# Main build
# ----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--out", default=".graph")
    parser.add_argument("--incremental", action="store_true",
                         help="(reserved) currently always does a full rebuild")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    out_dir = os.path.join(root, args.out)
    os.makedirs(out_dir, exist_ok=True)

    t0 = time.time()
    all_files = walk_repo(root)
    file_index = build_file_index(all_files, root)

    nodes = {}
    edges = []
    incoming_count = defaultdict(int)
    adj = defaultdict(list)
    external_count = defaultdict(int)

    for f in all_files:
        rel = os.path.relpath(f, root).replace(os.sep, "/")
        ext = os.path.splitext(f)[1]
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
        except OSError:
            content = ""
        loc = content.count("\n") + 1

        nodes[rel] = {
            "category": categorize(rel),
            "ext": ext,
            "loc": loc,
        }

        lang, extractor = LANGUAGE_EXTRACTORS.get(ext, (None, None))
        if not lang:
            continue

        if lang == "py":
            raw_imports = extractor(content, f)
        else:
            raw_imports = extractor(content)

        resolver = RESOLVERS[lang]
        for raw in raw_imports:
            resolved = resolver(f, raw, root, file_index)
            if resolved:
                target_rel = os.path.relpath(resolved, root).replace(os.sep, "/")
                if target_rel != rel:
                    edges.append({"from": rel, "to": target_rel, "raw": raw})
                    incoming_count[target_rel] += 1
                    adj[rel].append(target_rel)
            else:
                external_count[rel] += 1

    cycles = find_cycles(adj)
    dead_code = find_dead_code(nodes, incoming_count)

    graph = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "root": root,
        "stats": {
            "files": len(nodes),
            "edges": len(edges),
            "cycles": len(cycles),
            "dead_code_candidates": len(dead_code),
        },
        "nodes": nodes,
        "edges": edges,
    }

    with open(os.path.join(out_dir, "nodes.json"), "w") as f:
        json.dump(nodes, f, indent=2)
    with open(os.path.join(out_dir, "edges.json"), "w") as f:
        json.dump(edges, f, indent=2)
    with open(os.path.join(out_dir, "graph.json"), "w") as f:
        json.dump(graph, f, indent=2)
    with open(os.path.join(out_dir, "cycles.json"), "w") as f:
        json.dump(cycles, f, indent=2)
    with open(os.path.join(out_dir, "dead_code.json"), "w") as f:
        json.dump(dead_code, f, indent=2)

    # Mermaid diagram — category-level rollup (file-level would be unreadable)
    cat_edges = defaultdict(int)
    for e in edges:
        c1 = nodes[e["from"]]["category"]
        c2 = nodes[e["to"]]["category"]
        if c1 != c2:
            cat_edges[(c1, c2)] += 1
    mermaid_lines = ["graph TD"]
    for (c1, c2), count in sorted(cat_edges.items(), key=lambda x: -x[1]):
        mermaid_lines.append(f"    {c1} -->|{count}| {c2}")
    with open(os.path.join(out_dir, "graph.mmd"), "w") as f:
        f.write("\n".join(mermaid_lines) + "\n")

    # Human-readable report
    cat_counts = defaultdict(int)
    for meta in nodes.values():
        cat_counts[meta["category"]] += 1

    report = []
    report.append(f"# Codebase Graph Report\n")
    report.append(f"Generated: {graph['generated_at']}")
    report.append(f"Root: `{root}`\n")
    report.append(f"## Stats")
    report.append(f"- Files tracked: **{len(nodes)}**")
    report.append(f"- Internal import edges: **{len(edges)}**")
    report.append(f"- Circular dependencies found: **{len(cycles)}**")
    report.append(f"- Dead-code candidates (zero incoming edges): **{len(dead_code)}**\n")
    report.append(f"## Files by category")
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        report.append(f"- {cat}: {count}")
    if cycles:
        report.append(f"\n## Circular dependencies")
        for c in cycles[:20]:
            report.append(f"- {' -> '.join(c)}")
        if len(cycles) > 20:
            report.append(f"- ...and {len(cycles) - 20} more (see cycles.json)")
    if dead_code:
        report.append(f"\n## Dead-code candidates (top 30)")
        for d in dead_code[:30]:
            report.append(f"- {d}")
        if len(dead_code) > 30:
            report.append(f"- ...and {len(dead_code) - 30} more (see dead_code.json)")

    with open(os.path.join(out_dir, "report.md"), "w") as f:
        f.write("\n".join(report) + "\n")

    elapsed = time.time() - t0
    print(f"Graph built in {elapsed:.2f}s -> {out_dir}")
    print(f"  files={len(nodes)} edges={len(edges)} cycles={len(cycles)} dead_code={len(dead_code)}")


if __name__ == "__main__":
    main()
