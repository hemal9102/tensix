---
title: "System Architecture & Repository Matrix"
type: "system"
status: "active"
project: "[[hemalshah_portfolio]]"
tags:
  - system
  - architecture
  - vercel
created: 2026-07-26
updated: 2026-07-26
priority: "high"
owner: "Hemal Shah"
---

# System Architecture: HK Engineering & Portfolio Ecosystem

## 1. Executive Summary
This repository serves a dual purpose:
1. **Production Web Application**: The official enterprise AI consulting portfolio for Hemal Shah (HK Engineering) hosted on Vercel at `hemalshah.vercel.app`.
2. **AI Knowledge Operating System (Knowledge OS)**: The local-first Markdown source of truth governing architectural decision records (ADRs), SEO/GEO entity protocols, and automation workflows.

---

## 2. Technical Stack Matrix
- **Frontend Layer**: Vanilla HTML5, CSS3 (custom design system in `index.css`), and JavaScript (`script.js`). Zero heavy frontend framework bloat to maintain 100/100 Google PageSpeed Core Web Vitals.
- **Hosting & CDN**: Vercel Static Edge Network with strict Content Security Policy (CSP) and security headers defined in `vercel.json`.
- **AI Search & Schema Layer**: Extreme structured JSON-LD schemas (`Person`, `Organization`, `WebSite`, `FAQPage`, `Service`) injected across all root pages.
- **AI Crawler Corpus**: Explicit plaintext knowledge endpoints (`llms.txt` and `llms-full.txt`) adhering to the Entity Namespace Protocol for regional disambiguation in Ahmedabad.
- **Backend Architecture Reference**: Python, FastAPI, PostgreSQL, `pgvector`, and n8n (documented in `02_Projects/` and `blogs/`).

---

## 3. Directory & Routing Structure
```text
hemalshah/
├── 00_System/          # AI Knowledge OS system rules & personas
├── 01_Memory/          # Hot memory (session) & Living memory (standards)
├── 02_Projects/        # Active project memory graphs (ADRs, architectures)
├── 04_Knowledge/       # Domain concepts (GEO/AEO, RAG, n8n)
├── 06_Business/        # Business & local SEO dominance strategies
├── 07_AI/              # AI pipelines & MCP retrieval specs
├── 08_Life/            # Personal notes & habits
├── 09_Archive/         # Historical logs and past iterations
├── blogs/              # Technical spoke articles and case studies
├── skills/             # Antigravity / AI agent operational playbooks
├── assets/             # Optimized webp images and favicons
├── *.html              # Production web pages (Pillar & Core pages)
├── sitemap*.xml        # XML sitemaps with crawl priorities
└── vercel.json         # Edge deployment security & headers
```

---

## 4. Design & Performance Principles
- **Aesthetic Excellence**: Vibrant HSL color palettes, dark mode glassmorphism, micro-animations, and clean typography.
- **Zero CLS / Reflow**: Font preloading and strict dimension attributes on all media.
- **Semantic HTML**: Strict heading hierarchies (single `<h1>` per page) and accessible landmark tags.
