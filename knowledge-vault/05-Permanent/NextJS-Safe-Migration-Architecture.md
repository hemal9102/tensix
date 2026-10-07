---
title: Next.js Safe Migration Architecture
tags: [architecture, nextjs, seo, migration]
updated: 2026-08-01
---
# Next.js Safe Migration Architecture

**Purpose:** Documenting the strict architectural rules required to migrate a live static HTML site to Next.js without losing Google indexing, crawlability, or Domain Authority.

**Summary:** Most Next.js migrations fail SEO because they switch to Client-Side Rendering (CSR) or break URL structures. We will enforce perfect 1-to-1 URL redirects and strict Static Site Generation (SSG) Server Components to ensure zero loss of equity.

## Content
When we eventually upgrade the static Python/HTML architecture to a modern Next.js framework, we must follow these unshakeable rules:

### 1. URL Preservation (1-to-1 Mapping)
- The current indexed URLs ending in `.html` (e.g., `/navrangpura.html`) must not drop into 404s.
- **Rule:** We will configure `next.config.ts` to implement strict `301 Permanent Redirects` from `/*.html` to `/*`, ensuring perfect link equity transfer.

### 2. Crawlability (Strict SSG over CSR)
- Googlebot and AI web crawlers (Perplexity, ChatGPT) require raw HTML for fast indexing.
- **Rule:** Use Next.js App Router with strict Server Components (`export const dynamic = 'force-static'`). No React Client Components (`"use client"`) will be used for primary text content or routing.

### 3. Dynamic Metadata (Replacing Python Automation)
- Currently, we use `inject_nextgen_schemas.py` to push JSON-LD (FAQPage, Organization, OfferCatalog).
- **Rule:** In Next.js, this Python script will be retired in favor of Next.js's native `generateMetadata()` API, allowing us to dynamically generate mathematically perfect schemas inside `layout.tsx` and `page.tsx` on the server before the page is served.

### 4. Verification Gate
- **Rule:** Before launching, deploy to a private Vercel staging URL. Run Screaming Frog and Lighthouse to prove canonical tags, H1s, and schema match the live site perfectly.

## Related
- [[AEO-Strategy-MOC]]
