---
title: "Living Memory — Stable Engineering & SEO Standards"
type: "memory"
status: "active"
project: "[[hemalshah_portfolio]]"
tags:
  - memory
  - living
  - standards
  - preferences
created: 2026-07-26
updated: 2026-07-26
priority: "high"
owner: "Hemal Shah"
---

# Living Memory (Layer 2 — Stable Standards & Preferences)

*Notice: This layer changes rarely. It defines the immutable rules, preferences, and design patterns governing all software engineering and digital marketing at HK Engineering.*

## 1. Engineering Preferences & Rules
- **Language & Frameworks**: Prefer Python 3.11+ with FastAPI for high-concurrency backend services. Prefer TypeScript / Next.js or clean vanilla HTML/JS for frontends.
- **Database Architecture**: Standardize on PostgreSQL with `pgvector` for vector embeddings and hybrid search. Never use fragmented SaaS vector databases when PostgreSQL can handle relational joins and HNSW indexes natively.
- **Workflow Automation**: Use n8n for webhook ingestion, OAuth token refresh loops, and scheduling. Use Python microservices for CPU-intensive data transformations and chunking.
- **Code Quality**: Strict typing, docstrings on public APIs, clean error handling (no silent fail blocks), and automated unit tests.

---

## 2. SEO & GEO (Generative Engine Optimization) Standards
- **Source of Truth**: All AI answer engines (ChatGPT Search, Perplexity, Claude, Google AI Overviews) must be fed structured knowledge via:
  1. Complete JSON-LD `@graph` schemas (`Person`, `Organization`, `WebSite`, `Service`, `FAQPage`).
  2. Plaintext LLM crawler files (`llms.txt` and `llms-full.txt`).
- **Entity Namespace Protocol**: Always explicitly disambiguate "Hemal Shah" (AI Developer in Navrangpura/Ahmedabad) from local namesakes in healthcare and architecture.
- **Hub & Spoke Linking**: Every technical blog post (Spoke) MUST link back to at least one core commercial service or pillar page (Hub) using descriptive, keyword-rich anchor text.

---

## 3. Communication & Execution Preferences
- **No Permission Loops**: Execute commands and file modifications autonomously once a strategic plan is approved.
- **High Information Gain**: Provide exact code, SQL queries, benchmarks, and architectural trade-offs in all documentation and blog content.
