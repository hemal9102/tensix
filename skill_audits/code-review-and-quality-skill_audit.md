# 🛡️ Skill Quality Audit Report

**Skill Target:** `code-review-and-quality-skill`
**Overall Score:** `4 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Broad description for code reviews; lacks negative trigger definitions ("when NOT to use"). |
| **2. Single Responsibility** | 0/2 | Severe scope pollution: combines static security/duplication review with copy-pasted Next.js, PHP, and Lighthouse prompt injections. |
| **3. Token Efficiency** | 1/2 | 241 lines long; over 80% of lines are identical to injected prompt blocks found in other skills. |
| **4. Constraint Enforcement** | 1/2 | Contains negative rules and performance budgets, but they conflict across backend code review vs. frontend web tuning. |
| **5. Verification Loop** | 1/2 | Calls static scan scripts (`./scripts/code-review.sh` & `./scripts/find-duplicates.sh`), but lacks exit-code verification rules. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Copy-Pasted Prompt Injections (Lines 22–240):** Duplicates identical prompt dumps ("PRODUCTION AI ENGINEERING ENHANCEMENTS" & "PRODUCTION WEB ENGINEER ENHANCEMENTS") found in unrelated skills.
* **Scope Creep:** Extends static code analysis into PHP MVC optimization, Next.js App Router rules, Hostinger hosting, and Google AdSense compliance.
* **Lack of Negative Trigger Boundaries:** Fails to specify when to avoid using this skill (e.g., architectural planning or unit test writing).

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Remove Unrelated Web Engine Prompt Injections:** Strip lines 22–240 completely.
2. **Focus Exclusively on Code Quality & Security:** Limit scope to static code review, security flaw detection, formatting, and DRY duplication checks.
3. **Add Negative Trigger Rules:** Specify in YAML frontmatter that this skill should NOT be used for web performance tuning or architectural design.
4. **Strict Script Verification Protocol:** Require running `./scripts/code-review.sh` and verifying zero security/duplication errors before approving PRs/changes.

---

## 📦 Recommended 10/10 Refactored Version

```markdown
---
name: code-review-and-quality-skill
description: Performs static code reviews, security scans (detecting hardcoded secrets/flaws), style guide enforcement, and DRY duplication checks. Use strictly for code reviews and static analysis. Do NOT use for architectural design, performance tuning, or database schema creation.
tools: [read_file, write_file, run_command]
---

# Code Review & Quality Assurance Protocol

## Core Rules
1. **Zero Secrets Policy**: ❌ Never allow hardcoded API keys, secrets, or passwords in committed code.
2. **DRY Principle**: Extract repeated code logic blocks into shared utility functions.
3. **Style Compliance**: All changes must match guidelines in `references/style-guide.md`.

## Execution Workflow
1. **Identify Changes**: Locate all new or modified source files.
2. **Reference Checklist**: Read `references/review-checklist.md` and `references/engineering-standards.md`.
3. **Run Automated Scans**:
   ```bash
   ./scripts/code-review.sh
   ./scripts/find-duplicates.sh
   ```
4. **Refactor & Fix**: Correct identified duplication, security risks, or linting errors.
5. **Generate Audit Report**: Provide a concise summary of findings.

## Verification Checklist
- [ ] `./scripts/code-review.sh` executed and passed with 0 security warnings.
- [ ] `./scripts/find-duplicates.sh` executed and verified zero duplicate code blocks.
- [ ] No hardcoded credentials or sensitive data detected.
```
