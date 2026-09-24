---
name: static-website-security
description: Hardens static websites (HTML/CSS/JS on Vercel, Netlify, GitHub Pages) via SRI hashes, HTTP security headers, and CSP policies. Use when auditing or securing static frontends. Do NOT use for dynamic backend applications with SQL databases, server-rendered frameworks (Next.js/Nuxt), or API authorization testing.
tools: [Bash, Read, Edit, Write, Glob, Grep]
---

# Static Website Security Hardening

Use this skill to audit and secure static HTML/CSS/JS websites against CDN supply-chain attacks, missing HTTP security headers, clickjacking, and XSS.

---

## Operational Constraints

* ❌ **DO NOT** apply SQL injection scanners to static sites.
* ❌ **DO NOT** add SRI attributes to dynamic fonts (e.g. Google Fonts CSS).
* ❌ **DO NOT** deploy CSP without testing dynamic fetch endpoints in `connect-src`.

---

## Step 1 — Audit CDN & Form Endpoints
