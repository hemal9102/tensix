---
name: google-seo-docs
description: Fetches and applies canonical Google Search Central SEO guidelines for audits, metadata, structured data, crawling, indexing, and internationalization. Use ONLY when auditing or implementing SEO against official Google docs. Do NOT use for automated search engine index submissions (use indexnow or gsc_instant_indexing instead).
tools: [WebFetch, WebSearch]
---

## Purpose

Use this skill to audit, implement, debug, or advise on SEO by consulting canonical Google Search Central documentation directly.

---

## Canonical Documentation Index

### Fundamentals & Crawling
- **SEO Starter Guide:** https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- **Canonicalization:** https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- **Robots.txt:** https://developers.google.com/search/docs/crawling-indexing/robots/intro
- **Sitemaps:** https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview

### E-Commerce & International
- **E-Commerce SEO:** https://developers.google.com/search/docs/specialty/ecommerce
- **International / Hreflang:** https://developers.google.com/search/docs/specialty/international

---

## Decision Matrix

| Task / Problem | Target Guide | Action |
|---|---|---|
| Duplicate URL issues | Canonicalization | Implement rel="canonical" tags |
| Ranking drop | Debug Traffic Drops | Inspect Google Search Console logs |
| Schema errors | Rich Results Guide | Validate JSON-LD structured data |

---

## Execution Constraints

### ❌ Never Do
- Never block CSS/JS assets in `robots.txt`.
- Never apply `noindex` tags to valid indexable landing pages.
- Never use duplicate `<title>` or `<h1` tags across multiple pages.

### ✅ Always Do
- Fetch live Google documentation via `WebFetch` before making architectural recommendations.
- Include structured JSON-LD data (`Product`, `Organization`, `BreadcrumbList`) where applicable.
- Verify meta tag presence and structured data compliance using verification tools.

---

## Deterministic Verification

1. Run automated markup check:
   ```bash
   npx lighthouse http://localhost:3000 --only-categories=seo --output=json
   ```
2. Verify HTTP status and canonical headers:
   ```bash
   curl -I -A "Googlebot" https://example.com/
   ```
