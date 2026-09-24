---
name: obsidian-knowledge-manager
description: Framework for managing a private, structured Obsidian knowledge vault (`knowledge-vault/`) using PARA, Maps of Content (MOC), and Zettelkasten principles. Use when capturing long-term architectural decisions (ADRs), research synthesis, operational runbooks, or cross-cutting project knowledge. Do NOT use for editing active codebase files, creating transient notes, or duplicating static repository docs (`CLAUDE.md` / `ARCHITECTURE.md`).
---

# Obsidian Knowledge Vault Management Protocol

Maintain a private, atomic, highly-linked Markdown knowledge vault inside `knowledge-vault/` using PARA and Map of Content (MOC) architectures.

---

## Vault Architecture (`knowledge-vault/`)

```
knowledge-vault/
├── 00-MOC/        # Maps of Content (Navigation hubs / Indices)
├── Projects/      # Active, outcome-bound initiatives
├── Areas/         # Ongoing responsibilities (SEO, Security, Infra)
├── Resources/     # Reference material, research, runbooks
├── Permanent/     # Atomic Zettelkasten notes (1 concept per note)
├── Decisions/     # Architectural Decision Records (ADRs)
└── Archive/       # Superseded or completed notes (Never deleted)
```

---

## 5-Step Vault Management Workflow

1. **Deduplication Audit (Search First)**
   * Run `grep_search` across `knowledge-vault/` to check for existing notes on the topic.
   * If found $\rightarrow$ **Update note in-place** and bump `updated: YYYY-MM-DD`.

2. **Select Category & Atomic Title**
   * Assign folder by PARA classification.
   * Use descriptive Title Case filenames (e.g., `Session-Fingerprint-Binding.md`, `2026-07-30-redis-caching-adr.md`).

3. **Populate Standard Note Template**
   * Apply strict frontmatter and required sections (Purpose, Summary, Content, Related, References).

4. **Bi-Directional Link Insertion**
   * Connect note to at least 1 parent MOC (`[[00-MOC/Topic-MOC]]`) and related notes (`[[Related-Note]]`).
   * Add relative file links to canonical repository docs (e.g. `[ARCHITECTURE.md](../../ARCHITECTURE.md)`).

5. **Tag & Categorize**
   * Apply tags from standard taxonomy: `#architecture #database #security #performance #seo #deploy #infra #research #decision #runbook`.

---

## Standard Note Template

```markdown
---
title: <Descriptive Title>
tags: [architecture, security]
updated: YYYY-MM-DD
---

# <Descriptive Title>

**Purpose:** [One sentence explaining why this note exists]

**Summary:** [2–3 actionable sentences summarizing key takeaways]

## Content
[Structured knowledge, reasoning, problem, solution, and trade-offs]

## Related Links
- [[00-MOC/Main-Topic-MOC]]
- [[Related-Atomic-Note]]
- Repo Reference: [ARCHITECTURE.md](../../ARCHITECTURE.md)

## References
- [External URL or Issue Ticket]
```

---

## Execution Rules & Constraints

* ❌ **Don't duplicate repository documentation**: Never copy code structure or rules from `CLAUDE.md` or `ARCHITECTURE.md`. Link to them using relative paths.
* ❌ **Don't leave orphan notes**: Every note MUST link to a parent MOC or related index note.
* ❌ **Don't delete superseded knowledge**: Move retired or legacy notes to `knowledge-vault/Archive/`.
* ❌ **Don't deploy vault files**: Ensure `knowledge-vault/` remains gitignored and ignored in deployment scripts.

---

## Verification & Grounding Loop

1. **Pre-Save Audit**: Run search check to verify no redundant note exists.
2. **Quality Gate Validation**: Confirm note has frontmatter, valid tags, bi-directional `[[WikiLinks]]`, repo file links, and is linked from a parent MOC note.
