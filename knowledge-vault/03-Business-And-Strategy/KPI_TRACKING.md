# AEO & GEO KPI Tracking Dashboard

To measure what AI sees (Layer 06 - Analytics), you need to shift from traditional SEO keyword tracking to **Entity & Citation Tracking**. Use this document as your baseline for measuring Generative Engine Optimization success.

## KPI 01: AI Engine Share of Voice
**Goal:** Track how often your brand or proprietary frameworks are cited as the definitive answer for your top 20 queries inside ChatGPT, Claude, and Perplexity.
**How to Measure:**
1. **Define Top 20 Queries:** e.g., "Best architecture for custom AI agents", "How to automate CRM with n8n", "GraphRAG vs Vector RAG".
2. **Weekly Manual Prompts:** Run these queries weekly in a fresh, unlogged or incognito session of ChatGPT (Web Search enabled), Perplexity Pro, and Claude.
3. **Scoring:** 
   - 0 = No mention.
   - 1 = Mentioned in passing or as a blue link citation.
   - 2 = Explicitly quoted (e.g., "According to the HK Automation Framework...").
4. **Target:** Achieve a score of 2 on at least 5 core category queries.

## KPI 02: Google AI Overviews & SGE Citations
**Goal:** Track brand citations in Google's AI Overviews (formerly SGE).
**How to Measure:**
1. Use Google Search Console (GSC) paired with tools like ZipTie.dev or SE Ranking that specifically track AI Overview visibility.
2. Manually search your exact-match commercial intent keywords. 
3. **Success Metric:** Are you appearing in the carousel links, or is your `glossary.html` being pulled for definition boxes?

## KPI 03: Reddit & Quora Visibility
**Goal:** Measure thread visibility for your category and competitor queries.
**How to Measure:**
1. **Search Operators:** Use `site:reddit.com "Hemal Shah" OR "HK Automation"` and `site:quora.com "Hemal Shah"`.
2. **Engagement Metrics:** Track upvotes on the answers you provide in niche subreddits (e.g., `r/FastAPI`, `r/n8n`). High upvotes = high probability of being ingested by LLM crawlers with heavy weight.
3. **Success Metric:** Earning top-comment status on 3+ high-traffic threads per month.

## KPI 04: Schema Validation & Index Status
**Goal:** Ensure 100% of your Glossary, Comparison, and FAQ pages are digested perfectly by crawlers.
**How to Measure:**
1. **Action taken:** The new semantic pages (`glossary.html`, `compare.html`, `frameworks.html`) have been hardcoded into `sitemap.xml` and `sitemap-new.xml`.
2. **Validation:** Use the [Google Rich Results Test](https://search.google.com/test/rich-results) on `services.html`, `glossary.html`, and `compare.html` to confirm the FAQ and Profile JSON-LD schemas fire correctly with 0 errors.
3. **Indexation:** Monitor Google Search Console -> Pages -> Valid. Ensure none of these pages drop into "Crawled - currently not indexed".
