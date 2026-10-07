# Hostinger Shared Hosting: Next.js + Strapi Optimized Architecture

**Status**: Verified & Approved
**Context**: Deploying a modern JavaScript full-stack (Next.js + Strapi) on resource-constrained Shared Hosting environments (like Hostinger Business Shared Hosting).

## The Problem
Hostinger Business Shared Hosting imposes strict limits on CPU, RAM, and `max_processes`. Running two persistent Node.js servers (one for Next.js SSR and one for Strapi) simultaneously will reliably exhaust these limits. The heavy `npm run build` process for Next.js is particularly prone to crashing the server and bringing down all websites on the shared account.

## The Principal Architect Solution
To survive on shared infrastructure, the core architectural principle is to **shift compute burden off the constrained environment**.

### 1. The Zero-Footprint Frontend (Next.js)
Instead of deploying Next.js as a Server-Side Rendered (SSR) Node app, we convert it to a **Static Export (SSG)**.
- **Config**: Set `output: 'export'` in `next.config.ts`.
- **Images**: Next.js native Image Optimization requires a server. You must set `images: { unoptimized: true }` or use a custom third-party loader.
- **Routing**: API routes (`/api/*`) are not supported in static exports. All dynamic on-demand ISR (`revalidateTag`) logic must be removed.
- **Execution**: The output is purely HTML/CSS/JS. Hostinger's LiteSpeed web server serves this with virtually zero CPU/RAM cost.

### 2. The Offloaded Build Pattern
Never run `npm run build` for Next.js on the shared host.
- **CI/CD**: Use **GitHub Actions** (or a similar free CI runner) to build the Next.js static site whenever `main` is updated.
- **Delivery**: The GitHub Action should use FTP (e.g., `SamKirkland/FTP-Deploy-Action`) to push the compiled `/out` directory directly into Hostinger's `public_html`.
- **Content Updates**: When content is updated in Strapi, Strapi fires a webhook to GitHub Actions (`repository_dispatch`), triggering a fresh build and deploy.

### 3. The Optimized Backend (Strapi)
Strapi remains the single Node.js process running on the shared account.
- **Database**: Shared hosting typically does not provide PostgreSQL. We must use **MySQL** which is native, free, and unlimited on Hostinger. Install `mysql2` and remove `better-sqlite3`.
- **Connection Pooling**: To prevent Strapi from hoarding memory, clamp the MySQL connection pool in `config/database.ts`:
  ```typescript
  pool: { min: env.int('DATABASE_POOL_MIN', 1), max: env.int('DATABASE_POOL_MAX', 3) }
  ```
- **Deployment**: Deploy Strapi as a "Node.js Web App" on a subdomain (e.g., `api.yourdomain.com`) connected directly to GitHub via hPanel auto-sync.

## Summary
By offloading the build step to GitHub and reducing Next.js to a static asset bundle, we eliminate 50% of the persistent Node.js footprint and 100% of the build-time CPU spikes, achieving a highly stable, production-grade deployment on cheap shared infrastructure.
