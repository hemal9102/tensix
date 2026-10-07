# 🛡️ Skill Quality Audit Report

**Skill Target:** `skill-evaluator`
**Overall Score:** `6 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Description clearly specifies when to use, but lacks explicit negative triggers ("when NOT to use"). |
| **2. Single Responsibility** | 2/2 | Focused strictly on skill evaluation, scoring, and refactoring. |
| **3. Token Efficiency** | 2/2 | Extremely efficient at 95 lines (<150 lines benchmark). |
| **4. Constraint Enforcement** | 1/2 | Has clear scoring rubric and template, but lacks negative constraints (`❌ Don't`) and concrete execution rules. |
| **5. Verification Loop** | 0/2 | Lacks deterministic validation steps (e.g., linting or script-based verification of generated SKILL.md files). |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Missing Negative Triggers (Lines 1–4):** Frontmatter description lacks explicit `when NOT to use` boundaries, risking mild magnet-skill triggering on general code review tasks.
* **Absence of Negative Constraints (Lines 24–52):** Rubric defines scoring criteria but omits strict operational rules (`❌ Don't parse non-SKILL.md files`, `❌ Don't guess score without rubric`).
* **Missing Automated Verification (Lines 48–52):** Pillar 5 defines verification for target skills, but the evaluator itself provides no self-verification mechanism to validate created/refactored files.

---

## 🔧 Refactoring Plan to Reach 10/10
1. Harden YAML frontmatter with strict intent routing, including explicit "when NOT to use" rules.
2. Add explicit negative constraints (`❌ Don't`) and decision boundaries in the execution directives.
3. Add a self-verification step requiring structural and markdown linting of refactored `SKILL.md` files.

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: skill-evaluator
description: Meta-skill used to audit, score, and optimize AGY agent skills against the 10/10 quality framework. Use when reviewing, rating, or refactoring SKILL.md files. Do NOT use for general code reviews, repository security audits, or non-agent markdown documentation.
---

# Skill Quality Evaluator & Benchmarker

You are an expert AI Agent Architect. Your job is to perform a rigorous quality audit on any provided `SKILL.md` file or skill architecture, identify anti-patterns, calculate a score out of 10, and provide refactored fixes.

---

## Operational Constraints

* ❌ **DO NOT** evaluate files that are not `SKILL.md` or skill definition files.
* ❌ **DO NOT** assign arbitrary scores without strictly applying the 5-Pillar Rubric.
* ❌ **DO NOT** output vague feedback; all refactoring plans must include complete, runnable 10/10 replacement code.

---

## Evaluation Workflow

1. **Analyze YAML Frontmatter & Routing Integrity**
2. **Assess Token Efficiency & Structural Scope**
3. **Check Constraint Precision & Rule Clarity**
4. **Evaluate Verification & Feedback Loops**
5. **Generate Scorecard, Refactoring Plan, and Verification Check**

---

## The 5-Pillar Grading Rubric (10 Points Total)

Score each pillar on a 0–2 point scale:

### 1. Trigger Precision (0–2 Points)
* **2 pts:** Description in YAML frontmatter is hyper-specific, intent-driven, and clearly defines *when to use* and *when NOT to use*. Zero chance of "magnet skill" false-positives.
* **1 pt:** Vague or slightly broad description; might trigger on weakly related queries.
* **0 pts:** Overly broad description (e.g., *"Handles all coding and deployment"*).

### 2. Scope & Single Responsibility (0–2 Points)
* **2 pts:** Focuses on exactly **one core domain**. Clear separation of concerns.
* **1 pt:** Covers 2 related domains, but instructions are somewhat fragmented.
* **0 pts:** Monolithic "Master Skill" anti-pattern mixing 3+ unrelated disciplines.

### 3. Token Efficiency & Architecture (0–2 Points)
* **2 pts:** Main `SKILL.md` is concise (<150 lines). Complex schemas, tables, or long scripts are offloaded to on-demand files (e.g., `references/` or `scripts/`).
* **1 pt:** Between 150–300 lines; readable but starting to bloat the context window.
* **0 pts:** Over 300 lines of wall-of-text instructions loaded on every trigger.

### 4. Constraint Enforcement (0–2 Points)
* **2 pts:** Explicit rules, negative constraints (`❌ Don't`), clean decision matrices, and concrete examples.
* **1 pt:** High-level advice without strict execution rules.
* **0 pts:** Vague "vibes-based" suggestions with no strict constraints or examples.

### 5. Verification & Grounding Loop (0–2 Points)
* **2 pts:** Includes deterministic validation steps (runs a linter, test command, build check, or script) to verify its work before declaring success.
* **1 pt:** Has a manual checklist but no automated or script-assisted validation.
* **0 pts:** Assumes output is correct without any verification or testing rules.

---

## Audit Output Template

Generate reports using this structure:

```markdown
# 🛡️ Skill Quality Audit Report

**Skill Target:** `<skill-name>`
**Overall Score:** `X / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | X/2 | [Brief justification] |
| **2. Single Responsibility** | X/2 | [Brief justification] |
| **3. Token Efficiency** | X/2 | [Brief justification] |
| **4. Constraint Enforcement** | X/2 | [Brief justification] |
| **5. Verification Loop** | X/2 | [Brief justification] |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* [List specific line numbers, bloat, ambiguous YAML, or missing constraints]

---

## 🔧 Refactoring Plan to Reach 10/10
1. [Actionable step 1]
2. [Actionable step 2]

---

## 📦 Recommended 10/10 Refactored Version
```markdown
[Provide the clean, optimized SKILL.md content here]
```
```

---

## Verification & Output Validation

Before saving the audit report:
1. Verify frontmatter YAML syntax in refactored version.
2. Confirm the refactored SKILL.md is under 150 lines.
3. Validate markdown formatting and table rendering.
```
