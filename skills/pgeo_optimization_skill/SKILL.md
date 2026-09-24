---
name: pgeo_optimization_skill
description: Implements Programmatic Generative Engine Optimization (pGEO) architectures. Use when dynamically generating thousands of SEO/GEO landing pages with rich JSON-LD schema and citable statistics. Do NOT use for single-page sites, manual blog posts, or standard non-programmatic layouts.
---

# Programmatic GEO (pGEO) Skill

Automates the generation of structured, entity-rich programmatic pages optimized for Google Search and AI Overviews (GEO).

## 1. Architectural Rules & Execution Matrix

Every programmatically generated page MUST contain three core layers:

| Layer | Requirement | Implementation |
| :--- | :--- | :--- |
| **1. Dynamic JSON-LD** | Multi-type nested schema | `FAQPage` + `LocalBusiness` + `Service` |
| **2. Information Gain** | Unique, citable data point | Calculated metric (e.g. avg salary, time-to-hire, local stat) |
| **3. Entity Trapping** | Long-tail conversational Q&A | 3–4 dynamic questions wrapped in `FAQPage` schema |

> ❌ **Constraint:** Never generate duplicate template text across programmatic routes without injecting unique variable metrics. Pages without unique statistical data points will be penalized by AI crawlers.

---

## 2. Dynamic Schema Code Blueprint (Next.js / TypeScript)
