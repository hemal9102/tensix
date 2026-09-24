---
name: testing-and-validation-skill
description: Authors, executes, and validates unit, integration, and E2E test suites across backend APIs (Vitest/Pytest) and frontend UIs (Playwright/Cypress). Use when creating test suites, running automated tests, validating full-stack features, or debugging failing test assertions. Do NOT use for manual exploratory testing without code or infrastructure deployment.
---

# Testing & Validation Lead

Enforces automated testing standards, E2E browser automation, API contract validation, and deterministic self-healing test loops.

## 🎯 When to Use
* Authoring unit, integration, or E2E tests for new or existing features.
* Running test execution harnesses (`npm test`, `npx playwright test`, `pytest`).
* Setting up test fixtures, mock data layers, and database seed states.
* Diagnosing and repairing flaky or failing test assertions.

## ❌ When NOT to Use
* Code performance tuning without test suite involvement (use production web engineer skill).
* CI/CD infrastructure configuration without test authoring scope (use production engineering skill).

---

## 🚫 Non-Negotiable Testing Constraints
* **NEVER** delete failing test assertions or lower assertion thresholds just to make a build pass.
* **NEVER** mock the exact unit under test—mock external boundary dependencies (network, third-party APIs, DB adapters) only.
* **NEVER** write flaky tests dependent on hardcoded timeouts (`sleep(5000)`). Use deterministic wait conditions (`waitForSelector`, `await expect()`).
* **NEVER** declare a feature complete without running the target test suite and verifying a `0` exit code.

---

## 🧪 Testing Layer Architecture

| Test Level | Framework Target | Primary Scope | Execution Command |
| :--- | :--- | :--- | :--- |
| **Unit Testing** | Vitest / Jest / Pytest | Pure functions, domain logic, utilities | `npm run test:unit` / `pytest tests/unit` |
| **Integration Testing**| Vitest / Supertest | API route handlers, DB mutations, middleware | `npm run test:integration` |
| **E2E Testing** | Playwright / Cypress | Critical user flows (Auth, Checkout, Forms) | `npx playwright test` |
| **Contract Validation** | Zod / Pydantic | Request/response schema validation | `npm run typecheck` |

---

## 🔄 Self-Healing Test Debug Protocol

When a test fails, execute this deterministic resolution loop:

```
Inspect Failure Log -> Locate Root Cause -> Fix App Code (or Update Stale Test) -> Re-Run Test Suite -> Verify Zero Failures
```

1. **Extract Error Traceback:** Read un-truncated stack trace, line number, expected vs actual values.
2. **Determine Failure Origin:** Distinguish between actual code regression vs stale test expectation.
3. **Apply Fix:** Modify implementation code or test fixture. Never swallow exceptions or bypass checks.
4. **Re-Execute:** Run specific failed spec file until 100% pass rate achieved.

---

## ⚡ Grounding & Verification Protocol

Before confirming test suite completion:
1. **Run Full Test Suite:** Execute `npm test` or `npx playwright test`.
2. **Confirm Exit Code:** Verify exit code is `0` with zero skipped or failing tests.
3. **Coverage Check:** Ensure all critical user paths and edge cases have passing assertions.
