# 🛡️ Skill Quality Audit Report

**Skill Target:** `pgeo_optimization_skill`
**Overall Score:** `6 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Clear usage intent for programmatic SEO/GEO, but lacks explicit negative triggers and has a frontmatter name mismatch (`programmatic-geo` vs directory `pgeo_optimization_skill`). |
| **2. Single Responsibility** | 2/2 | Focused tightly on the combined domain of Programmatic SEO and Generative Engine Optimization. |
| **3. Token Efficiency** | 2/2 | Highly concise at 38 lines. |
| **4. Constraint Enforcement** | 1/2 | High-level architectural recommendations without strict execution constraints or code examples. |
| **5. Verification Loop** | 0/2 | Completely lacks automated verification commands, schema linting, or indexation checks. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **YAML Frontmatter Name Mismatch:** The directory is named `pgeo_optimization_skill`, but the frontmatter specifies `name: programmatic-geo`.
* **Missing Negative Exclusions:** Fails to define when NOT to use (e.g. static single-page sites, manual blog editing, standard landing pages).
* **Abstract Strategy Without Code Specifications:** Section 1 & 2 recommend dynamic schema injection and FAQ generation but provide no JSON-LD template, Next.js code snippet, or dataset structure.
* **No Automated Verification:** Provides no commands or scripts to validate programmatic pages against Google Schema specs or duplicate content checkers before indexing.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Align Frontmatter Name:** Update YAML `name` to match folder `pgeo_optimization_skill` (or standardize naming).
2. **Add Negative Exclusions:** Clearly state exclusions in YAML description.
3. **Add Concrete Code Blueprints:** Include exact JSON-LD schema builder templates and dynamic route logic for Next.js/Astro.
4. **Implement Deterministic Validation Checks:** Add validation scripts to verify that programmatically generated pages pass schema checks and contain required information gain fields.

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: pgeo_optimization_skill
description: Implements Programmatic Generative Engine Optimization (pGEO) architectures. Use when dynamically generating thousands of SEO/GEO landing pages with rich JSON-LD schema and citable statistics. Do NOT use for single-page sites, manual blog posts, or standard non-programmatic layouts.
---

# Programmatic GEO (pGEO) Skill

Automates the generation of structured, entity-rich programmatic pages optimized for Google Search and AI Overviews (GEO).

## 1. Architectural Rules & Execution Matrix

Every programmatically generated page MUST contain three core layers:

| Layer | Requirement | Implementation |
| :--- | :--- | :--- |
| **1. Dynamic JSON-LD** | Multi-type nested schema | `FAQPage` + `LocalBusiness` + `Service` |
| **2. Information Gain** | Unique, citable data point | Calculated metric (e.g. avg salary, time-to-hire, local stat) |
| **3. Entity Trapping** | Long-tail conversational Q&A | 3–4 dynamic questions wrapped in `FAQPage` schema |

> ❌ **Constraint:** Never generate duplicate template text across programmatic routes without injecting unique variable metrics. Pages without unique statistical data points will be penalized by AI crawlers.

---

## 2. Dynamic Schema Code Blueprint (Next.js / TypeScript)

```typescript
// lib/pgeo-schema.ts
export function generatePgeoSchema(data: { city: string; industry: string; avgSalary: string }) {
  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Service",
        "name": `${data.industry} Services in ${data.city}`,
        "provider": { "@type": "LocalBusiness", "name": "BrandName" }
      },
      {
        "@type": "FAQPage",
        "mainEntity": [{
          "@type": "Question",
          "name": `What is the average ${data.industry} compensation in ${data.city}?`,
          "acceptedAnswer": {
            "@type": "Answer",
            "text": `The average salary in ${data.city} for ${data.industry} is ${data.avgSalary}.`
          }
        }]
      }
    ]
  };
}
```

---

## 3. Verification & Validation Protocol

Run these automated verification steps after generating programmatic routes:

```bash
# Verify all programmatic HTML outputs contain JSON-LD FAQ schema
grep -rn '"@type": "FAQPage"' out/ | wc -l

# Ensure zero empty statistical placeholders exist in built pages
grep -rn "undefined" out/
```

- [ ] All programmatic routes render valid JSON-LD in `<head>`.
- [ ] No unpopulated dynamic variables (`undefined`, `null`, `[City]`) exist in output.
- [ ] Schema validation script returns 0 errors across generated batch.
```
