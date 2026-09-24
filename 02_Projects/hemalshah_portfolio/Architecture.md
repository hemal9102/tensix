---
title: "Project Architecture: Hub & Spoke Entity Graph"
type: "project"
status: "active"
project: "[[hemalshah_portfolio]]"
tags:
  - project
  - architecture
  - seo
  - geo
created: 2026-07-26
updated: 2026-07-26
priority: "high"
owner: "Hemal Shah"
---

# Architecture: Hub & Spoke Entity Graph (`hemalshah_portfolio`)

## 1. Top-Level Entity Graph (JSON-LD & Semantic Linking)
The website is structured as a hierarchical **Hub & Spoke** model to maximize Topical Authority and Domain Information Gain without keyword stuffing.

```text
               [ Homepage (index.html) ]
                     │        │
         ┌───────────┘        └───────────┐
         ▼                                ▼
[ Commercial Pillar Hub 1 ]      [ Leadership Pillar Hub 2 ]
(hk-engineering-ahmedabad.html)  (hemal-shah-ahmedabad.html)
         ▲                                ▲
         │                                │
         ├────────────────┬───────────────┤
         ▼                ▼               ▼
   [ Spoke 1 ]      [ Spoke 2 ]     [ Spoke 3 ]
   RAG Case Study   ETL Pipeline    GEO/AEO Schema
```

---

## 2. Page-Level Architectural Roles
- **Homepage (`index.html`)**: Broad entity declaration (`Hemal Shah`, `HK Engineering`, `AI Automation Engineer Ahmedabad`). Links to all major sections and pillar pages.
- **Pillar Hub 1 (`hk-engineering-ahmedabad.html`)**: Commercial intent hub targeting enterprise AI consulting, custom software development company, and API integrations in Ahmedabad.
- **Pillar Hub 2 (`hemal-shah-ahmedabad.html`)**: Professional leadership and technical authority hub establishing Hemal Shah's developer credentials, GitHub contributions, and speaking profile.
- **Technical Spokes (`blogs/*`)**: High-information-gain deep dives providing proof of work (SQL schemas, Python scripts, latency benchmarks). Each spoke links back to both Pillar Hubs to pass internal PageRank.

---

## 3. Machine Readability Architecture (`llms.txt`)
AI crawlers bypass visual CSS/HTML and consume `llms.txt` and `llms-full.txt`.
- **Entity Namespace Protocol**: Explicitly defines regional boundary rules (e.g., distinguishing HK Engineering from manufacturing firms in Ahmedabad).
- **Full Text Corpus**: Appends the raw markdown/text of all blogs and pillar pages into `llms-full.txt` so AI models can digest and cite technical benchmarks immediately.
