# 🛡️ Skill Quality Audit Report

**Skill Target:** `master-seo-toolkit`
**Overall Score:** `2 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 0/2 | Overly broad description; acts as a "magnet skill" for any query mentioning SEO without defining negative triggers. |
| **2. Single Responsibility** | 0/2 | Classic monolithic "Master Skill" anti-pattern grouping 11 distinct, complex domains together. |
| **3. Token Efficiency** | 2/2 | Very concise at 44 lines. |
| **4. Constraint Enforcement** | 0/2 | Lacks explicit execution rules, negative constraints (`❌ Don't`), decision matrices, or code examples. |
| **5. Verification Loop** | 0/2 | Provides no deterministic validation scripts, automated checks, or command-line verification steps. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Monolithic Master Skill Anti-Pattern:** Attempts to handle 11 separate specialized sub-domains (Technical SEO, AI visibility, Local SEO, Schema generation, Page speed, EEAT, Security, etc.) in a single meta-skill without clear routing boundaries.
* **Broad Magnet Description:** Description in YAML frontmatter does not define boundaries or exclusions, causing accidental triggering on targeted sub-tasks.
* **Zero Execution Constraints:** Section 2 & 3 give vibes-based summary tasks ("Map the target website's architecture", "Run through each of the 11 capabilities") without concrete rules or syntax specifications.
* **Missing Automated Verification:** No commands or scripts are provided to verify canonical tags, sitemap validity, or schema markup automatically.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Deconstruct Monolith into Specialized Skills:** Convert this master skill into an explicit orchestrator/router that delegates specific audits to dedicated sub-skills (e.g. `technical-seo-auditor`, `schema-generator`).
2. **Sharpen Frontmatter & Add Exclusions:** Clarify that this skill should only be invoked for top-level, comprehensive SEO site audits, NOT single-page schema fixes or quick robots.txt edits.
3. **Add Rigid Audit Execution Rules:** Define clear negative constraints and priority matrices for audit findings.
4. **Implement Verification Scripts:** Add bash/python command invocations (e.g., using `curl`, `lighthouse`, or schema validator CLI) to test pages deterministically.

---

## 📦 Recommended 10/10 Refactored Version
```markdown
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

```bash
# Check for missing canonical tags across HTML pages
grep -L 'rel="canonical"' public/**/*.html

# Check for duplicate H1 tags in components
grep -rn "<h1" src/ | wc -l
```

- [ ] All pages contain valid `<title>` and `<meta name="description">`.
- [ ] No indexing block (`noindex`) present on production route layouts.
- [ ] Automated linter/checker returns 0 exit code on sitemap and schema syntax.
```
