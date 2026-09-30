# CLAUDE.md — TENSIX (tensix.in)
# AI Agent Rules, Infrastructure, SEO & Operational Protocol
# Last updated: 2026-09-30

---

## 0. GIT & GITHUB — MANDATORY

> **ALWAYS use account `hemal9102` for all git operations. No exceptions.**

| Field              | Value                                                        |
|--------------------|--------------------------------------------------------------|
| **GitHub account** | `hemal9102`                                                  |
| **Repo**           | `https://github.com/hemal9102/tensix.git`                    |
| **Branch**         | `main`                                                       |
| **Push command**   | `git push origin main`                                       |

### Production Deployment & DNS Architecture:
- **Canonical Domain:** `https://tensix.in/` (Apex redirects 308 to `https://www.tensix.in/`)
- **DNS Host:** Cloudflare (Authoritative NS: `lina.ns.cloudflare.com`, `mark.ns.cloudflare.com`)
- **Hosting Platform:** Vercel (Auto-deploys from GitHub `main` branch)
- **CNAME Target:** `d8ced1b4152d7850.vercel-dns-017.com`

### Git & Verification Workflow:
```powershell
$env:PYTHONIOENCODING="utf-8"
python validate_schemas.py
python screaming_frog_audit.py
git add -A
git commit -m "feat: <description>"
git push origin main
```

---

## 1. PROJECT IDENTITY & SCOPE

| Field            | Value                                                              |
|------------------|--------------------------------------------------------------------|
| **Project**      | TENSIX — Autonomous AI Systems, Cloud Infra & Software Studio      |
| **Owner**        | Hemal Shah (Sole Founder & Principal Architect)                    |
| **Canonical URL**| `https://tensix.in/` (also serves `https://www.tensix.in/`)         |
| **Location**     | Navrangpura, Ahmedabad, Gujarat 380009, India (23.0366° N, 72.5615° E)|
| **Stack**        | Semantic HTML5 + Vanilla CSS3 / JS + Vercel Edge Serverless        |
| **Total Pages**  | 37 Production Pages (All passing Schema and Crawler Audits)         |

---

## 2. CENTRAL ENTITY IDs — NEVER CHANGE THESE

These `@id` anchors are the single source of truth for the JSON-LD schema web:

```
Organization  →  https://tensix.in/#organization
Person        →  https://hemalshah.vercel.app/#person
WebSite       →  https://tensix.in/#website
```

- **Full entity definitions** live on `index.html`.
- **All other pages** reference via `{"@id": "..."}` only (Entity Trap pattern).
- This guides AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Googlebot) directly across the site hierarchy.

---

## 3. INSTANT INDEXING & SEARCH SUBMISSION ENGINES

The repository contains automated instant indexing pipelines:

| Script / Asset | Target Engine | Purpose & Usage |
|---|---|---|
| `submit_google_indexing.py` | Google Search Console Indexing API | Submits all sitemap URLs as `URL_UPDATED` using service account |
| `submit_indexnow.py` | Bing, Yandex, Seznam, Naver | Submits all sitemap URLs via IndexNow API protocol |
| `c4b69324e9334bbba3ff6f3f02db4fb6.txt` | IndexNow Key Verification | Root verification key file served at `https://tensix.in/c4b69324e9334bbba3ff6f3f02db4fb6.txt` |
| `google-service-account.json` | Google Cloud API | Credentials file for Google Indexing API (in `.gitignore`) |

### Running Indexing Pipelines:
```powershell
# 1. Submit to Google Indexing API
python submit_google_indexing.py

# 2. Submit to IndexNow (Bing / Yandex)
python submit_indexnow.py
```

---

## 4. DESIGN SYSTEMS & CORE COMPONENTS ACROSS THE SITE

### 4.1 Swiss Industrial Design System
- **Monochrome Brutalist Aesthetic:** Precision typography, dark-mode terminal consoles, high-contrast badges, and negative space ratios.
- **Interactive ROI Calculator:** Embedded client savings estimator comparing SaaS bloat vs bare-metal Python/VPS setups.
- **Live Diagnostic Console:** Animated telemetry dashboard on the homepage showing agent loop status, ping response, and system throughput.
- **Architectural Topology Schematics:** In-line SVG diagrams rendering zero-downtime CI/CD pipelines, reverse proxies, and GraphRAG knowledge flows.

### 4.2 High-Converting Competitor & Comparison Matrices
- **`tensix-vs-traditional-agencies.html`:** Full 7-dimension comparison matrix contrasting TENSIX against Indian agencies (Elsner, KrishaWeb, Uplers, Growth Hackers, WPWeb Infotech).
- **`services.html`:** Complete 6-stage hybrid delivery pipeline (Blueprint &rarr; Sandbox &rarr; Engineering &rarr; Hardening &rarr; Verification &rarr; Retainer).
- **Local Industry Digital Survival Guides:** 6 long-form whitepapers targeting Ahmedabad's economic clusters (Textiles, Pharma, Machinery, Real Estate, Jewelry, Healthcare).

---

## 5. SCHEMA, SEO & AUDIT RULES — MANDATORY

### ✅ ALWAYS DO
- Use `@graph` arrays — never standalone `@type` blocks.
- Every page must contain: `WebPage/Article`, `BreadcrumbList`, and `FAQPage` where relevant.
- All 37 pages must pass `python validate_schemas.py` with 0 errors before pushing.
- All internal links must pass `python screaming_frog_audit.py` with 0 broken links and 0 orphans.
- Keep `sitemap.xml` strictly updated with all canonical URLs.

### ❌ NEVER DO
- **NO `AggregateRating` schemas** without verifiable external review data.
- **NO duplicate `@id` anchors** across pages.
- **NO committing secret credentials:** `google-service-account.json`, `.env`, or `.pem` keys must remain strictly in `.gitignore`.
- **NO backslashes in canonical URLs** — always use standard forward slashes.

---

## 6. REBRANDING & DISAMBIGUATION

- **TENSIX** is an elite software, autonomous AI agent, and cloud engineering studio.
- It was previously incubated under the engineering alias *HK Engineering*.
- To avoid any confusion with manufacturing or CNC suppliers, all public entity branding is exclusively **TENSIX** (`https://tensix.in/`).
- The transition record is permanently documented at `https://tensix.in/hk-engineering-ahmedabad.html`.

---

© 2026 TENSIX. Founded and solely owned by Hemal Shah.
