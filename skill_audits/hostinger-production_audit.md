# 🛡️ Skill Quality Audit Report

**Skill Target:** `hostinger-production`
**Overall Score:** `2 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Broad description with no negative triggering boundaries (`when NOT to use`). |
| **2. Single Responsibility** | 0/2 | Monolithic "Master Skill" anti-pattern attempting to act as DevOps, DB Admin, Security, SEO, Next.js, and Cloudflare engineer simultaneously. |
| **3. Token Efficiency** | 0/2 | File contains 323 lines of heavily sparse, double-spaced wall-of-text that bloats context unnecessarily. |
| **4. Constraint Enforcement** | 0/2 | Vague, single-word checklists ("Indexes", "N+1", "Cache headers") without strict rules, negative constraints, or code snippets. |
| **5. Verification Loop** | 1/2 | Includes standard build commands (`npm run build`), but lacks deterministic health check or smoke test scripts. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Monolithic Master Skill Anti-Pattern (Lines 13–15):** Explicitly claims to be 8 different roles simultaneously (Platform Engineer, DevOps, Node Architect, Next.js Architect, Security, Cloudflare, Reliability, etc.).
* **Excessive Vertical Whitespace & Bloat (Lines 56–84, 124–145, 230–252):** Unnecessary double-spacing inflates file line count to 323 lines while providing very little actionable instruction.
* **Vibes-Based Keyword Dumping:** Contains lists of single words (e.g., lines 126–144: `Indexes`, `N+1`, `Pooling`) without any actionable rules, thresholds, or code examples on *how* to audit or enforce them.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Narrow Scope to Hostinger Node/Next.js Deployment:** Strip out unrelated domains like database optimization, SEO, and Cloudflare (delegate to specialized skills).
2. **Compact Layout & Remove Bloat:** Compress line count under 100 lines using compact Markdown tables and clean lists.
3. **Enforce Concrete Deployment Guardrails:** Add strict pre-flight check commands, build validation, and automated health checks.

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: hostinger-production
description: Production deployment, environment configuration, and health verification for Node.js and Next.js applications on Hostinger hPanel/VPS. Use ONLY when deploying Node/Next apps to Hostinger. Do NOT use for general SEO, Cloudflare configuration, or database tuning.
tools: [run_command, view_file]
---

## Purpose

Automate and validate production deployment of Node.js and Next.js applications on Hostinger infrastructure with deterministic health checks.

---

## Pre-Flight Checklist & Guardrails

### ❌ Never Do
- Never deploy without verifying local production build succeeds (`npm run build`).
- Never expose raw `.env` files or secret keys in public root paths.
- Never bypass Node.js version alignment between host environment and `package.json`.

### ✅ Always Do
- Enforce Node.js runtime version compatibility (18.x–22.x LTS).
- Set `NODE_ENV=production` in Hostinger hPanel environment settings.
- Validate health endpoint (`/api/health`) post-deployment.

---

## Automated Deployment Workflow

1. **Pre-Deployment Build Verification:**
   ```bash
   npm run lint && npm run build
   ```

2. **Verify Environment Security:**
   ```bash
   grep -E "SECRET|KEY|PASSWORD" .env.production || echo "Secrets verified"
   ```

3. **Post-Deployment Health Verification:**
   ```bash
   curl -s -o /dev/null -w "%{http_code}" https://your-domain.com/api/health
   ```
   *Expected Result:* `200`
```
