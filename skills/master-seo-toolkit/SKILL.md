---
name: master-seo-toolkit
description: Orchestrates a full-site comprehensive SEO audit delegating to specialized sub-skills. Use ONLY for multi-page end-to-end SEO reviews and repository-wide audits. Do NOT use for isolated single-file edits (e.g. editing robots.txt only, generating one schema tag, or fixing a single image alt tag).
---

# Master SEO Audit Orchestrator

Orchestrates full-site SEO audits across technical, structured data, content authority, and performance domains.

## 1. Scope & Delegation Matrix

When performing a full audit, route specific file types and issues to dedicated sub-skills:

| Audit Domain | Target File / Area | Sub-Skill Delegate |
| :--- | :--- | :--- |
| **Structured Data** | `<script type="application/ld+json">` | `structured-data-validator` |
| **Technical & Metadata** | `<head>`, canonicals, `<meta>` | `technical-seo-auditor` |
| **AI / GEO Visibility** | Content structure, FAQ schema | `ai-visibility-auditor` |
| **Crawl Configuration** | `robots.txt`, `sitemap.xml`, `llms.txt` | `sitemap-validator` |

> ❌ **Constraint:** Do NOT attempt to manually rewrite schema or overhaul CSS bundle performance directly inside this orchestrator. Delegate to specialized domain scripts/sub-skills.

---

## 2. Audit Workflow & Constraints

1. **Crawl & Inspect Architecture:**
   - Scan root layout files, `sitemap.xml`, and metadata headers.
   - Verify HTTPS enforcement, `rel="canonical"` self-referencing, and single `<h1>` tag presence.

2. **Categorize Audit Findings:**
   - **Critical (P0):** Indexing blockers, missing canonicals, broken sitemaps.
   - **High (P1):** Invalid JSON-LD schema, missing open-graph tags, duplicate H1s.
   - **Medium (P2):** Missing image `alt` attributes, unoptimized heading hierarchies.

---

## 3. Verification & Validation Commands

Run these automated verification checks before certifying an SEO audit clean:
