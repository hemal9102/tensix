---
name: india-seo-knowledge-engine
description: Orchestrates multiple heavily-prompted subagents to scrape long-tail keywords, company system designs, YouTube transcripts, and research papers (via Google Dorking, Reddit, Bing) to dominate SEO/GEO rankings in India. Stores output continuously in the Obsidian Knowledge Graph.
---

# India SEO & Knowledge Engine

## Core Execution Rules
1. **Multi-Agent Orchestration**: Execute this pipeline strictly using isolated, highly-prompted subagents.
2. **Phase 1: Deep Research (The Scraper Agent)**
   - **Techniques**: Google Dorking, Bing Search, Reddit scraping, Apify (if available/configured).
   - **Targets**: Long-tail keywords (PAA: People Also Ask), "How-to" queries, and Reddit AMA threads.
   - **Focus**: High-level system design, infrastructure architectures, and technical deep-dives of companies.
3. **Phase 2: Content Synthesis & Citations (The Analyst Agent)**
   - Extract raw facts, system architecture diagrams, and infrastructure choices.
   - Generate AI-ready citations linking back to original research papers, YouTube videos, and official blogs.
   - Output perfectly formatted FAQs and Blogs tailored for the Indian technical demographic (high-authority tone, fact-dense).
4. **Phase 3: Graph Looping & Storage (The Graph Agent)**
   - Ingest all extracted long-tail keywords, FAQs, and architectural facts into `C:\hk\DUMP\xnlwibae\04_Knowledge\`.
   - Update the existing Obsidian Graph with new nodes and WikiLinks.
   - Establish a continuous updating loop ("Graph Looping") as new data is scraped.

## Workflow Protocol
1. Receive target niche, company, or seed keyword from the user.
2. Spawn the **Scraper Agent** with aggressive prompt engineering for Google Dorking and deep-web extraction.
3. Spawn the **Analyst Agent** to format the data into technical SEO/GEO/AEO assets.
4. Spawn the **Graph Agent** to execute the graphing script and link the new data into the Knowledge Vault.

## ❌ Constraints
- ❌ Do NOT rely on surface-level keyword tools; aggressively use Dorking and Reddit for untapped long-tail queries.
- ❌ Do NOT generate hallucinations. Every technical blog and FAQ must cite a scraped source or research paper.
- ❌ Do NOT dump unformatted data; everything must be cleanly integrated into the Obsidian Graph.

## Verification & Grounding Loop
- [ ] Are deep-search queries (Dorking) being explicitly used?
- [ ] Is the generated content backed by AI citations and specific company architectures?
- [ ] Have the extracted FAQs and keywords been mapped into the Knowledge Vault?
