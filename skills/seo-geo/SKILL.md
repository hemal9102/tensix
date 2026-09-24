---
name: seo-geo
description: Optimizes web content and technical site infrastructure for Generative Engine Optimization (GEO) and AI Search Engines (Google AI Overviews, ChatGPT Search, Perplexity, Bing Copilot). Use when auditing content for AI search visibility, optimizing passage citability, configuring robots.txt for AI crawlers, or creating llms.txt. Do NOT use for basic HTML layout or non-search technical refactoring.
---

# Generative Engine Optimization (GEO) & AI Search Specialist

Audits, structures, and optimizes web content to maximize citations, brand mentions, and passage extraction across major AI search engines.

## 🎯 When to Use
* Auditing web pages for AI search engine visibility (Google AI Overviews, ChatGPT Search, Perplexity).
* Re-formatting article passages for optimal AI citability (134–167 word answer blocks).
* Setting up `robots.txt` rules for AI crawlers (GPTBot, ClaudeBot, PerplexityBot) and generating `/llms.txt`.
* Injecting JSON-LD schema markup (`Article`, `Organization`, `Person`) for LLM entity resolution.

## ❌ When NOT to Use
* Traditional local SEO Google Business Profile optimizations (use local SEO skills).
* General code refactoring or UI component styling (use web engineering skills).

---

## 🚫 Non-Negotiable GEO Constraints
* **NEVER** rely on client-side rendering (CSR) alone for critical AI search content. AI crawlers bypass heavy JS execution—use Server-Side Rendering (SSR) or Static Pre-rendering.
* **NEVER** block primary AI search crawlers (`GPTBot`, `OAI-SearchBot`, `ClaudeBot`, `PerplexityBot`) in `robots.txt` if AI search visibility is desired.
* **NEVER** publish vague, unattributed claims. AI engines favor passage-level citability backed by hard data, primary sources, and clear entity definitions.

---

## 📊 GEO Audit Pillars & Scoring Criteria

| Pillar | Weight | Key Optimization Target | Verification Metric |
| :--- | :---: | :--- | :--- |
| **Passage Citability** | 30% | 134–167 word self-contained answer blocks with "X is..." definitions | Direct answer within first 50 words |
| **Technical & Rendering** | 25% | Server-Side Rendered (SSR) HTML, valid SSR metadata | Zero JS requirement for content rendering |
| **Crawler Access & llms.txt** | 20% | Unrestricted AI user-agents in `robots.txt`, valid `/llms.txt` file | HTTP 200 on `/llms.txt` and crawler access |
| **Entity & Structured Data** | 15% | JSON-LD (`Organization`, `Article`, `Person`, `sameAs` links) | Valid schema validation without errors |
| **Multi-Modal & Tables** | 10% | Semantic HTML tables, structured lists, optimized media | Clean HTML table / list tags present |

---

## 🤖 AI Crawler Configuration (`robots.txt`)

Ensure your `robots.txt` explicitly enables search-indexing crawlers:

```txt
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /
```

---

## 📄 `/llms.txt` Standard Template

Place at `/llms.txt` to provide explicit guidance to LLM crawlers:

```markdown
# Site Title & Core Domain
> Concise summary of the organization, core topics, and primary offerings.

## Key Resources & Documentation
- [Primary Guide Title](https://example.com/guide): Comprehensive overview of key topic.
- [API Documentation](https://example.com/docs): Technical specifications.
```

---

## ⚡ Grounding & Verification Protocol

Before declaring GEO optimization complete:
1. **SSR Content Check:** Fetch page HTML with JavaScript disabled (`curl -s <url>`) to confirm all text and metadata are fully rendered.
2. **Robots & Header Audit:** Verify `robots.txt` allows AI crawlers and HTTP response header `X-Robots-Tag` permits indexing.
3. **Structured Data Validation:** Validate JSON-LD schema using `npx schema-dts` or validator tools.
4. **Citability Report:** Generate a GEO score out of 100 with actionable passage reformatting recommendations.
