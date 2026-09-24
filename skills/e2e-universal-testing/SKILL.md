---
name: e2e-universal-testing
description: End-to-end testing skill covering unit, API, integration, auth, performance, and security testing across multiple tech stacks. Use when writing, executing, or fixing test suites, running coverage checks, or implementing security/SQLi test vectors. Do NOT use for manual exploratory testing without code creation.
---

# Universal End-to-End & Security Testing

Provides deterministic test suites across all application layers (Unit, Integration, E2E UI, API, Security, Auth), generating executable test files and validating application behavior against edge cases and attack vectors.

---

## Tool Selection Matrix

| Layer | Stack | Primary Tool | Secondary Tool |
|---|---|---|---|
| Unit / React | TypeScript / JS / Next.js | **Vitest** + React Testing Library | Jest |
| Unit / Async | Python / FastAPI / Django | **Pytest** + pytest-asyncio | unittest |
| API | REST / GraphQL / gRPC | **Supertest** / **httpx** | Newman |
| E2E UI | Web Apps | **Playwright** | Cypress |
| DB / Integration | PostgreSQL / MySQL / Redis | **Testcontainers** | In-memory mocks |
| Security / SQLi | Auth / API Endpoints | **OWASP Payload Suite** | Semgrep |

---

## Execution Directives & Workflow

1. **Test Environment & Structure Setup**
   - Place unit/integration/API tests in `__tests__/` (JS/TS) or `tests/` (Python).
   - Ensure explicit test assertions covering: Happy Path, Boundary Values (0, null, MAX_INT), Invalid Types, Oversized Payloads, and Security Vectors.

2. **Security & Input Validation Testing**
   - Test endpoints against XSS (`<script>alert(1)</script>`), SQL Injection (`' OR 1=1 --`), and SSRF inputs to verify parameterized queries and sanitization.
   - Audit Auth routes for RBAC violations, JWT expiry, invalid secret signatures, and missing Bearer headers.

3. **Execution & Coverage Verification**
   - Run the appropriate test runner command (`npx vitest run --coverage` or `pytest --cov`).
   - Fix failing tests without deleting or disabling passing assertions.

---

## Verification & Constraints

- ❌ **No Dummy Mocks for Security:** Always verify actual failure status codes (401/403/422) on malformed/unauthorized requests.
- ❌ **No Silenced Assertions:** Never comment out broken tests to pass coverage goals.

- [ ] All unit, API, and security tests pass with 0 errors.
- [ ] Code coverage satisfies target threshold ($\ge 80\%$).
- [ ] Security test vectors return expected error codes without 500 unhandled exceptions.
