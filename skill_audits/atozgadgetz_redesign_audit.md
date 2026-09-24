# 🛡️ Skill Quality Audit Report

**Skill Target:** `atozgadgetz_redesign`
**Overall Score:** `6 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Specific to `atozgadgetz.com`, but lacks explicit negative triggers for general WordPress/WooCommerce projects. |
| **2. Single Responsibility** | 2/2 | Focused exclusively on the website redesign and SEO preservation workflow for a specific domain. |
| **3. Token Efficiency** | 2/2 | Exceptionally concise at 38 lines, consuming minimal context tokens. |
| **4. Constraint Enforcement** | 1/2 | Contains hardcoded brand IDs, colors, and business rules, but lacks explicit negative constraint formatting (`❌ Don't`). |
| **5. Verification Loop** | 0/2 | No automated checks (e.g., HTTP 301/200 redirect verification script or sitemap diff checker) included. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Missing Automated Verification:** Lacks a programmatic step to crawl old vs. new URLs to verify zero 404 errors post-migration.
* **Unstructured Pre-Flight Checklist:** Requirements are listed as general text bullets rather than actionable verification steps.
* **Implicit Trigger Scope:** Does not explicitly state when NOT to use this skill (e.g., generic WooCommerce sites or non-WordPress projects).

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Add Negative Boundaries in YAML:** Explicitly instruct the agent NOT to load this skill for general e-commerce redesigns.
2. **Implement Automated URL & Redirect Verification:** Include a command/script (e.g., `curl` or Python script) to test permalink mappings and HTTP status codes.
3. **Format Negative Constraints:** Group rules using clear `❌ Don't` markers.

---

## 📦 Recommended 10/10 Refactored Version

```markdown
---
name: atozgadgetz-redesign
description: Standard operating procedure for redesigning the AtoZ Gadgetz WordPress/WooCommerce website (atozgadgetz.com) while preserving SEO, tracking IDs, and brand assets. Use ONLY when working on atozgadgetz.com. Do NOT use for generic WooCommerce or non-WordPress redesign tasks.
---

# AtoZ Gadgetz Website Redesign Protocol

## Strict Brand & System Constraints
- **Pixel ID**: MUST retain Facebook Pixel ID `584430773881344`.
- **Core Tagline**: MUST retain *"You deserve a Gadget Today!!"*.
- **Primary Color**: MUST preserve WooCommerce price color `#0D743B`.
- ❌ **Don't de-index** active indexed pages during cosmetic redesigns.
- ❌ **Don't alter** permalink slugs unless implementing 301 redirects.

## Execution Workflow
1. **Extract & Back Up Data**: Save brand logos, CF7 templates, legal pages, and shipping rules (Free Shipping > ₹450).
2. **Export Sitemap URLs**: Extract current live URLs via `sitemap_index.xml`.
3. **Maintain Permalinks**: Match target permalinks to source slugs, or generate 301 redirect maps.
4. **Run Verification**: Validate all URLs and tracking setup.

## Verification Protocol
```bash
# Verify permalinks and 301 redirects return valid HTTP 200/301 status
curl -s -o /dev/null -w "%{http_code}" https://atozgadgetz.com/sitemap_index.xml
```

## Checklist
- [ ] Facebook Pixel ID verified in header/footer script.
- [ ] 100% of sitemap URLs mapped with 200 OK or 301 Redirect.
- [ ] Shipping logic (Free Shipping > ₹450) re-tested in WooCommerce checkout.
```
