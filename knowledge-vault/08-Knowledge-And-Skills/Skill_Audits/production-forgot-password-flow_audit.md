# 🛡️ Skill Quality Audit Report

**Skill Target:** `production-forgot-password-flow`
**Overall Score:** `8 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 2/2 | Frontmatter description is hyper-specific, intent-driven, lists explicit activation triggers (building reset flows, reviewing auth PRs, auditing password recovery), and specifies tool dependencies. |
| **2. Single Responsibility** | 2/2 | 100% focused on a single domain: production-grade password reset / forgot password flow implementation end-to-end. |
| **3. Token Efficiency** | 0/2 | Over 600 lines long! Contains complete TypeScript, Prisma, and React code implementations inline in `SKILL.md` rather than offloading code files to an on-demand `references/` or `templates/` directory. |
| **4. Constraint Enforcement** | 2/2 | Outstanding rules and negative constraints: security principle matrix, non-negotiable token rules (SHA-256 in DB, raw in email), rate limits, anti-pattern risk table, and pre-merge checklist. |
| **5. Verification Loop** | 2/2 | Includes an automated Vitest test suite (`__tests__/auth/forgot-password.test.ts`) covering rate limiting, enumeration prevention, token invalidation, and session deletion verification. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Monolithic File Length (640 lines):** Storing full multi-file boilerplate (Prisma schemas, Next.js route handlers, React pages, email HTML templates, and test suites) directly inside `SKILL.md` wastes substantial LLM context space on every activation.
* **Inline Templates Instead of On-Demand References:** Large code blocks should be modularized into reference files (e.g., `references/api-routes.ts`, `references/email-template.ts`, `references/test-suite.ts`) and loaded only when needed.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Modularize Code Assets:** Move full route handlers, React components, and test files into a `references/` directory within the skill folder.
2. **Keep Core SKILL.md Concise (<150 lines):** Retain the security principles matrix, architectural flow, anti-pattern list, and pre-merge checklist in `SKILL.md`, with concise pointers to reference files.
3. **Maintain 100% Security Rigor:** Preserve all non-negotiable security constraints, anti-pattern warnings, and test requirements.

---

## 📦 Recommended 10/10 Refactored Version

```markdown
---
name: production-forgot-password-flow
description: |
  Production-grade architecture and full implementation for Forgot Password /
  Reset Password flows. Covers DB schema (Prisma), token generation, hashing,
  API routes, rate limiting, session invalidation, email templates, frontend
  states, and security anti-patterns. Activates whenever building or reviewing
  any auth reset, password recovery, or token-based verification feature.
tools: [Read, Write, Bash, PowerShell, Grep]
---

# Production Forgot Password Flow

## Role
You are a **Senior Security Engineer**. When this skill activates, implement the full flow end-to-end — DB schema, API routes, email, and frontend. Never implement a partial flow. Never store plaintext tokens. Never reveal whether an email exists.

## When This Skill Activates
- Building a forgot password / reset password feature
- Reviewing any PR that touches auth, tokens, or password handling
- Any mention of reset link, email verification, or token expiry
- Auditing existing password reset for security issues

---

## 1. Security Principles (Non-Negotiable)

| Principle | Rule |
|---|---|
| **No enumeration** | Always respond "If an account exists, we sent an email" — never "Email not found" |
| **No plaintext tokens** | Hash token with SHA-256 before storing. Send only raw token in email. |
| **No reuse** | Mark token `used_at` on first use. Reject all subsequent uses. |
| **Short-lived** | Token expires in 15–30 minutes. Never longer. |
| **Session invalidation** | Invalidate ALL sessions on password reset — not just current device. |
| **No password in email** | Never email the new password. |
| **No token in logs** | Never log the raw token string. Log only `token_id` or hashed form. |
| **Rate limiting** | 5 requests/hr per email, 10 requests/hr per IP. |

---

## 2. Architecture & File Structure

Offload detailed code implementations to on-demand reference files:
- `references/schema.prisma` — Database schema & token cleanup SQL
- `references/tokens.ts` — Crypto token generation & SHA-256 hashing
- `references/routes.ts` — Next.js API routes (forgot-password, validate, reset-password)
- `references/templates.ts` — HTML email templates
- `references/components.tsx` — Client components for forgot & reset password forms
- `references/tests.ts` — Vitest integration & security regression test suite

---

## 3. Anti-Patterns to Avoid

| Anti-Pattern | Risk | Correct Approach |
|---|---|---|
| `"Email not found"` response | Account enumeration | Always: "If an account exists, we sent an email" |
| Store raw token in DB | Account takeover | Store SHA-256 hash only |
| Tokens expire in 24hr+ | Phishing risk | 15–30 minutes max |
| Reusable tokens | Replay attack | Set `used_at` on first use, reject thereafter |
| No session invalidation | Attacker session persists | Delete ALL sessions in same transaction |
| Password in email | Credential exposure | Never send passwords — only reset links |
| Token in server logs | Log scraping | Log only `token_id`, never raw token |
| No rate limit | Brute force / Mail bomb | 5/hr per email, 10/hr per IP |

---

## 4. Verification & Testing

Always run integration tests after implementing or modifying reset flows:

```bash
npx vitest run __tests__/auth/forgot-password.test.ts
```

### Pre-Merge Checklist
- [ ] Raw token stored only as SHA-256 hash in database
- [ ] Forgot-password endpoint returns identical message for existing/non-existing emails
- [ ] Token expires in 15 minutes and is marked `used_at` upon redemption
- [ ] All active sessions deleted atomically during password reset
- [ ] Rate limiting enforced (5/hr per email, 10/hr per IP)
- [ ] Vitest test suite passes with 100% coverage on security edge cases
```
