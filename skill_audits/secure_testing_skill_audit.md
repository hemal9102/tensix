# 🛡️ Skill Quality Audit Report

**Skill Target:** `secure_testing_skill`
**Overall Score:** `7 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Description covers intent well ("safe security testing of your application"), but lacks explicit slash commands (e.g. `/security-test`) or explicit negative triggers (e.g., "Do NOT use for external penetration testing or automated web scraping"). |
| **2. Single Responsibility** | 2/2 | Focused strictly on a single domain: defensive security testing and application vulnerability assessment. |
| **3. Token Efficiency** | 2/2 | Highly token-efficient (37 lines). Concise and lightweight. |
| **4. Constraint Enforcement** | 1/2 | Provides good high-level advice, but lacks explicit negative rules (`❌ Don't`), concrete code examples, or structured decision matrices. |
| **5. Verification Loop** | 1/2 | Mentions writing integration tests and static analysis, but does not provide specific automated execution commands or verification scripts. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Name Mismatch:** The frontmatter `name:` (`secure-testing-workflow`) differs from the directory name (`secure_testing_skill`).
* **Missing Explicit Negative Triggers:** Does not explicitly state when NOT to activate (e.g., unauthorized active scanning against third-party hosts).
* **Missing Verification Commands:** Lacks copy-pasteable CLI commands for SAST, linting, or integration testing.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Align Name & Triggers:** Match frontmatter name to directory name (`secure-testing-skill`) and add explicit slash command triggers (`/security-audit`, `/secure-test`).
2. **Add Strict Constraint Matrix:** Include explicit negative rules (`❌ Don't`) forbidding aggressive automated scanning against external endpoints.
3. **Add Deterministic Verification Execution:** Include CLI commands for running static analysis (e.g., `npm audit`, `snyk test`, `semgrep`).

---

## 📦 Recommended 10/10 Refactored Version

```markdown
---
name: secure-testing-skill
description: >
  Safe, defensive security testing workflow for application codebases.
  Use when the user requests a security review, vulnerability assessment, code audit, or invokes /security-audit or /secure-test.
  Do NOT use for unauthorized external penetration testing, automated web scraping, or attacking third-party hosts.
tools: [Read, Write, Bash, PowerShell, Grep]
---

# Safe and Thorough Security Testing Workflow

Identify attack surfaces, review code patterns, write security integration tests, and run automated static analysis to harden application security.

---

## 1. Defensive Security Workflow

| Phase | Core Objective | Actionable Steps |
| :--- | :--- | :--- |
| **1. Attack Surface Mapping** | Identify input vectors | List all API endpoints, query params, headers, form inputs, and file upload routes. |
| **2. Code Review** | Uncover vulnerabilities | Inspect handlers for unparameterized raw SQL, unsanitized HTML output (XSS), or broken auth. |
| **3. Integration Tests** | Test resilience | Write automated tests sending unexpected/malformed payloads to ensure safe HTTP failures. |
| **4. Static Analysis** | CI security scanning | Execute dependency auditors and SAST linters. |
| **5. Manual Verification** | Endpoint validation | Use localized `curl` requests to confirm fixes before and after implementation. |

---

## 2. Negative Constraints & Guardrails

* ❌ **Never** run automated fuzzing or vulnerability probes against production third-party IP addresses.
* ❌ **Never** disable SSL/TLS verification in test scripts unless running against an isolated local mock server.
* ❌ **Never** print raw passwords, API keys, or secret tokens in test output logs.

---

## 3. Automated Verification Execution

Execute these commands to verify codebase security:

```bash
# 1. Dependency Vulnerability Audit
npm audit --audit-level=high

# 2. Static Application Security Testing (SAST)
npx semgrep --config=auto .

# 3. Security Test Suite Execution
npm test -- __tests__/security/
```
```
