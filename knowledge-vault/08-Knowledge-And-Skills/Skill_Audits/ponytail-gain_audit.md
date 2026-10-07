# 🛡️ Skill Quality Audit Report

**Skill Target:** `ponytail-gain`
**Overall Score:** `4 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 2/2 | Description is specific, intent-driven, lists explicit triggers (`/ponytail-gain`, `"ponytail gain"`, etc.), and clearly specifies negative triggers ("not a persistent mode, and not a per-repo number"). |
| **2. Single Responsibility** | 0/2 | Major anti-pattern! Lines 56–275 contain injected omni-rules ("PRODUCTION AI ENGINEERING ENHANCEMENTS" and "CRITICAL: PRODUCTION WEB ENGINEER ENHANCEMENTS") covering unrelated web frameworks, PHP MVC, Next.js, and Lighthouse audits. |
| **3. Token Efficiency** | 1/2 | 275 lines total. While under 300 lines, ~80% of the content is irrelevant injected prompt bloat. |
| **4. Constraint Enforcement** | 1/2 | Contains good negative constraints for ponytail gain ("never print per-repo savings", "edits nothing"), but is contaminated by conflicting web performance constraints. |
| **5. Verification Loop** | 0/2 | Lacks deterministic validation or script-assisted checks for output formatting. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Injected Omni-Rules / Monolithic Bloat (Lines 56–275):** Over 200 lines of unrelated web optimization instructions (PHP MVC, Hostinger, LiteSpeed, Next.js 15, React 19, Tailwind CSS v4) were appended to a simple scoreboard display skill.
* **Context Window Pollution:** The injected content wastes substantial LLM context tokens every time `/ponytail-gain` is invoked.
* **Lack of Verification:** No validation rule to verify that ASCII rendering or median calculations match published benchmarks.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Strip Injected Sections:** Completely remove lines 56–275 containing the injected web engineering rules.
2. **Add Offloaded Data:** Keep benchmark numbers in a clean data table or external reference file if extended details are needed.
3. **Add Verification Loop:** Include a verification rule ensuring ASCII formatting renders cleanly in fixed-width blocks without breaking layout.

---

## 📦 Recommended 10/10 Refactored Version

```markdown
---
name: ponytail-gain
description: >
  Show ponytail's measured impact as a compact scoreboard: less code, less
  cost, more speed, from the benchmark medians. One-shot display, not a
  persistent mode, and not a per-repo number. Trigger: /ponytail-gain,
  "ponytail gain", "what does ponytail save", "show ponytail impact",
  "ponytail scoreboard".
---

# Ponytail Gain

Display this scoreboard when invoked. One-shot: do NOT change mode, write flag
files, or persist anything.

The figures are the published benchmark medians (5 everyday tasks: email
validator, debounce, CSV sum, countdown timer, rate limiter; three models:
Haiku, Sonnet, Opus). They are measured, not computed from the current repo.
Source: `benchmarks/` and the README.

## Scoreboard

Render plain ASCII bars. The bar length shows the measured range; the label
carries the exact figure:

```
  ponytail gain                     benchmark median · 5 tasks · 3 models

  Lines of code   no-skill  ████████████████████  100%
                  ponytail  ██▌·················    6–20%   ▼ 80–94%
  Cost            no-skill  ████████████████████  100%
                  ponytail  █████▌··············   23–53%  ▼ 47–77%
  Speed           ponytail  ▸ 3–6× faster

  This repo:  /ponytail-debt  (shortcuts you deferred)
              /ponytail-audit (what's still cuttable)
```

## Honesty boundary

These are benchmark medians, not this repo. NEVER print a per-repo savings
number ("you saved X lines/tokens here"): the unbuilt version was never
written, so there is no real baseline to subtract from in a live repo. The
only real per-repo figures come from `/ponytail-debt` (a counted ledger), and
this card points there instead of inventing one.

## Boundaries

One-shot display. Edits nothing, changes no mode.
"stop ponytail" or "normal mode": revert.

## Verification

Before rendering, ensure the ASCII block preserves fixed-width alignment and no dynamic numbers are computed for the current repository.
```
