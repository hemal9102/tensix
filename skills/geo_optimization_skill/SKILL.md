---
name: geo-optimization
description: Generative Engine Optimization (GEO) skill for structuring website data and JSON-LD schemas for AI Overviews and LLM answer engines (Gemini, Perplexity, ChatGPT). Use when optimizing sites for AI search visibility. Do NOT use for traditional sitemaps, standard CSS layout styling, or database query tuning.
tools: [read_file, write_file, run_command]
---

# Generative Engine Optimization (GEO) Protocol

## Core Rules
1. **Exhaustive Schema Layering**: Inject structured JSON-LD dictionaries covering `Organization`, `LocalBusiness`, `FAQPage`, `Person`, and `SoftwareApplication`.
2. **Dense Entity Proximity**: Bind core brand entities with high-value technical context entities in JSON-LD fields.
3. ❌ **Don't hide data**: Never inject JSON-LD schema data that contradicts visible page content.
4. ❌ **Don't use invalid types**: Only use official schema.org entity types.

## Workflow Protocol
1. **Extract Business Entities**: Identify key services, products, FAQs, and brand identity.
2. **Draft JSON-LD Payload**: Generate nested `<script type="application/ld+json">` block.
3. **Inject into Web Head**: Place JSON-LD script inside HTML `<head>` tag.
4. **Validate JSON-LD Syntax**: Programmatically parse and validate JSON-LD syntax.

## Verification Checklist
- [ ] Valid JSON-LD script injected into HTML `<head>`.
- [ ] `node -e "JSON.parse(fs.readFileSync('page.html').toString().match(/<script type=\"application\/ld\+json\">([\s\S]*?)<\/script>/)[1])"` executes with exit code 0.
- [ ] Includes `FAQPage` and core entity schemas (`Organization` or `LocalBusiness`).
