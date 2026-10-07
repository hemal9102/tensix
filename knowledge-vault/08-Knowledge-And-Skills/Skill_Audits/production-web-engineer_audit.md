# 🛡️ Skill Quality Audit Report

**Skill Target:** `production-web-engineer`
**Overall Score:** `4 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 0/2 | Frontmatter description ("A senior Performance Engineer...") is vague, lacks explicit trigger keywords or slash commands, and provides no guidance on when to use or when NOT to use. Acts as a "magnet skill". |
| **2. Single Responsibility** | 1/2 | Overly broad master skill mixing Web Vitals, Next.js 15, React 19, PHP MVC, Hostinger, Lighthouse resolution, database indexing, and SEO auditing. |
| **3. Token Efficiency** | 1/2 | 228 lines total. Contains duplicate/overlapping prompt sections (lines 6–96 repeat concepts in lines 101–228). |
| **4. Constraint Enforcement** | 1/2 | Lists performance budgets (e.g. Max JS 150KB) and high-level rules, but lacks concrete code examples, decision matrices, or negative constraint pairs. |
| **5. Verification Loop** | 1/2 | Lists a text checklist ("Builds Successfully", "No TypeScript Errors"), but provides no automated build, typecheck, or lint command execution steps. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Magnet Skill Frontmatter:** The frontmatter description lacks explicit user intent triggers, risking unprompted activation on broad web-related queries.
* **Duplicated Directives:** Section 1 (lines 6–96) and Section 2 (lines 101–228) repeat identical rules for bundle limits, SEO, and auto-fixes.
* **Vibes-Based Auditing:** Lacks automated script triggers or specific CLI invocations (e.g., `npx lighthouse`, `npm run build`) to programmatically measure metrics.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Refactor YAML Frontmatter:** Add explicit trigger terms (`/web-performance`, `"audit core web vitals"`, `"optimize web app"`) and negative triggers.
2. **Deduplicate & Scope:** Consolidate repeated directives into focused sections; offload framework-specific guidelines (e.g., Next.js 15 rules) to `references/nextjs.md`.
3. **Add Deterministic Verification:** Include concrete CLI commands (`npm run build`, `npx tsc --noEmit`, `npx lighthouse`) to verify optimizations.

---

## 📦 Recommended 10/10 Refactored Version

```markdown
---
name: production-web-engineer
description: >
  Audits and optimizes web applications for Core Web Vitals, SEO, bundle size, and accessibility.
  Use when the user explicitly requests web performance optimization, bundle size reduction, Core Web Vitals auditing, or invokes /web-performance.
  Do NOT use for general feature coding or backend database refactoring.
tools: [Read, Write, Bash, PowerShell, Grep]
---

# Production Web Performance Engineer

## Core Mandate
Optimize existing web architecture for maximum speed, SEO, and accessibility without breaking working functionality or changing UI aesthetics.

---

## 1. Performance Budgets & Hard Constraints

| Metric | Budget / Limit | Enforcement Rule |
| :--- | :--- | :--- |
| **Initial JS** | ≤ 150 KB | Split bundles using dynamic imports (`next/dynamic` or `React.lazy`) |
| **Route JS** | ≤ 80 KB | Tree-shake unused dependencies |
| **Total CSS** | ≤ 40 KB | Purge unused CSS utility classes |
| **DOM Nodes** | ≤ 1500 nodes | Virtualize long lists |
| **Images (Above Fold)** | ≤ 200 KB | Modern formats (`AVIF`/`WebP`) with explicit `priority` attribute |
| **Long Tasks** | ≤ 50 ms | Yield execution to main thread |

---

## 2. Optimization Protocol

1. **Measure First:** Run baseline performance audit before touching code.
2. **Locate Bottlenecks:** Identify blocking resources, hydration mismatches, or layout thrashing.
3. **Rewrite & Improve:** Replace unoptimized components with native platform APIs or server-rendered alternatives.
4. **Verify Zero Regressions:** Ensure no SEO, accessibility, or visual UI breakage occurred.

---

## 3. Anti-Patterns & Negative Rules

* ❌ **Don't** add third-party JS libraries for simple tasks achievable in vanilla JS or CSS.
* ❌ **Don't** import Google Fonts via CSS `@import`. Use native `next/font` or `<link rel="preload">`.
* ❌ **Don't** force client-side rendering (`"use client"`) when Server Components can handle data fetching.
* ❌ **Don't** delete failing tests or ignore type errors to meet performance metrics.

---

## 4. Verification & Grounding Loop

Always run automated checks to confirm optimizations before declaring success:

```bash
# 1. Typecheck & Build
npm run build

# 2. Bundle Analysis
npx next-bundle-analyzer

# 3. Lighthouse CI Audit
npx lhci collect --url=http://localhost:3000
```
```
