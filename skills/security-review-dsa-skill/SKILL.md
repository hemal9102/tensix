---
name: security-review-dsa-skill
description: Conducts rigorous security vulnerability reviews (OWASP Top 10, threat modeling) and Data Structures & Algorithms (DSA) performance audits (time/space complexity analysis, edge cases). Use when reviewing code for security vulnerabilities, memory leaks, or algorithmic efficiency. Do NOT use for basic UI layout styling or devops infrastructure deployment.
---

# Security & DSA Code Review Lead

Combines defensive security auditing (STRIDE/OWASP) with algorithmic complexity analysis ($O(N)$ bounds, space complexity, data structures) to guarantee secure and scalable code.

## 🎯 When to Use
* Auditing code for security vulnerabilities (injection, XSS, broken access control, secret leaks).
* Conducting DSA reviews to optimize algorithm efficiency, recursion depth, or time/space complexity.
* Evaluating edge cases, memory allocations, data structure choices, and concurrent access patterns.

## ❌ When NOT to Use
* Infrastructure deployment or cloud DNS configuration (use production engineering skill).
* Frontend layout aesthetics or visual CSS design (use UI/UX master skill).

---

## 🚫 Non-Negotiable Review Constraints
* **NEVER** pass un-sanitized user input directly to DB queries, shell execution, or raw HTML rendering.
* **NEVER** allow hardcoded API keys, JWT secrets, or credentials in source code.
* **NEVER** accept $O(N^2)$ or $O(2^N)$ algorithms where $O(N \log N)$ or $O(N)$ solutions exist for production data bounds.
* **NEVER** ignore boundary conditions (empty inputs, integer overflow, null pointers, off-by-one errors).

---

## 🛡️ Security Audit Checklist (OWASP / STRIDE)

| Security Focus Area | Risk Vectors | Mitigation Requirement |
| :--- | :--- | :--- |
| **Injection Defense** | SQLi, Command Injection, XSS | Parametrized queries, ORM escaping, strict schema validation |
| **Access Control** | IDOR, Privilege Escalation | Explicit RBAC/ABAC checks on every route handler |
| **Secrets & Crypto** | Exposed keys, weak hashing | Environment variables, SHA-256 / bcrypt / Argon2id |
| **Input Validation** | ReDoS, buffer overflow, path traversal | Zod / Pydantic schemas, path normalization |

---

## 🧮 DSA & Algorithmic Performance Audit

| Algorithmic Vector | Anti-Pattern | Target Optimization |
| :--- | :--- | :--- |
| **Time Complexity** | Nested loops ($O(N^2)$) on large collections | Hash maps, two-pointer, divide & conquer ($O(N)$ or $O(N \log N)$) |
| **Space Complexity** | Unbounded memory allocation, recursive stack growth | Iterative processing, streaming, tail-recursion, sliding window |
| **Data Structure Choice** | Using Array lookup $O(N)$ for frequent key searches | Map / Set ($O(1)$ amortized lookup) |
| **Edge Cases** | Null/empty structures, max limits, concurrent mutation | Guard clauses, immutability, thread synchronization |

---

## ⚡ Grounding & Verification Protocol

Before completing a review or optimization:
1. **Security Scan:** Check for hardcoded secrets and un-sanitized inputs.
2. **Typecheck & Linter:** Run static analysis tools (`npx tsc --noEmit`, `eslint`, or `mypy`).
3. **Automated Unit & Benchmark Tests:**
   - Execute existing test suite (`npm test` / `pytest`).
   - Validate performance against boundary datasets ($N=10,000+$ items).
