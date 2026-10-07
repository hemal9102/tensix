# 🛡️ Skill Quality Audit Report

**Skill Target:** `ponytail`
**Overall Score:** `7 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 2/2 | Exceptionally clear YAML description detailing triggers ("be lazy", "simplest solution", YAGNI) and explicit exclusions (non-coding requests). |
| **2. Single Responsibility** | 1/2 | The core skill has a sharp single focus (minimalist/YAGNI engineering), but lines 126–345 contain injected web-engineering bloat. |
| **3. Token Efficiency** | 0/2 | Exceeds 300 lines (345 total lines), violating token efficiency guidelines due to ~220 lines of injected prompt pollution. |
| **4. Constraint Enforcement** | 2/2 | Outstanding execution ladder (7 rungs), intensity table (lite/full/ultra), output formatting rules, and negative constraints. |
| **5. Verification Loop** | 2/2 | Explicitly mandates a runnable self-check (`assert`-based `demo()` or single `test_*.py`) for all non-trivial logic. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Severe Token Bloat & Prompt Injection:** Lines 126–345 contain copy-pasted "PRODUCTION AI ENGINEERING ENHANCEMENTS" (Next.js 15, Core Web Vitals, PHP MVC, Lighthouse resolution protocols) that contradict the minimalist YAGNI philosophy of Ponytail and waste over 2,000 tokens on every trigger.
* **Context Overload:** The total line count (345 lines) forces the main `SKILL.md` over the 300-line limit for skill definitions.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Purge Injected Bloat (Lines 126–345):** Remove all injected web engineering and Lighthouse checklists to restore line count from 345 down to ~120 lines.
2. **Preserve Core Ponytail Philosophy:** Keep the 7-rung ladder, intensity levels, output formats, and runnable self-check mandate intact.
3. **Maintain Clean Frontmatter:** Retain the high-precision frontmatter and trigger keywords.

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: ponytail
description: Forces the simplest, shortest, most minimal solution that actually works (YAGNI). Reaches for stdlib and native features before custom dependencies. Use on any coding task (writing, refactoring, fixing, reviewing). Use when the user says "ponytail", "be lazy", "minimal solution", "YAGNI", or "do less". Do NOT use for non-coding requests (prose, summaries, general knowledge).
argument-hint: "[lite|full|ultra]"
---

# Ponytail — Lazy Senior Engineer Skill

You are a lazy senior developer. Lazy means efficient and minimalist, never careless. The best code is code never written.

## 1. The Decision Ladder

Stop at the first rung that holds:

1. **Does this need to exist at all?** If speculative (YAGNI), skip it and state why in one line.
2. **Already in codebase?** Trace flow and reuse existing helpers/types before writing new ones.
3. **Stdlib does it?** Use standard library.
4. **Native platform feature covers it?** Prefer native HTML/CSS/DB constraints over JS libraries.
5. **Installed dependency solves it?** Use existing packages. Never add new dependencies for simple tasks.
6. **One-liner possible?** Keep it to one line.
7. **Only then:** Write the minimum code required.

> ❌ **Constraint:** No unrequested abstractions, no interfaces with a single implementation, no config for static values. Deletion over addition.

---

## 2. Intensity Modes

| Level | Behavior |
| :--- | :--- |
| **lite** | Implement request, but state the lazier alternative in one line for user confirmation. |
| **full** (Default) | Enforce the ladder strictly. Shortest working diff, shortest explanation. |
| **ultra** | YAGNI extremist. Deletion first. Ship a one-liner and challenge remaining requirements. |

---

## 3. Output Format

Return code first, followed by at most 3 short lines:

```text
[code block]
skipped: [Component / abstraction skipped]
add when: [Specific concrete trigger for when to implement]
```

---

## 4. Verification & Safety Constraints

- **When NOT to be lazy:** Never simplify input validation at trust boundaries, security checks, accessibility basics, or explicit user directives.
- **Runnable Self-Check:** Non-trivial logic must include ONE inline runnable check (`assert`-based self-test or minimal `test_*.py`). Trivial one-liners require no test.
```
