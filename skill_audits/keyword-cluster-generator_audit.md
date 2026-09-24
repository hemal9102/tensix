# 🛡️ Skill Quality Audit Report

**Skill Target:** `keyword-cluster-generator`
**Overall Score:** `7 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Clear functional description, but lacks negative triggers (`when NOT to use`). |
| **2. Single Responsibility** | 2/2 | Focused exclusively on keyword clustering, topical authority, and hub-and-spoke content planning. |
| **3. Token Efficiency** | 2/2 | Compact and well-structured at 82 lines. |
| **4. Constraint Enforcement** | 1/2 | Good search intent breakdown and hub-and-spoke rules, but lacks explicit negative rules (`❌ Don't`). |
| **5. Verification Loop** | 1/2 | Includes a manual output checklist, but lacks deterministic schema/cannibalization validation tools. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Missing Negative Boundaries:** YAML frontmatter description does not specify when NOT to use this skill (e.g. for page-level meta tag auditing or search console indexing).
* **Missing Negative Rule Section:** Lacks a dedicated `❌ Never Do` section to explicitly forbid keyword stuffing, cannibalizing main pillar URLs, or overlapping search intents.
* **Manual Verification Only:** Output verification relies entirely on a manual markdown checklist rather than programmatic validation of the resulting cluster structure.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Refine Frontmatter:** Add negative trigger boundaries in description to prevent activation during general SEO audits.
2. **Add Strict Execution Constraints:** Include explicit `❌ Never Do` negative constraints (prevent cannibalization, cap cluster depth).
3. **Automate Output Validation:** Provide a schema or script validation check for generated keyword cluster JSON/Markdown output.

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: keyword-cluster-generator
description: Generates topical keyword clusters, hub-and-spoke content silos, and search intent mappings for topical authority. Use ONLY when planning keyword strategy or site content architecture. Do NOT use for meta tag editing (use google-seo-docs) or indexing requests (use indexnow).
tools: [WebFetch, Read, Write]
---

## Purpose

Design structured Hub-and-Spoke keyword clusters to build search engine topical authority and prevent keyword cannibalization.

---

## Execution Guardrails

### ❌ Never Do
- Never assign the same primary long-tail keyword or search intent to multiple cluster pages (prevents cannibalization).
- Never create more than 5 sub-clusters per single pillar topic (prevents structural bloat).
- Never generate generic URL slugs (e.g. `/page-123`).

### ✅ Always Do
- Map every target keyword to exactly 1 Search Intent category (`Informational`, `Navigational`, `Commercial`, `Transactional`).
- Enforce strict bi-directional internal linking: Spoke $\rightarrow$ Pillar, Pillar $\rightarrow$ Spoke.
- Ensure every cluster page targets a distinct sub-niche long-tail variant.

---

## Keyword Cluster Output Schema

Every generated cluster MUST adhere to the following layout:

```markdown
# Pillar Page: [Core Topic Title]
- **Target Primary Keyword:** [Broad Keyword]
- **Search Intent:** [Informational / Commercial]
- **Target URL Slug:** /[pillar-slug]

## Cluster 1: [Subtopic A Name]
- **Primary Spoke Keyword:** [Long-tail Keyword] (Intent: Informational)
- **Suggested Page Title:** [SEO Title]
- **Target URL Slug:** /[pillar-slug]/[spoke-slug]
- **Internal Link Anchor:** "[Link Text back to Pillar]"
```

---

## Output Validation Loop

- Verify output against JSON/Markdown structural checklist:
  - Pillar page defined: YES
  - Sub-clusters count: 3 to 5
  - Search intent assigned for 100% of keywords: YES
  - Zero duplicate primary keywords across spokes: VERIFIED
```
