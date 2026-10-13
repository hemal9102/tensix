---
title: "Decision Record: 50-Competitor Outflank Architecture, TypeSafe Jev Economics & Knowledge Graph Integration"
type: "adr"
tags:
  - adr
  - decisions
  - jev-model
  - knowledge-graph
  - schema-hardening
date: 2026-10-13
status: accepted
---

# ADR: 50-Competitor Outflank Architecture & TypeSafe Jev Routing Economics

## 📋 Context
Incumbent software and marketing agencies across Ahmedabad (Sanand, Changodar, Vatva, S.G. Highway) hold legacy search visibility despite critical performance bottlenecks (up to 4,109ms main-thread CPU blocking, 2,483ms TTFB, 336-day sitemap decay). 

To outflank incumbents across search and AI answer engines without purchasing backlinks, TENSIX designed a 4-phase automated intelligence pipeline weaponizing:
1. Raw HTTP socket telemetry.
2. Google Knowledge Graph Freebase Machine IDs (`kgmid`) via Wikidata property `P646`.
3. 45–55 word high-density BERT Position 0 snippet cards.
4. TypeSafe Jev System One decision engine on OpenRouter.

## ⚖️ Decision
1. **Model & Economics**: Reject meta-router `typesafe/jev-router` (which caused expensive fallback to generative LLMs at ~$0.05/call). Standardize on `typesafe/jev-1.13` via OpenRouter `/api/alpha/decisions` for strict deterministic classification at **$0.000015/call** ($0.0008 total for 50 competitors).
2. **Entity Grounding**: Reject unanchored schema categories. Bind every service page to a verified Wikidata QID and Google Machine ID (`/m/...`) inside JSON-LD.
3. **Passage Ranking Architecture**: Place an explicit 45–55 word direct-answer definition block immediately after the hero section on all 10 service pages to target Google Featured Snippets and LLM vector RAG extraction.
4. **Real-Time Push**: Implement `push_indexing_gateway.py` to dispatch URL notifications to Google Indexing API and IndexNow upon deployment.

## 🚀 Consequences
* **Positive**:
  * 100% schema validation compliance (0 duplicate `@id` nodes across 47 JSON-LD schemas).
  * 0.0ms main-thread JavaScript blocking vs 4,109ms incumbent bloat.
  * Sub-300ms global edge TTFB.
  * Direct alignment with Google Knowledge Graph and future Agentic Experience Optimization (AXO).
* **Negative / Trade-offs**:
  * Requires strict manual or scripted validation on schema edits (`validate_schemas.py`) to prevent cross-page `@id` collisions.

---
**Related Documents**:
* [[04-Research-And-GEO/COMPETITIVE_OUTFLANK_AND_JEV_PIPELINE|Complete Outflank Specification]]
* [[00-MOC/Research-And-GEO-MOC|Research and GEO MOC]]
