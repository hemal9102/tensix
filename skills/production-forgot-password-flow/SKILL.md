---
name: production-forgot-password-flow
description: Enforces production-grade security patterns and step-by-step specifications for implementing or auditing Password Reset & Recovery flows. Use when building, auditing, or refactoring forgot-password endpoints, token hashing, email reset links, or session invalidation logic. Do NOT use for general OAuth login, basic password hashing, or standard signup flows.
---

# Production Forgot Password Flow Security Architecture

Defines mandatory security invariants, token lifecycles, database patterns, and API contracts for password recovery workflows.

## 🎯 When to Use
* Implementing or reviewing password recovery (`/forgot-password`, `/reset-password`) endpoints.
* Auditing existing auth code for account enumeration, token leak vulnerabilities, or session persistence bugs.
* Setting up rate limiting, password reset token hashing (SHA-256), and session revocation.

## ❌ When NOT to Use
* Initial user signup or OAuth/SSO login implementation (use standard authentication skills).
* General user profile password change when user is already authenticated.

---

## 🚫 Non-Negotiable Security Invariants
* **NEVER** return distinguishable API responses based on email existence ("Email not found"). Always return generic confirmation: *"If an account exists, a reset link has been sent."*
* **NEVER** store raw tokens in the database. Store only a cryptographic SHA-256 hash. Send the raw 256-bit token in the email link only.
* **NEVER** log raw reset tokens or send plaintext passwords in emails.
* **NEVER** allow token reuse. Set `used_at` timestamp immediately upon first redemption within an atomic transaction.
* **NEVER** allow tokens to remain valid past 15 minutes.
* **NEVER** leave active sessions open. All active sessions and refresh tokens MUST be deleted atomically when a password is reset.

---

## 🏗️ Implementation Architecture

### 1. Database Schema Pattern (Prisma / SQL)
```prisma
model PasswordResetToken {
  id         String    @id @default(cuid())
  user_id    String
  token_hash String    @unique        // SHA-256 hash of raw token
  expires_at DateTime                 // now() + 15 minutes max
  used_at    DateTime?                // Set on first redemption
  created_at DateTime  @default(now())
  ip_address String?
  user       User      @relation(fields: [user_id], references: [id], onDelete: Cascade)
  @@index([user_id])
  @@index([expires_at])
}
```

### 2. API Contract & Flow Sequence

| Endpoint | Method | Input | Core Operation | Security Constraint |
| :--- | :--- | :--- | :--- | :--- |
| `/api/auth/forgot-password` | `POST` | `{ email }` | Rate limit (5/hr/ip) -> Hash token -> Store hash -> Email raw token | Generic 200 response for all valid email inputs |
| `/api/auth/reset-password/validate` | `GET` | `?token=` | Hash token -> Lookup token record | Check `expires_at > now()` & `used_at == null` |
| `/api/auth/reset-password` | `POST` | `{ token, new_password }` | Atomic transaction: Update password + set `used_at` + delete sessions | Invalidate ALL user sessions & refresh tokens |

---

## 🔒 Security Decision Matrix

| Potential Vulnerability | Mitigation Strategy | Enforcement |
| :--- | :--- | :--- |
| **Account Enumeration** | Constant-time generic responses | Identical HTTP response body & status code for existing/non-existing emails |
| **DB Breach Token Theft** | One-way token hashing | DB stores `sha256(raw_token)`, email contains `raw_token` |
| **Replay Attacks** | Atomic single-use marking | Transactional `used_at` check & update |
| **Session Hijacking** | Multi-device revocation | `prisma.session.deleteMany({ where: { user_id } })` in reset transaction |
| **Brute Force & Spam** | Tiered Rate Limiting | 5 requests/hr per email, 10 requests/hr per IP via Redis |

---

## ⚡ Grounding & Verification Protocol

After implementation or modification, run deterministic checks:
1. **Schema Check:** Run `npx prisma validate` to ensure indexes and relations match the security pattern.
2. **Type Check & Lint:** Run `npm run typecheck` or `npx tsc --noEmit` to verify route handlers and types.
3. **Automated Security Tests:** Run unit/integration tests to verify anti-enumeration and replay prevention:
   - `npm test -- forgot-password`
   - Verify `429 Too Many Requests` when rate limits are exceeded.
   - Verify token invalidation on second invocation.
