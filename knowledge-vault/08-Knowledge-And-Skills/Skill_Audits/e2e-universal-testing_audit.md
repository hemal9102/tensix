# 🛡️ Skill Quality Audit Report

**Skill Target:** `e2e-universal-testing`
**Overall Score:** `2 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 0/2 | Magnet skill description that triggers on virtually any query mentioning "testing", "security", "SQLi", or "auth". |
| **2. Single Responsibility** | 0/2 | Monolithic "Master Skill" anti-pattern: combines unit, API, GraphQL, E2E, mobile, security, auth, DB integration, and load testing. |
| **3. Token Efficiency** | 0/2 | Extremely bloated at 1,317 lines (>300 lines limit by 4x), causing severe context window strain on every invocation. |
| **4. Constraint Enforcement** | 1/2 | Contains execution mandates ("Always write real test code"), but rules are buried under a massive wall of code templates. |
| **5. Verification Loop** | 1/2 | Provides framework run commands (`vitest run`, `pytest`), but lacks deterministic validation script modularity. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Severe Context Window Bloat (1,317 Lines):** Consumes over 40KB of raw text tokens per invocation, degrading model performance and blowing context budgets.
* **Monolithic Master Skill Anti-Pattern:** Attempts to be a universal testing reference for TS, Python, Java, Go, PHP, Ruby, Dart, REST, GraphQL, gRPC, OWASP, SQLi, and Load testing in a single file.
* **Lack of Modular Offloading:** Fails to split code templates and stack decision tables into dedicated files under `references/` or `templates/`.
* **Zero Negative Trigger Constraints:** Lacks explicit `Do NOT use when...` guidance to prevent unwanted activation.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Deconstruct Monolith into Sub-Skills:** Split into domain-specific skills: `unit-testing`, `api-security-testing`, `e2e-playwright-testing`, and `db-integration-testing`.
2. **Offload Templates to `references/`:** Move code templates for Vitest, Pytest, Supertest, and Testcontainers out of `SKILL.md` into `references/`.
3. **Trim `SKILL.md` to Core Orchestration (<120 lines):** Maintain a slim orchestrator skill that routes tasks to offloaded references based on project tech stack.
4. **Enforce Test Execution & Verification:** Require running the appropriate test runner command (`vitest run` or `pytest`) and asserting 100% test pass rates before task completion.

---

## 📦 Recommended 10/10 Refactored Version

```markdown
---
name: e2e-universal-testing
description: Orchestrates universal end-to-end and integration testing workflows across frontend, backend, and API layers. Use when planning and executing test suites (Vitest, Pytest, Playwright). Do NOT use for basic inline code debugging or single function refactoring without test execution.
tools: [read_file, write_file, run_command]
---

# Universal E2E & Integration Testing Protocol

## Core Mandates
1. **Always Write Real Test Code**: ❌ Never return pseudocode or conversational explanations.
2. **Never Break Existing Tests**: Only add new test cases or fix broken assertions.
3. **Mandatory Security Coverage**: Security & auth routes MUST include OWASP input validation tests.

## Tech Stack Router & Reference Loading
Load appropriate stack references from `references/` based on detected project config:
- **TypeScript / React / Next.js**: Read `references/typescript-vitest-guide.md`
- **Python / FastAPI / Django**: Read `references/python-pytest-guide.md`
- **E2E Browser Testing**: Read `references/playwright-e2e-guide.md`
- **Security & OWASP Scans**: Read `references/security-owasp-guide.md`

## Workflow Protocol
1. **Detect Stack**: Inspect `package.json`, `pyproject.toml`, or directory structure.
2. **Load Stack Guide**: Read matching guide from `references/`.
3. **Write Test Suite**: Create test file under `__tests__/` or `tests/`.
4. **Execute Test Runner**: Run matching test command and verify exit code 0.

## Verification Checklist
- [ ] Test file written matching stack conventions.
- [ ] Test runner executed via CLI (`vitest run` / `pytest`).
- [ ] All new tests pass with 0 failures.
```
