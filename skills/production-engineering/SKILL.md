---
name: production-engineering
description: Audits production readiness, architecture, deployment pipelines, database migrations, security, and disaster recovery before code ships to production. Use when preparing for deployment, conducting pre-launch audits, or evaluating infrastructure PRs. Do NOT use for routine local development, UI styling tweaks, or standalone code refactoring.
---

# Production Engineering Lead

Comprehensive pre-production validation across infrastructure, application layers, database schemas, and networking configuration.

## 🎯 When to Use
* Pre-deployment audits for production environments (Hostinger, Cloudflare, AWS, etc.).
* Reviewing PRs modifying infrastructure code, environment variables, or database schemas.
* Diagnosing production incidents or performing "go live" readiness evaluations.

## ❌ When NOT to Use
* Local development setup or dev server troubleshooting (use local dev workflow).
* Feature code refactoring or component UI tweaks (use specific web engineer skills).
* Standalone security dependency checks without full infrastructure scope (use security review skills).

---

## 🚫 Critical Execution Constraints
* **NEVER** execute state-mutating shell commands (e.g., `DROP TABLE`, `rm -rf`, raw DB migrations) on production databases without explicit user approval.
* **NEVER** read all companion reference files upfront. Use lazy loading—only inspect relevant reference docs (e.g., `prisma-review.md`, `cloudflare-review.md`) based on the specific layer under investigation.
* **NEVER** bypass or suppress failing health checks or build steps. Stop immediately and report critical failures.

---

## 🔍 Layer-Based Audit Protocol

Traverse the stack systematically based on the change surface:

```
Architecture -> Env / Secrets -> Database -> Deployment -> CDN / DNS -> Application -> Observability -> Security
```

| Layer | Primary Focus | Verification Check |
| :--- | :--- | :--- |
| **Architecture** | Scalability, single points of failure | Verify stateless design & service decoupling |
| **Secrets & Env** | Missing env vars, exposed credentials | Audit `.env.example` vs production secret keys |
| **Database** | Migration safety, index optimization | Run `npx prisma validate` / dry-run schema diff |
| **Deployment** | Build reproducible scripts, fallback routes | Test production build command (`npm run build`) |
| **CDN & DNS** | Cloudflare SSL/TLS, CNAME rules, caching | Verify DNS records, cache headers, WAF rules |
| **Application** | Next.js/Express route handlers, 500 safety | Execute automated test suite (`npm run test`) |
| **Observability** | Log aggregation, metric tracking, alerts | Validate error boundary catches and logger setup |
| **Security & DR** | CORS, rate limiting, rollback plan | Verify automated backup & immediate rollback plan |

---

## ⚡ Grounding & Verification Loop

Before confirming production readiness:
1. **Inspect Change Surface:** Run `git status` and `git diff` to identify all affected configurations and code paths.
2. **Schema & Configuration Validation:** Run static validation commands (`npx prisma validate`, typechecks).
3. **Build & Test Verification:** Execute full test suite and production build step (`npm test`, `npm run build`).
4. **Final Gate & Scorecard:** Issue final verdict based on empirical build results.

---

## 📋 Production Readiness Scorecard

Always present the final audit using this structure:

| Evaluation Area | Score (0-10) | Status | Key Observations |
| :--- | :---: | :---: | :--- |
| **Architecture & Scalability** | X/10 | [PASS/FAIL] | [Notes] |
| **Deployment & Build Safety** | X/10 | [PASS/FAIL] | [Notes] |
| **Database & Migrations** | X/10 | [PASS/FAIL] | [Notes] |
| **Security & Secrets** | X/10 | [PASS/FAIL] | [Notes] |
| **Observability & Health Checks** | X/10 | [PASS/FAIL] | [Notes] |
| **Disaster Recovery & Rollback** | X/10 | [PASS/FAIL] | [Notes] |

**Production Ready:** `[YES / NO]`

### Critical Blockers (Must fix before launch):
- [ ] Item 1

### Recommendations:
- [ ] Recommendation 1
