# 🛡️ Skill Quality Audit Report

**Skill Target:** `geo_optimization_skill`
**Overall Score:** `6 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Clear trigger scope for Generative Engine Optimization (GEO), but lacks explicit negative trigger rules ("when NOT to use"). |
| **2. Single Responsibility** | 2/2 | Focused exclusively on GEO strategies and JSON-LD structured data optimization for LLMs. |
| **3. Token Efficiency** | 2/2 | Extremely token-efficient at 42 lines, keeping context overhead low. |
| **4. Constraint Enforcement** | 1/2 | Describes core strategies, but lacks strict negative constraints (`❌ Don't`) or explicit JSON-LD formatting rules. |
| **5. Verification Loop** | 0/2 | Contains no validation steps (e.g., JSON-LD schema linting script or structured data validator). |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Missing Automated Verification:** Lacks a programmatic verification step to lint injected JSON-LD scripts for valid syntax and schema types.
* **Informal Rule Definitions:** Strategies are presented as prose concepts rather than strict, actionable agent rules.
* **Undefined Negative Boundaries:** Does not explicitly state when to avoid triggering (e.g., standard CSS styling or internal database query optimization).

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Add Negative Trigger Rules:** Specify in YAML frontmatter that this skill should NOT be used for standard visual CSS work or traditional sitemap SEO.
2. **Implement JSON-LD Schema Validation:** Add an automated verification command (e.g., `npx schema-dts` or Python JSON-LD validator) to check generated scripts.
3. **Format Negative Constraints:** Introduce clear `❌ Don't` rules regarding hidden content or invalid schema types.

---

## 📦 Recommended 10/10 Refactored Version

```markdown
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
```
