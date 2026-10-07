# 🛡️ Skill Quality Audit Report

**Skill Target:** `memory-mcp-skill`
**Overall Score:** `4 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Clear intention for saving to MCP graph database, but lacks negative trigger criteria. |
| **2. Single Responsibility** | 0/2 | Extreme scope pollution: combines MCP memory graph sync with 200+ lines of unrelated web performance/Next.js/PHP prompt injections. |
| **3. Token Efficiency** | 1/2 | 241 lines long, but ~85% of content is irrelevant copy-pasted web engineering boilerplate. |
| **4. Constraint Enforcement** | 1/2 | MCP memory node rules (lines 10–18) are clear, but heavily diluted by conflicting generic web engineering guidelines. |
| **5. Verification Loop** | 1/2 | Mentions script exit code triggers (`exit 0`), but provides no verification query to confirm MCP nodes were saved successfully. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Frankenstein / Injected Bloat Anti-Pattern:** Lines 22–240 contain a massive, copy-pasted set of web engineering rules, Next.js directives, Lighthouse checklists, and PHP MVC optimization guidelines completely unrelated to memory MCP graph persistence.
* **Diluted Execution Logic:** The actual core logic for storing architecture rules and conventions in the MCP graph is buried in lines 10–18.
* **Missing MCP Write Verification:** No validation step exists to check if `mcp__create_nodes` or graph updates succeeded post-execution.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Purge All Unrelated Web Engineering Directives:** Delete lines 22–240 entirely to restore focus on MCP memory management.
2. **Define Strict Trigger & Exclusion Criteria:** Update frontmatter description and add negative constraints (e.g. "Do NOT use for general code refactoring, performance audits, or Next.js layout building").
3. **Enhance MCP Storage Logic & De-duplication:** Structurally define how `ArchitectureRule` and `Convention` nodes are created, updated, and related in the graph.
4. **Add Post-Write Verification Query:** Include a command/tool call to query the MCP graph after writing to confirm nodes exist.

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: memory-mcp-skill
description: Automatically pushes code changes and design decisions to a long-term Memory MCP graph database. Use ONLY when persisting architecture decisions, database schema updates, or API conventions to graph memory post-build. Do NOT use for code optimization, performance auditing, or UI design.
tools: [run_command, mcp]
---

# MCP Memory Graph Sync

Persists architectural decisions, schema changes, and codebase conventions into the MCP Knowledge Graph database.

## 1. Automated Execution Constraints

Run this skill immediately following successful test suite completion (`exit 0`).

### Node Categorization Matrix

| Git Diff Pattern | Target Node Type | Graph Attributes |
| :--- | :--- | :--- |
| `schema.prisma`, Pydantic models, SQL migrations | `ArchitectureRule` | `name`, `schema_version`, `summary` |
| API endpoints, route handlers, hooks | `Convention` | `endpoint`, `pattern`, `behavior` |

> ❌ **Constraint:** Never duplicate existing nodes. Always query the MCP graph by name before insertion; if a node exists, update its attributes instead of creating a duplicate.

---

## 2. Execution Steps

1. **Detect Changes:**
   ```bash
   git diff --name-only HEAD~1
   ```
2. **Read Node Definitions & Check Existence:**
   - Call `mcp__search_nodes` with the target entity name.
3. **Persist to Graph:**
   - If node exists: update node via `mcp__update_nodes`.
   - If node is new: call `mcp__create_nodes` and set relation `mcp__create_relations` to parent module.

---

## 3. Verification & Validation Loop

Confirm that nodes were properly registered in the MCP memory layer:

- [ ] Query MCP graph: `mcp__search_nodes` for newly written entities.
- [ ] Confirm response returns updated timestamp and matching entity ID.
- [ ] Ensure 0 orphan nodes were generated during graph updates.
```
