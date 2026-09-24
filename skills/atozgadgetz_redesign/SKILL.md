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
