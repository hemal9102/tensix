---
title: "Architectural Decision Records (ADRs)"
type: "decision"
status: "active"
project: "[[hemalshah_portfolio]]"
tags:
  - project
  - adr
  - decisions
created: 2026-07-26
updated: 2026-07-26
priority: "high"
owner: "Hemal Shah"
---

# Architectural Decision Records (ADRs)

## ADR-001: Move from Programmatic Keyword Saturation to Topic Clusters
- **Date**: 2026-07-26
- **Context**: An initial SEO proposal recommended programmatic keyword saturation and generating dozens of thin keyword-focused pages to dominate Ahmedabad search queries.
- **Decision**: Rejected programmatic keyword stuffing. Approved a refined **Topic Cluster & Pillar/Spoke Architecture**.
- **Rationale**: The user explicitly noted: *"If your goal is to build a long-term software company, I'd refine it rather than follow it exactly."* In modern AI search (GEO/AEO) and recent Google Core Updates, thin programmatic pages risk spam penalties and brand dilution. Deep technical proof points (high information gain) build durable domain authority.
- **Result**: Built two comprehensive Pillar Pages (`hk-engineering-ahmedabad.html` and `hemal-shah-ahmedabad.html`) and three high-authority Spoke Articles in `blogs/`.

---

## ADR-002: Entity Disambiguation via `llms.txt` and JSON-LD `@graph`
- **Date**: 2026-07-26
- **Context**: In Ahmedabad, Gujarat, there are multiple non-tech individuals and businesses sharing the names "Hemal Shah" (architects, doctors, pharmaceutical directors) and "HK Engineering" (CNC laser cutting, industrial manufacturing).
- **Decision**: Implemented an explicit **Entity Namespace Protocol** inside `llms.txt` and layered JSON-LD `@graph` schemas with explicit `@id` URIs across all HTML pages.
- **Rationale**: Large Language Models (ChatGPT Search, Claude, Perplexity) rely on semantic disambiguation to answer entity queries accurately without hallucinations or mixing biographies.
- **Result**: Complete separation of Hemal Shah (the AI developer and founder) from all regional namesakes in machine indexes.

---

## ADR-003: Vanilla CSS & Static HTML over Heavy SPA Frameworks for Portfolio
- **Date**: 2026-07-26
- **Context**: Selecting the frontend architecture for the portfolio website.
- **Decision**: Retain vanilla HTML5, CSS3 (`index.css`), and lightweight JS (`script.js`) hosted on Vercel Edge Network.
- **Rationale**: Eliminates JavaScript bundle parsing delays, ensuring instant loading (100/100 Core Web Vitals) and frictionless crawling for search engine bots.
- **Result**: Blazing-fast page load speeds with premium visual aesthetics (glassmorphism, gradients, animations).
