---
name: ai-knowledge-os
description: Architect and manage a local Markdown/Obsidian Knowledge OS, 3-tier memory hierarchy, and MCP memory layers. Use when building or organizing Obsidian vaults for AI memory. Do NOT use for general note writing, isolated code refactoring, or standard project setup without vault integration.
---

# AI Knowledge OS Architecture

## Core Execution Rules
1. **Markdown Source of Truth**: All knowledge MUST reside in plain text Markdown. Vector stores and DBs are temporary indices.
2. **3-Tier Memory Enforcement**:
   - **Layer 1 (Hot)**: Active context < 10KB.
   - **Layer 2 (Living)**: Standards, preferences, architectural rules.
   - **Layer 3 (Historical)**: Immutable logs, daily notes, past experiments.
3. **Mandatory Frontmatter**: Every created note MUST adhere to standard YAML metadata schema (`references/templates.md`).

## Workflow Protocol
1. **Analyze Request**: Determine target tier (Hot, Living, Historical) and category (Project, Skill, Knowledge, ADR).
2. **Load Reference Schemas**: Read `references/vault-schema.md` for folder structure and `references/templates.md` for schemas.
3. **Execute Vault Edit**: Create/update target Markdown files. Ensure all internal links use bi-directional WikiLinks (`[[Note Name]]`).
4. **Run Verification**: Validate note structure and YAML frontmatter formatting.

## Verification Checklist
- [ ] File contains valid YAML frontmatter header.
- [ ] No orphan files; at least 1 WikiLink back to a index/hub note.
- [ ] Correct vault folder destination used (`01_Memory`, `02_Projects`, etc.).
