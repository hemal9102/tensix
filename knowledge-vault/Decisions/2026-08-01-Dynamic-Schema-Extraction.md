---
title: Upgrade to Dynamic Schema Extraction
tags: [decision, architecture, automation]
updated: 2026-08-01
---
# Upgrade to Dynamic Schema Extraction

**Purpose:** Prevent duplicate schema penalties across the site and build massive topical authority.

**Summary:** We decided to rewrite `inject_nextgen_schemas.py` from static hardcoding to dynamic HTML parsing using BeautifulSoup. It will dynamically scrape existing `<div class="faq-card">` HTML and build unique `FAQPage` JSON-LD schemas on the fly for every single page.

## Content
Previously, `inject_nextgen_schemas.py` hardcoded the exact same `FAQPage` ("Who is Hemal Shah?") and `HowTo` schema across 50+ HTML pages. 
This is an anti-pattern. Search engines and LLMs will flag this as schema spam.

To build absolute topical authority, the Python injection script must be a **Dynamic Extractor**:
1. Scan the raw HTML for FAQ blocks.
2. Extract the `<h3>` (questions) and `<p>` (answers).
3. Generate a mathematically perfect, URL-specific `FAQPage` schema.
4. Detect the file name (e.g., `navrangpura.html` vs `services.html`) and inject specific `OfferCatalog` services.

## Related
- [[AEO-Strategy-MOC]]
- [[LLM-Schema-Architecture-No-GMB]]
