---
name: keyword-cluster-generator
description: Strategic SEO framework for generating keyword clusters, content silos (Hub-and-Spoke model), search intent mapping, and topical authority architectures. Use when planning site content structures, mapping keyword research into article silos, or designing pillar-and-spoke strategies for organic SEO. Do NOT use for single-page copy editing, technical site audits, or non-search content outlines.
---

# Keyword Cluster & Topical Authority Generator

Build structured SEO content silos, map search intent, and design Hub-and-Spoke page architectures to establish topical authority.

---

## The Hub & Spoke Architectural Model

* **Pillar Page (Hub)**: Comprehensive, high-level guide covering the core seed topic broad keyword.
* **Cluster Pages (Spokes)**: Laser-focused articles targeting specific subtopics and long-tail keywords.
* **Bi-Directional Linking**: Every cluster page links to its parent pillar page; the pillar links out to all child cluster pages.

---

## 4-Step Clustering Workflow

1. **Seed Topic & Semantic Discovery**
   * Extract primary broad term and generate semantically relevant sub-categories (LSI terms).
   * Group related search queries by core entity rather than surface syntax.

2. **Search Intent Classification**
   Map every keyword to one of 4 intent types:
   * **Informational (I)**: Guides, tutorials, FAQs (*"how to set up smart plugs"*).
   * **Navigational (N)**: Direct brand/resource searches (*"TP-Link app download"*).
   * **Commercial (C)**: Research, reviews, comparisons (*"best smart plugs for Alexa"*).
   * **Transactional (T)**: Purchase intent (*"buy smart plug 4-pack"*).

3. **Silo Mapping & Hierarchy Design**
   * Organize keywords into distinct clusters preventing keyword cannibalization.
   * Format structure according to the standard Output Template below.

4. **Internal Link & URL Structure Specification**
   * Assign clean URL slugs (e.g., `/smart-home/best-alexa-plugs`).
   * Define anchor text patterns for bi-directional linking.

---

## Standard Cluster Output Template

```markdown
### 🌐 Pillar Page
- **Title:** [Comprehensive Pillar Page Title]
- **Target Keyword:** [Broad Seed Keyword]
- **Primary Intent:** Informational / Commercial
- **URL Slug:** `/category-name/seed-topic-guide`

### 📌 Cluster 1: [Subtopic Name]
- **Keyword 1:** [Long-tail Query] | **Intent:** [I/N/C/T] | **Slug:** `/category/slug-1`
  - *Suggested Title:* "[Title]"
  - *Secondary LSI Terms:* [Term 1, Term 2]
- **Keyword 2:** [Long-tail Query] | **Intent:** [I/N/C/T] | **Slug:** `/category/slug-2`
  - *Suggested Title:* "[Title]"

### 📌 Cluster 2: [Subtopic Name]
- **Keyword 3:** [Long-tail Query] | **Intent:** [I/N/C/T] | **Slug:** `/category/slug-3`
  - *Suggested Title:* "[Title]"

### 🔗 Internal Linking Plan
- **Spoke-to-Hub:** Anchor text "[Pillar Keyword]" linking to `/category-name/seed-topic-guide`.
- **Hub-to-Spoke:** Contextual links from Pillar sections to child Cluster URLs.
```

---

## Execution Rules & Constraints

* ❌ **Don't allow cannibalization**: Never assign identical search intents and primary keywords to two separate cluster pages. Merge overlapping keywords into a single URL.
* ❌ **Don't use dynamic/ugly slugs**: Avoid URL slugs containing parameters or IDs (e.g., `/post-123`). Enforce clean, hierarchical paths.
* ❌ **Don't create orphan clusters**: Every cluster page must explicitly map back to a parent pillar page.

---

## Verification & Grounding Loop

1. **Cannibalization Check**: Scan all generated cluster targets to ensure zero duplicate intent/keyword overlap across pages.
2. **Completeness Audit**: Confirm output contains 1 Pillar, at least 3 distinct sub-clusters, 3-5 long-tail keywords per cluster, intent tags (I, N, C, T), clean slugs, and an internal linking strategy.
