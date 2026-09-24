# 🛡️ Skill Quality Audit Report

**Skill Target:** `debugging-api-data-extraction`
**Overall Score:** `10 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 2/2 | Description and activation section clearly specify precise triggers (silent empty UI, HTTP 200, double extraction). |
| **2. Single Responsibility** | 2/2 | Laser-focused on a single class of bugs: silent empty data extraction & wrapper envelope mismatches. |
| **3. Token Efficiency** | 2/2 | 297 lines long (under the 300-line limit), highly structured, and packed with high-signal diagnostic guidance. |
| **4. Constraint Enforcement** | 2/2 | Strict rules against guessing ("do NOT guess"), clear negative code examples (`✗` vs `✓`), and diagnostic decision matrices. |
| **5. Verification Loop** | 2/2 | Features a dedicated 6-layer protocol ending with targeted logging verification (Layer 5) and regression testing (Layer 6). |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* *None detected.* The skill strictly adheres to the 10/10 quality framework.

---

## 🔧 Refactoring Plan to Reach 10/10
* No major refactoring required! Optional future optimization: move regression test examples to `references/test-templates.md` if additional content is added to keep `SKILL.md` under 200 lines.

---

## 📦 Recommended 10/10 Refactored Version

```markdown
---
name: debugging-api-data-extraction
description: Systematic debugging process for "silent empty data" bugs — API call succeeds (HTTP 200), database has data, but UI renders empty state. Handles double-extraction bugs, swallowed fetch errors, and envelope shape mismatches across Next.js, React, FastAPI, and Express.
tools: [read_file, write_file, grep_search, run_command]
---

# Debugging API Data Extraction Bugs

## Role & Core Directives
You are a **Senior Debugging Engineer**.
- ❌ **Do NOT guess** or speculate on fixes without running the 6-layer trace protocol.
- ❌ **Do NOT blame** caching, networking, or the DB until Layers 1 & 2 are proven clean.
- ❌ **Never swallow** catch errors by returning empty fallback arrays silently.

## Activation Trigger
- UI shows empty state ("No items found") but DB contains valid records.
- API returns HTTP 200 OK but component renders zero elements.
- `?.map()` or `.filter()` returns `[]` unexpectedly without console errors.

## 6-Layer Trace Protocol
1. **Layer 1 (Backend Verification)**: Run `curl -s <endpoint> | jq '.'` to verify raw payload.
2. **Layer 2 (Network Verification)**: Confirm frontend fetch receives response; check for swallowed catch blocks.
3. **Layer 3 (Wrapper Return Shape)**: Grep for `fetchApi`/`apiClient` return statements to detect double `.data` extraction.
4. **Layer 4 (Variable Assignment Chain)**: Trace backwards from empty UI component prop to raw fetch call.
5. **Layer 5 (Log Verification)**: Add temporary `Array.isArray()` log to confirm envelope shape hypothesis.
6. **Layer 6 (Regression Test)**: Add a Vitest contract test for wrapper return shape.

## Verification Checklist
- [ ] Layer 1 curl test confirmed backend HTTP 200 payload shape.
- [ ] Checked for `.data.data` or `?.data?.data` double extraction anti-patterns via grep.
- [ ] Vitest regression test created to prevent contract regression.
```
