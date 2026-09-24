# 🛡️ Skill Quality Audit Report

**Skill Target:** `testing-and-validation-skill`
**Overall Score:** `3 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 0/2 | Vague description without negative triggers; bloated context causes accidental triggering on all web dev tasks. |
| **2. Single Responsibility** | 0/2 | **Severe Monolithic Anti-Pattern**: Combines E2E testing, Next.js 15, PHP MVC, Lighthouse, SEO, and bundle optimization. |
| **3. Token Efficiency** | 1/2 | 239 lines, ~80% of which is copy-pasted junk prompt injection completely unrelated to testing. |
| **4. Constraint Enforcement** | 1/2 | Large list of generic rules ("Never increase bundle size"), but lacks specific testing constraints. |
| **5. Verification Loop** | 1/2 | Mentions shell test runners (`run-tests.sh`), but lacks automated assertion verification or failure diagnostics. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Monolithic Master Skill Anti-Pattern (Lines 18–239):** Injects 220+ lines of unrelated web development rules (Next.js 15, React 19, Tailwind v4, PHP MVC, Hostinger, SEO, Lighthouse) into a testing skill.
* **Prompt Injection Junk (Lines 20–110 & 112–238):** Duplicate "Omni-rules" sections copy-pasted directly from external prompts into the skill file.
* **Vague Trigger Routing (Lines 1–5):** Lacks explicit `when NOT to use` boundaries, causing magnet-skill false positives on general code edits.

---

## 🔧 Refactoring Plan to Reach 10/10
1. Purge all 220+ lines of unrelated web framework, performance, and SEO copy-paste junk.
2. Restructure the skill strictly around integration and end-to-end (E2E) testing workflows.
3. Add explicit `when NOT to use` triggers and operational testing constraints (`❌ Don't`).

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: testing-and-validation-skill
description: Authors, executes, and debugs integration and E2E tests for backend APIs and frontend UIs using Playwright, Cypress, or Pytest. Use when writing or running test suites. Do NOT use for performance benchmarking, bundle size auditing, Next.js architecture setup, or SEO optimizations.
tools: [read_file, write_file, run_command]
---

# Integration & E2E Testing Skill

Provides a deterministic workflow for authoring, running, and self-healing integration and E2E test suites.

---

## Operational Constraints

* ❌ **DO NOT** write superficial tests that only check status codes without asserting payload structure.
* ❌ **DO NOT** leave failing test suites un-debugged; analyze stack traces and iterate until green.
* ❌ **DO NOT** hardcode environment-specific credentials or ports in test files.

---

## Execution Workflow

1. **Inspect Application State**: Identify target API endpoints, React/Vue page components, and database schemas.
2. **Draft Test Cases**:
   - For UI/E2E: Create Playwright/Cypress tests with user action flows and visible UI assertions.
   - For API/Backend: Create Pytest/Jest tests with payload schema validation and database state checks.
3. **Execute Test Pipeline**:
   ```bash
   # Run unit/integration tests
   npm test -- --selectProjects=integration
   
   # Run E2E tests
   npx playwright test
   ```
4. **Self-Healing Diagnostics Loop**:
   - If tests fail, extract stack traces and screenshot artifacts.
   - Refactor implementation or test fixtures.
   - Re-run targeted test spec until 100% passing.

---

## Verification & Output Checklist

- [ ] All new features covered by at least one integration or E2E spec.
- [ ] Test command executes cleanly with zero exit code errors (`Exit Code 0`).
- [ ] No flaky assertions relying on arbitrary `sleep()` timeouts (use element visibility waits).
```
