# 🛡️ Skill Quality Audit Report

**Skill Target:** `live-web-search-skill`
**Overall Score:** `3 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Clear trigger description, but lacks explicit negative boundaries (`when NOT to use`). |
| **2. Single Responsibility** | 0/2 | Extreme Frankenstein anti-pattern! Combines live web searching with 220+ lines of injected Next.js, Lighthouse, PHP, and bundle-size rules. |
| **3. Token Efficiency** | 1/2 | 240 lines long, with 90% being completely irrelevant copy-pasted web engineering boilerplate. |
| **4. Constraint Enforcement** | 1/2 | Includes simple query rules in lines 8–10, but completely lacks negative constraints for web search execution. |
| **5. Verification Loop** | 0/2 | Hardcodes unverified script execution (`./scripts/test-search.sh`) without fallback to native web search tools (`search_web` / `read_url_content`). |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Frankenstein Context Injection (Lines 20–240):** Contains 220+ lines of copy-pasted web performance and Next.js engineering rules (`INJECTED OMNI-RULES FOR AUTONOMOUS PRODUCTION READINESS`), identical to `human-in-the-loop-skill`.
* **Unvalidated Bash Script Dependency (Line 13):** Hardcodes execution of `./scripts/test-search.sh`, which is non-portable (especially on Windows) and unverified.
* **Tool Mismatch:** Lists `run_command` in frontmatter while ignoring standard search tools (`search_web`, `read_url_content`).

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Purge Irrelevant Injected Content:** Strip lines 20–240 completely to restore focus strictly on live web search.
2. **Align Tools with Standard Capabilities:** Map tools to `search_web` and `read_url_content` instead of external bash scripts.
3. **Enforce Search Grounding Rules:** Add strict query optimization rules, domain whitelists/blacklists, and result verification steps.

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: live-web-search-skill
description: Fetches real-time web information, official API documentation, and live error resolutions. Use ONLY when local codebase or offline documentation lacks required information. Do NOT use for searching local code files or repository history.
tools: [search_web, read_url_content]
---

## Purpose

Retrieve up-to-date web documentation, API syntax, and library release notes via structured search queries.

---

## Query Optimization & Constraints

### ❌ Never Do
- Never pass conversational filler (e.g., "how do I fix error in Next.js").
- Never rely on unverified SEO blog posts when official documentation is available.
- Never trigger web search for symbols present in local codebase.

### ✅ Always Do
- Include exact package name, version, and error code (e.g. `Prisma migration P2025 Next.js 15`).
- Prioritize official documentation domains (e.g., `developer.mozilla.org`, `nextjs.org/docs`, `prisma.io/docs`).

---

## Standard Search Workflow

1. **Construct Targeted Query:**
   - Format: `[Technology/Package] [Exact Error Code / Topic] [Version] site:[Official Domain]`

2. **Execute Search:**
   - Call `search_web` with optimized query string.

3. **Fetch Full Documentation:**
   - Fetch authoritative URL content via `read_url_content` to verify implementation details.

---

## Verification & Grounding Loop

* Verify fetched snippets against target runtime version (e.g., confirm Next.js 15 App Router vs Page Router syntax).
* Validate that code patterns pass local syntax checking prior to deployment.
```
