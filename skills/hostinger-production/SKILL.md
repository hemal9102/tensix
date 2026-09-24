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
