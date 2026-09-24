---
title: "TENSIX System Architecture & Repository Matrix"
type: "system"
tags:
  - system
  - architecture
  - tensix
  - vercel
  - oci
created: 2026-09-25
updated: 2026-09-25
priority: "high"
owner: "Hemal Shah"
canonical: "https://tensix.in/"
---

# System Architecture: TENSIX Autonomous Engineering Studio

## 1. Executive Summary
This repository (`H:\portfolio_website\tensix`) operates as:
1. **Production Web Application & Productized Engineering Portal**: The official website for **TENSIX** (`https://tensix.in/`), founded and solely owned by **Hemal Shah** in Navrangpura, Ahmedabad (`23.0366° N, 72.5615° E`).
2. **AI Knowledge Operating System & Obsidian Second Brain**: The local-first Markdown source of truth governing architectural decision records (ADRs), productized service tiers, buyer personas, sales psychology, and AI discovery protocols.
3. **Autonomous AI Swarm Hub**: The central command node where Hemal Shah directs specialized autonomous AI agents (researchers, coders, validators) to build and deploy high-concurrency systems.

---

## 2. Technical Stack Matrix
- **Frontend Layer**: Vanilla HTML5, CSS3 (glassmorphic design system), and JavaScript (`script.js`). Zero heavy client-side JavaScript frameworks to maintain a perfect 100/100 Core Web Vitals rating.
- **Edge & VPS Infrastructure**: Vercel Static Edge Network with strict Content Security Policy (CSP) headers in `vercel.json` alongside Oracle Cloud Infrastructure (OCI) and Plesk Linux VPS deployment paths.
- **AI Search & Schema Layer**: Unified Schema.org JSON-LD hierarchy (`Organization`, `ProfessionalService`, `Person`, `OfferCatalog`, `GeoCoordinates`, `FAQPage`, `BreadcrumbList`) across all pages.
- **AI Crawler Endpoints**: `/llms.txt` and `/llms-full.txt` (92k+ character corpus) compiled via `regen_llms.py`.
- **Backend Architecture Reference**: Python 3.12+, FastAPI async APIs, PostgreSQL, `pgvector`, Playwright, FastMCP, and Docker.

---

## 3. Directory & Knowledge OS Structure
```text
tensix/
├── 00-MOC/              # Obsidian Map of Content navigation hubs
├── 00_System/           # System architecture rules, AI personas
├── 01_Memory/           # Hot working memory & living engineering standards
├── 02_Projects/         # Active project charters, sprint roadmaps
├── 04_Knowledge/        # Domain conceptual notes (AEO/GEO, GraphRAG, CI/CD)
├── 06_Business/         # Sales psychology, buyer personas, keyword dominance
├── 07_AI/               # FastMCP pipelines, LangGraph multi-agent specs
├── knowledge-vault/     # Obsidian Zettelkasten & PARA knowledge graph
├── assets/              # Optimized WebP assets, SVG icons, Inter fonts
├── *.html               # Production web pages (Pillars, Hubs, Case Studies)
└── *.py                 # 25+ Python automation, indexing & audit scripts
```

---

## 4. Operational & Delivery Principles
- **100% Fixed-Price Scope**: Zero surprise hourly billing.
- **Zero-Downtime Guarantee**: Seamless database migrations and DNS cutovers.
- **Complete IP Ownership**: Client holds 100% legal ownership of code and server keys from Day 1.
- **Direct Architect Access**: Work directly with Lead Architect Hemal Shah.
