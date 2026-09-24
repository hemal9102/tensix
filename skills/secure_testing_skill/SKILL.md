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
