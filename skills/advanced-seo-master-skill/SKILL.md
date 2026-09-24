---
name: advanced-seo-master-skill
description: Optimizes web content and pages for traditional search engines (SEO), AI Search/Answer Engine Optimization (AEO/GEO), and Core Web Vitals. Use when auditing, structuring, or writing web pages to ensure search visibility and AI citation eligibility across Google, ChatGPT, Perplexity, and Claude. Do NOT use for general copy editing without search intent or for pure backend code tuning.
---

# Advanced SEO & AEO Optimization

Optimizes digital content and web pages for high search engine visibility (Google, Bing) and AI search engine discoverability and citations (Google AI Overviews, ChatGPT, Perplexity, Claude).

---

## Workflow & Execution Steps

1. **AI & Search Discoverability Audit**
   - Verify `robots.txt` explicitly allows search and AI crawlers (`GPTBot`, `PerplexityBot`, `ClaudeBot`, `Google-Extended`, `Bingbot`).
   - Check entity presence, author attributions, and freshness indicators (`Last updated` timestamps).
   - Ensure structured data schemas (`Article`, `FAQPage`, `HowTo`, `Product`, `Organization`) are present and valid.

2. **Structural Content Formatting (AEO/GEO Optimization)**
   - **TL;DR Block:** Place a concise 2–3 sentence direct answer block in a blockquote immediately following the `H1`.
   - **Definition Section:** Use an `H2` "What is [Topic]" containing a single, clear, self-contained definition sentence within the first 40–60 words.
   - **Data & Citation Density:** Incorporate statistics with cited original sources, expert quotes with credentials, and structured comparison tables.
   - **FAQ Block:** Include 4–5 self-contained Q&A entries answering specific long-tail queries. Keep each answer under 50 words.

3. **Core Web Vitals & Technical Health Validation**
   - Ensure semantic HTML5 elements are used (`<header>`, `<article>`, `<main>`, `<footer>`).
   - Verify meta title (50–60 chars) and meta description (150–160 chars) target main search intent without keyword stuffing.

---

## Directives & Negative Constraints

* ❌ **Don't keyword stuff:** Keyword packing penalizes AI search citations by ~10%. Focus on natural semantic coverage.
* ❌ **Don't meander in FAQ answers:** Every FAQ answer must stand completely alone without referencing earlier sections (e.g. avoiding "As stated above").
* ❌ **Don't leave content undated or unauthored:** Always specify author credentials and last-updated timestamps.
* ❌ **Don't gate core authoritative content:** Search crawlers and AI bots cannot parse or cite gated pages behind auth/paywalls.

---

## Verification & Grounding Loop

Before concluding the SEO/AEO optimization task:
1. Validate JSON-LD structured data with schema validation tools or syntax checkers.
2. Confirm all heading hierarchy rules (`H1` -> `H2` -> `H3`) are strictly sequential.
3. Check page word count and extractability of TL;DR and FAQ snippets against <50 word limits.
