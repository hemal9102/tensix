---
name: techstack-pipeline-skill
description: Orchestrates complex, multi-step engineering tasks (feature additions, major refactors, cross-stack migrations) through a structured pipeline (Plan -> Isolate -> Claim -> Verify -> Merge). Use for multi-file or multi-role engineering tasks requiring isolated git worktrees and automated verification. Do NOT use for single-file edits, minor bug fixes, or simple Q&A.
---

# Techstack Pipeline Orchestrator

Filesystem-based protocol managing task queues, git worktrees, architectural decision records (ADRs), and stack-agnostic verification pipelines.

## 🎯 When to Use
* Tasks spanning multiple layers (e.g. API route + database schema + frontend component + test suite).
* Complex refactoring requiring strict plan-first execution and impact analysis.
* Parallel development streams requiring isolated git worktree environments.
* Tasks where automated build/test/lint verification is mandatory before merging code.

## ❌ When NOT to Use
* Single-file typo fixes, simple line changes, or standalone question answering.
* Direct production deployment without staging/worktree phases (use production-engineering skill).

---

## 🚫 Non-Negotiable Pipeline Constraints
* **NEVER** trigger full pipeline overhead for simple, single-file or single-line fixes.
* **NEVER** merge a git worktree or task branch if verification (`verify.py` or build/test suite) returns a non-zero exit code.
* **NEVER** perform un-isolated edits across concurrent tasks—always use dedicated worktrees (`git worktree`) per concurrent task.
* **NEVER** bypass writing Architectural Decision Records (ADRs) when making structural or schema changes.

---

## 🔄 5-Step Pipeline Execution Sequence

```
1. Plan Tasks -> 2. Query Impact Graph -> 3. Isolate Worktree -> 4. Execute Task -> 5. Verify & Merge
```

| Pipeline Step | Tool / Command | Core Operation | Invariant / Rule |
| :--- | :--- | :--- | :--- |
| **1. Plan Tasks** | `python3 scripts/task_queue.py add --title "<task>" --role <role>` | Break task into role-based items (`backend`, `frontend`, `database`, `testing`) | Assign clear single responsibility per task item |
| **2. Impact Analysis** | `python3 scripts/query_graph.py impact <file>` | Inspect dependency blast radius using codebase graph | Never guess affected files |
| **3. Worktree Isolation** | `python3 scripts/worktree.py create <branch-name>` | Spawn isolated git worktree directory | Prevents concurrent agent workspace conflicts |
| **4. Task Execution** | `python3 scripts/task_queue.py claim <id>` | Complete task edits inside worktree directory | Commit changes locally inside worktree |
| **5. Verification & Merge** | `python3 scripts/verify.py --root <worktree-path>` | Auto-detect stack (Node/Python/PHP/Go) & run build/test/lint | Block merge if exit code != 0 |

---

## ⚡ Grounding & Verification Protocol

Before merging any task branch into main:
1. **Execute Verification Harness:** Run `python3 scripts/verify.py --root <worktree-path>` or the stack's native build and test scripts (`npm test && npm run build`, `pytest`, etc.).
2. **Validate Exit Code:** Assert exit code is `0`. If any test, lint, or compilation error occurs, fix the errors and re-verify.
3. **Graph Refresh & Cleanup:** Remove completed worktree (`python3 scripts/worktree.py remove <branch>`) and update graph indexes.
