---
name: memory-mcp-skill
description: Framework for persisting durable design decisions, architectural rules, user preferences, and project gotchas across sessions into local file-based memory layers (.claude/memory and knowledge-vault/). Use after successfully implementing non-obvious architecture changes, settling design trade-offs, or establishing new project conventions. Do NOT use for transient conversation logs, temporary debug notes, or auto-generated code summaries.
---

# Long-Term Memory & Knowledge Persistence Protocol

Persist durable decisions, project constraints, and architectural context into local repository memory stores without relying on external memory servers.

---

## The 2 Storage Memory Layers

1. **Claude Session Memory Store** (`.claude/memory/*.md` + `MEMORY.md` index):
   * *Purpose*: Micro-facts, user preferences, gotchas, and cross-session constraints loaded during context initialization.
2. **Obsidian Knowledge Vault** (`knowledge-vault/`):
   * *Purpose*: Architectural Decision Records (ADRs), deep research, Map of Content (MOC) index notes, and operational runbooks.

*Note: Code structural rules belong directly in `CLAUDE.md` or `ARCHITECTURE.md` files.*

---

## 4-Step Memory Persistence Workflow

1. **Evaluate Trigger Condition**
   * Confirm code changes or decision trade-offs have passed tests and linting.
   * Classify target memory layer using the Routing Matrix below.

2. **Deduplication Audit (Mandatory)**
   * Grep target directory (`.claude/memory/` and `knowledge-vault/`) for pre-existing matching keys or note titles.
   * If existing record exists $\rightarrow$ **Update in-place** and update timestamp.
   * If new record $\rightarrow$ Create markdown file using the standard template.

3. **Format & Write Note**
   * Structure entries with explicit metadata: **Problem**, **Solution**, **Reasoning**, **Trade-offs**, **Future Improvements**.

4. **Update Index File**
   * Append a 1-line pointer entry to `MEMORY.md` or parent MOC note.

---

## Memory Routing Matrix

| Decision / Change Type | Target Destination | Format / File Pattern |
| :--- | :--- | :--- |
| **Architectural Trade-off / ADR** | `knowledge-vault/Decisions/` | `YYYY-MM-DD-<slug>.md` |
| **Project Gotcha / User Preference** | `.claude/memory/` | `<topic-slug>.md` + `MEMORY.md` |
| **Repository Layer Rule** | `CLAUDE.md` / `ARCHITECTURE.md` | Inline documentation section |

---

## Execution Rules & Constraints

* ❌ **Don't call non-existent MCP memory tools**: Rely exclusively on local file reads/writes (`.claude/memory/` and `knowledge-vault/`).
* ❌ **Don't duplicate static code docs**: Do not duplicate function signatures or directory layouts covered by `CLAUDE.md`.
* ❌ **Don't record transient state**: Never write temporary debugging logs, raw error traces, or unvalidated scratch notes into durable memory.

---

## Verification & Grounding Loop

1. **Pre-write Check**: Execute `grep_search` across memory directories to verify zero duplicate notes exist for the same topic.
2. **Post-write Check**: Verify newly written file has valid frontmatter and is referenced in `MEMORY.md` or relevant MOC note.
