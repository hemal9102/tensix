#!/usr/bin/env python3
"""
query_graph.py — reads .graph/graph.json (produced by build_graph.py) and
answers architecture questions without re-scanning the repo.

Usage:
    python3 query_graph.py impact   <path/to/file>
    python3 query_graph.py callers  <path/to/file>
    python3 query_graph.py deps     <path/to/file>
    python3 query_graph.py path     <from/file> <to/file>
    python3 query_graph.py cycles
    python3 query_graph.py dead-code
    python3 query_graph.py category <name>
    python3 query_graph.py stats
"""

import argparse
import json
import os
import sys
from collections import defaultdict, deque


def load_graph(graph_dir):
    path = os.path.join(graph_dir, "graph.json")
    if not os.path.exists(path):
        print(f"No graph found at {path}. Run build_graph.py first.", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def build_adjacency(edges):
    forward = defaultdict(list)   # who I depend on
    reverse = defaultdict(list)   # who depends on me
    for e in edges:
        forward[e["from"]].append(e["to"])
        reverse[e["to"]].append(e["from"])
    return forward, reverse


def normalize(nodes, raw_path):
    """Allow user to pass a path with or without leading ./ and match loosely."""
    candidates = [raw_path, raw_path.lstrip("./")]
    for c in candidates:
        if c in nodes:
            return c
    # fuzzy: suffix match
    matches = [n for n in nodes if n.endswith(raw_path)]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        print(f"Ambiguous path '{raw_path}', matches:", file=sys.stderr)
        for m in matches:
            print(f"  {m}", file=sys.stderr)
        sys.exit(1)
    print(f"File not found in graph: {raw_path}", file=sys.stderr)
    sys.exit(1)


def bfs_reachable(start, adj):
    seen = {start}
    q = deque([start])
    order = []
    while q:
        cur = q.popleft()
        for nxt in adj.get(cur, []):
            if nxt not in seen:
                seen.add(nxt)
                order.append(nxt)
                q.append(nxt)
    return order


def shortest_path(start, end, adj):
    if start == end:
        return [start]
    seen = {start}
    q = deque([[start]])
    while q:
        path = q.popleft()
        cur = path[-1]
        for nxt in adj.get(cur, []):
            if nxt == end:
                return path + [nxt]
            if nxt not in seen:
                seen.add(nxt)
                q.append(path + [nxt])
    return None


def cmd_impact(graph, target):
    nodes = graph["nodes"]
    target = normalize(nodes, target)
    _, reverse = build_adjacency(graph["edges"])
    affected = bfs_reachable(target, reverse)
    print(f"Impact analysis for: {target}")
    print(f"Files that (transitively) depend on it: {len(affected)}")
    for f in affected:
        print(f"  - {f}  [{nodes[f]['category']}]")
    if not affected:
        print("  (nothing depends on this file, per the current graph)")


def cmd_callers(graph, target):
    nodes = graph["nodes"]
    target = normalize(nodes, target)
    _, reverse = build_adjacency(graph["edges"])
    callers = reverse.get(target, [])
    print(f"Direct callers/importers of: {target}")
    for c in callers:
        print(f"  - {c}  [{nodes[c]['category']}]")
    if not callers:
        print("  (none found)")


def cmd_deps(graph, target):
    nodes = graph["nodes"]
    target = normalize(nodes, target)
    forward, _ = build_adjacency(graph["edges"])
    deps = forward.get(target, [])
    print(f"Direct dependencies of: {target}")
    for d in deps:
        print(f"  - {d}  [{nodes[d]['category']}]")
    if not deps:
        print("  (none found — leaf file, or only external imports)")


def cmd_path(graph, a, b):
    nodes = graph["nodes"]
    a = normalize(nodes, a)
    b = normalize(nodes, b)
    forward, _ = build_adjacency(graph["edges"])
    path = shortest_path(a, b, forward)
    if path:
        print(" -> ".join(path))
    else:
        print(f"No import path found from {a} to {b}")


def cmd_cycles(graph, graph_dir):
    path = os.path.join(graph_dir, "cycles.json")
    with open(path) as f:
        cycles = json.load(f)
    if not cycles:
        print("No circular dependencies found.")
        return
    print(f"Found {len(cycles)} circular dependency chain(s):")
    for c in cycles:
        print("  " + " -> ".join(c))


def cmd_dead_code(graph, graph_dir):
    path = os.path.join(graph_dir, "dead_code.json")
    with open(path) as f:
        dead = json.load(f)
    if not dead:
        print("No dead-code candidates found.")
        return
    print(f"Found {len(dead)} file(s) with zero incoming internal imports:")
    for d in dead:
        print(f"  - {d}")
    print("\nNote: these are candidates only — files may be entrypoints not")
    print("covered by the heuristics, or loaded dynamically/by a bundler config.")


def cmd_category(graph, name):
    nodes = graph["nodes"]
    matches = [rel for rel, meta in nodes.items() if meta["category"] == name]
    print(f"Files in category '{name}': {len(matches)}")
    for m in sorted(matches):
        print(f"  - {m}")


def cmd_stats(graph):
    print(json.dumps(graph["stats"], indent=2))
    cat_counts = defaultdict(int)
    for meta in graph["nodes"].values():
        cat_counts[meta["category"]] += 1
    print("\nBy category:")
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=[
        "impact", "callers", "deps", "path", "cycles", "dead-code", "category", "stats"
    ])
    parser.add_argument("args", nargs="*")
    parser.add_argument("--graph-dir", default=".graph")
    parsed = parser.parse_args()

    graph_dir = os.path.abspath(parsed.graph_dir)
    graph = load_graph(graph_dir)

    if parsed.command == "impact":
        cmd_impact(graph, parsed.args[0])
    elif parsed.command == "callers":
        cmd_callers(graph, parsed.args[0])
    elif parsed.command == "deps":
        cmd_deps(graph, parsed.args[0])
    elif parsed.command == "path":
        cmd_path(graph, parsed.args[0], parsed.args[1])
    elif parsed.command == "cycles":
        cmd_cycles(graph, graph_dir)
    elif parsed.command == "dead-code":
        cmd_dead_code(graph, graph_dir)
    elif parsed.command == "category":
        cmd_category(graph, parsed.args[0])
    elif parsed.command == "stats":
        cmd_stats(graph)


if __name__ == "__main__":
    main()
