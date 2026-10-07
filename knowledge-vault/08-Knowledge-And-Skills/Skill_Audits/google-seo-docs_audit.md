# 🛡️ Skill Quality Audit Report

**Skill Target:** `google-seo-docs`
**Overall Score:** `7 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Clear purpose description, but lacks negative triggering boundaries (`when NOT to use`). |
| **2. Single Responsibility** | 1/2 | Single core domain (SEO), but hardcodes project-specific details (`AtoZGadgets — Next.js App Router`). |
| **3. Token Efficiency** | 2/2 | Highly efficient layout at 121 lines with structured Markdown tables and bullet points. |
| **4. Constraint Enforcement** | 2/2 | Includes clear `Always Implement`, `Never Do`, and situation-mapping decision tables. |
| **5. Verification Loop** | 1/2 | Has a manual audit checklist, but lacks deterministic/scripted validation steps. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Project-Specific Hardcoding (Lines 76–96):** Hardcodes domain rules specifically for `AtoZGadgets — Next.js App Router`. Skills should be generic and adaptable to any stack/project unless designated as a project-specific skill.
* **Missing Negative Triggers:** YAML frontmatter does not define negative constraints or specify when NOT to activate this skill (e.g., when implementing programmatic sitemap submission APIs or local search engine index submission).
* **Manual-Only Verification:** Step 5 under Execution Process and the Quick Audit Checklist rely entirely on manual human verification rather than automated inspection commands (e.g. running Lighthouse CLI, `curl` check, or link checker).

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Refactor Frontmatter:** Add explicit `when to use` and `when NOT to use` rules in the description to prevent false positives.
2. **Generalize Architecture Rules:** Parameterize project framework rules instead of hardcoding `AtoZGadgets`.
3. **Automate Verification:** Add deterministic verification steps (e.g., automated URL status check script, schema validator CLI).

---

## 📦 Recommended 10/10 Refactored Version
```markdown
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
```
