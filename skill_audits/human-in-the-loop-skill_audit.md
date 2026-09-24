# 🛡️ Skill Quality Audit Report

**Skill Target:** `human-in-the-loop-skill`
**Overall Score:** `3 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Frontmatter description describes human intervention, but lacks negative triggers (`when NOT to use`). |
| **2. Single Responsibility** | 0/2 | Severe Frankenstein anti-pattern! Combines human-in-the-loop logic with 220+ lines of copy-pasted Next.js, Lighthouse, PHP, and Web Vitals rules. |
| **3. Token Efficiency** | 1/2 | 241 lines long, of which 90% is completely irrelevant copy-pasted web performance boilerplate. |
| **4. Constraint Enforcement** | 1/2 | Basic human decision rules (A/B/C choices) exist in lines 8–11, but are completely buried under generic performance rules. |
| **5. Verification Loop** | 0/2 | References external script (`./scripts/prompt-human.sh`) and risk matrix without verifying script presence or handling fallback. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Frankenstein Context Injection (Lines 22–241):** Over 90% of this file is an injected block of web performance rules (`INJECTED OMNI-RULES FOR AUTONOMOUS PRODUCTION READINESS`, Next.js 15, bundle size caps, PHP MVC, etc.) that have zero relation to Human-in-the-Loop decision handling.
* **Dead / Unvalidated Script Dependencies (Line 15):** References `./scripts/prompt-human.sh` and `./references/risk-matrix.md` without checking if these paths exist or providing an interactive fallback mechanism.
* **Conflicting Instructions:** The skill purports to pause execution for human review, but lines 97–102 order the AI to "Execute recursively" and "Do not stop after one optimization".

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Purge Irrelevant Injected Content:** Delete lines 22–241 completely to restore focused scope on Human-in-the-Loop execution.
2. **Define Structured Decision Schema:** Standardize how multi-option decision choices (A/B/C) are presented to human developers.
3. **Add Interactive Fallback & Verification:** Replace unvalidated bash script references with fallback interactive prompt tools (`ask_question`).

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: human-in-the-loop-skill
description: Intercepts high-risk, ambiguous, or multi-branch execution phases to prompt the developer with structured A/B/C decision options. Use ONLY when encountering destructive operations, major architectural choices, or when automated recovery loops reach 3 failures. Do NOT use for standard low-risk code edits or non-blocking warnings.
tools: [ask_question]
---

## Purpose

Pause execution safely during high-risk scenarios and solicit clear, structured decision input from the developer before making changes.

---

## Execution Guardrails

### ❌ Never Do
- Never ask open-ended questions (e.g. "What should I do now?"). Always present structured choices.
- Never mutate files, drop database tables, or execute destructive commands while awaiting approval.
- Never trigger human intervention for routine non-destructive tasks.

### ✅ Always Do
- Summarize exact risk, context, and error logs before presenting options.
- Limit options to 2–4 distinct, actionable technical pathways (Options A, B, C).
- Include explicit recommendation and risk assessment for each choice.

---

## Decision Prompt Format

When triggering human intervention, present options in this standard format:

```markdown
### 🛑 Human Intervention Required

**Trigger Reason:** [High Risk Operation / 3x Auto-Fix Failure / Architectural Choice]
**Current State:** [Brief context summary]

**Option A (Recommended):** [Action description]
* *Pros/Cons:* [Impact]

**Option B:** [Alternative action]
* *Pros/Cons:* [Impact]

**Option C:** [Abort / Rollback]
```

---

## Verification & Recovery

- Parse human response and resume execution strictly down the selected pathway.
- Log human decision and rationale in the task execution trace.
```
