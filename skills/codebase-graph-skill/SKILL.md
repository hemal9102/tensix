---
name: codebase-graph-skill
description: Builds and queries internal dependency/import graphs for local codebases (JS, TS, Python, PHP). Use when analyzing blast radius ("what breaks if I change X"), finding callers/dependencies, detecting circular imports, identifying dead code, or surveying codebase architecture. Do NOT use for external vendor packages or non-code directories.
---

# Codebase Dependency Graph

Maps and queries file-level dependency relationships (`import`, `require`, `use`) across local multi-language codebases to enable deterministic impact analysis, cycle detection, and architectural queries.

---

## Directives & Boundaries

* ❌ **Do NOT parse external packages:** Analyze only internal codebase files. Exclude `node_modules`, `vendor`, `venv`, and `dist` directories.
* ❌ **Do NOT guess dependencies manually:** Use script-based parsing (`build_graph.py` / `query_graph.py`) to inspect edges and nodes deterministically.
* ❌ **Do NOT rely on stale graphs:** Always run incremental graph refreshes after major refactors before performing queries.

---

## Workflow & Execution Steps

1. **Build / Refresh Dependency Graph**
   Run graph builder to generate structural metadata:
   ```bash
   python3 scripts/build_graph.py --root . --out .graph --incremental
   ```
   *Generates `.graph/graph.json` containing nodes (files, categories, line counts) and edges (resolved imports).*

2. **Verify Graph Integrity**
   Verify graph health before executing queries:
   ```bash
   python3 scripts/query_graph.py stats
   ```

3. **Query Graph for Specific Insights**
   Execute targeted queries to answer structural questions:
   - **Impact / Blast Radius:** `python3 scripts/query_graph.py impact <path/to/file>`
   - **Callers / Inbound Edges:** `python3 scripts/query_graph.py callers <path/to/file>`
   - **Dependencies / Outbound Edges:** `python3 scripts/query_graph.py deps <path/to/file>`
   - **Dependency Paths:** `python3 scripts/query_graph.py path <source_file> <target_file>`
   - **Circular Dependency Check:** `python3 scripts/query_graph.py cycles`
   - **Unused File / Dead Code Detection:** `python3 scripts/query_graph.py dead-code`

4. **Synthesize Findings**
   Formulate responses citing exact file paths, direction of dependencies, and verified node statistics.

---

## Verification Checklist

- [ ] `.graph/graph.json` generated without fatal parser errors.
- [ ] Graph query command exits with status code 0 before presenting findings.
- [ ] Impact analysis includes all transitive dependents.
