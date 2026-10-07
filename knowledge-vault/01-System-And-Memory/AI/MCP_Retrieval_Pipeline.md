---
title: "MCP Retrieval Pipeline & AI Agent Integration"
type: "ai"
status: "active"
project: "[[hemalshah_portfolio]]"
tags:
  - ai
  - mcp
  - pipeline
  - retrieval
created: 2026-07-26
updated: 2026-07-26
priority: "high"
owner: "Hemal Shah"
---

# MCP Retrieval Pipeline & AI Agent Integration

## 1. Pipeline Overview
To enable any AI assistant (Claude, ChatGPT, Cursor, Codex, Antigravity) to work seamlessly within this Knowledge OS without exceeding token limits or hallucinating architectural rules, we implement a hybrid retrieval layer.

```text
User Question / Agent Task
            │
            ▼
Memory Search (MCP / BM25 + Embeddings)
            │
            ▼
Load Priority 1: Current Task & Active Files
Load Priority 2: 00_System/ & 01_Memory/ (Rules & Personas)
Load Priority 3: 02_Projects/hemalshah_portfolio/ (Active ADRs)
Load Priority 4: 04_Knowledge/ & 03_Skills/ (Domain Concepts)
            │
            ▼
Execution & Code Synthesis
```

---

## 2. Model Context Protocol (MCP) Integration Rules
- **Markdown Authority**: All MCP servers must treat the local `.md` files in this vault as the immutable source of truth.
- **Bi-directional Linking**: When synthesizing new knowledge or ADRs, AI agents must include standard Wiki-style links (e.g., `[[Architecture]]`, `[[Enterprise_RAG_Architecture]]`) to preserve graph integrity.
- **Auto-Promotion**: Any recurring pattern or decision generated during a working session must be promoted from `01_Memory/HOT_MEMORY.md` into `02_Projects/` or `04_Knowledge/` during the review cycle.
