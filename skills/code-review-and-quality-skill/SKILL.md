---
name: code-review-and-quality-skill
description: Audits code for security vulnerabilities, coding standards compliance, code duplication, and maintainability. Use when reviewing code before merging, scanning for security flaws or hardcoded secrets, checking DRY compliance, or enforcing code quality standards. Do NOT use for initial code generation or full system architecture redesign.
---

# Code Review & Quality Audit

Performs static code analysis, security vulnerability scanning, DRY (Don't Repeat Yourself) duplication checks, and adherence to project engineering standards.

---

## Core Focus Areas

1. **Security Vulnerability Scanning**
   - Check for hardcoded secrets, API keys, credentials, or sensitive tokens.
   - Audit input sanitization to prevent SQL injection, XSS, and command injection.
   - Verify safe handling of environment variables and secrets management.

2. **DRY & Duplication Analysis**
   - Detect repeated logic blocks across multiple modules or components.
   - Recommend or refactor repeated routines into shared utility modules.

3. **Code Quality & Maintainability**
   - Enforce explicit typing, clean function boundaries, and single-responsibility principles.
   - Ensure proper error handling (avoid swallowing exceptions or using empty catch blocks).

---

## Execution Workflow

1. **Identify Review Targets**
   - Inspect newly created or modified files in the codebase.
2. **Execute Static Scans**
   - Run project linters, static security scanners, or duplication checkers.
3. **Refactor & Apply Fixes**
   - Extract duplicated logic into shared utilities.
   - Eliminate hardcoded values and improve error handling.
4. **Generate Structured Review Report**
   - Categorize findings into Security, Performance, Quality, and Duplication with concrete fix recommendations.

---

## Verification & Safety Rules

- [ ] Zero hardcoded credentials or API tokens present in diff.
- [ ] Linter and typecheck commands run clean with 0 errors.
- [ ] Refactored helper abstractions preserve original function signatures and behaviors.
