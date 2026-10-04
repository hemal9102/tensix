# CLAUDE.md — TENSIX (tensix.in)
# AI Agent Rules, Infrastructure, SEO & Operational Protocol
# Last updated: 2026-10-04

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
- **Canonical URLs:** `https://www.tensix.in/<path>` with NO `.html` (e.g. `https://www.tensix.in/about`, home = `https://www.tensix.in/`). Apex `tensix.in` 308s to www; `vercel.json` `cleanUrls: true` 308s every `*.html` to the extensionless path.
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
Person        →  https://tensix.in/#person
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
| `submit_google_indexing.py` | Google Indexing API | Submits sitemap URLs as `URL_UPDATED`. **Google officially supports this API only for `JobPosting` / `BroadcastEvent` pages**; for normal pages it may be ignored. Primary Google path = `sitemap.xml` + Search Console. |
| `submit_indexnow.py` | Bing, Yandex, Seznam, Naver | Submits all sitemap URLs via IndexNow (`host` must be `www.tensix.in` to match the URLs) |
| `c4b69324e9334bbba3ff6f3f02db4fb6.txt` | IndexNow Key Verification | Root verification key file served at `https://www.tensix.in/c4b69324e9334bbba3ff6f3f02db4fb6.txt` |
| `google-service-account.json` | Google Cloud API | Credentials file for Google Indexing API (in `.gitignore`) |

### Running Indexing Pipelines:
```powershell
# 1. Submit to IndexNow (Bing / Yandex)
python submit_indexnow.py

# 2. Google: resubmit sitemap.xml in Search Console (Indexing API is job/livestream-only)
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
- Exactly ONE `<link rel="canonical">` per page, equal to `https://www.tensix.in/<path>` (no `.html`). `screaming_frog_audit.py` enforces this.
- Internal links are root-relative and extensionless (`/about`, `/blogs/<slug>`).

### ❌ NEVER DO
- **NO `AggregateRating` schemas** without verifiable external review data.
- **NO duplicate `@id` anchors** across pages.
- **NO committing secret credentials:** `google-service-account.json`, `.env`, or `.pem` keys must remain strictly in `.gitignore`.
- **NO backslashes in canonical URLs** — always use standard forward slashes.
- **NO `.html` in canonical, sitemap `<loc>`, og:url, hreflang, or JSON-LD `url`/`item`** — these 308-redirect under cleanUrls. (`@id` values are opaque identifiers and stay unchanged.)
- **Do NOT run scripts in `09_Archive/legacy_seo_scripts/`** — they hardcode the old `hemalshah.vercel.app` domain and `.html` URLs.

---

## 6. REBRANDING & DISAMBIGUATION

- **TENSIX** is an elite software, autonomous AI agent, and cloud engineering studio.
- It was previously incubated under the engineering alias *HK Engineering*.
- To avoid any confusion with manufacturing or CNC suppliers, all public entity branding is exclusively **TENSIX** (`https://tensix.in/`).
- The transition record is permanently documented at `https://tensix.in/hk-engineering-ahmedabad.html`.

---

## 7. GOOGLE INGESTION & CAFFEINE EDGE PIPELINE STANDARD

> **Caution:** the tier mechanics below (SimHash thresholds, 24–72h sharding, Wave 2 queue) are working hypotheses, NOT published by Google. Treat them as heuristics, not rules.

- Technical pages should follow the heuristics in `GOOGLE_INGESTION_ARCHITECTURE.md`:
  - **Tier 0:** Sub-100ms TTFB on Cloudflare/Vercel edge to maximize Googlebot hostload crawl budget.
  - **Tier 1:** 100% pre-rendered semantic HTML5 with `defer` scripts to avoid WRS Wave 2 queue delays.
  - **Tier 2:** High-IDF technical terminology and distinct case studies to ensure >3 Hamming distance clearance on 64-bit SimHash.
  - **Tier 3:** Single unified `@graph` JSON-LD schema linking `#organization` and `#person` for Knowledge Graph entity resolution.
  - **Tier 4 & 5:** Respect the 24–72 hour Caffeine edge sharding and staging buffer; monitor Search Console progression from "Crawled - currently not indexed" to "URL is on Google".

---

© 2026 TENSIX. Founded and solely owned by Hemal Shah.

---

## 8. MANDATORY SKILLS & PHILOSOPHY (from ~/.gemini/GEMINI.md)

### 8.1 Ponytail Skill (`ponytail`) — Always Active
- **Every coding, refactoring, designing, reviewing, or fixing task must adhere to the `ponytail` skill.**
- Channel a pragmatic senior engineer: choose the simplest, shortest, cleanest, and most minimal solution that actually works.
- Always climb the ladder:
  1. **YAGNI**: Question whether speculative code or features need to exist at all.
  2. **Codebase Reuse**: Reuse existing utilities, helpers, and patterns already in the repository before writing new ones.
  3. **Standard Library First**: Prefer stdlib over external packages.
  4. **Native Platform Features**: Use native platform capabilities (HTML/CSS, native APIs, database constraints) before pulling dependencies.
  5. **No Bloat**: Avoid unnecessary dependencies, boilerplate, or over-engineering.

### 8.2 TypeSafe Skill (`typesafe-ai` / `typesafe`) — Always Active
- **Every AI-powered workflow, semantic decision, routing, or LLM-driven task must leverage the `typesafe-ai` skill.**
- Treat AI units of intelligence as typed programming primitives rather than arbitrary free-form generation.
- Use System One models (e.g. Jev) for fast, calibrated, typed judgments:
  - **Choice**: Categorization and option selection with probability distributions.
  - **Noul**: Calibrated binary condition probabilities.
  - **Score**: Probability-weighted ranking across ordered dimension levels.
- Keep workflows deterministic in application code; use TypeSafe judgments for programmable common sense and semantic evaluations.
