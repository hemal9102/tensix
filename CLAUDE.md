# CLAUDE.md — TENSIX (tensix.in)
# AI Agent Rules, Infrastructure, SEO & Operational Protocol
# Last updated: 2026-10-05

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
python build_service_pages.py   # only if the SERVICES data changed
python build_agent_files.py     # md/ mirrors, llms*.txt, sitemaps, skill digest
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
| **Total Pages**  | 45 Production Pages incl. 8 `/services/*` pages (all passing Schema and Crawler Audits) |

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

### 4.1 Light Swiss Design System
- **White theme:** `--color-bg:#FFFFFF`, `--color-bg-light:#F8FAFC`, text `#0F172A`, muted `#475569`, and `<meta name="theme-color" content="#ffffff">` on every page. Precision typography, high-contrast badges, generous negative space.
- **Consoles and schematics are light panels**, not dark terminals. Inline SVG topology diagrams (e.g. the homepage `topology-chassis`) use dark strokes on white.
- Text accents use 600-level shades for contrast; `#fff` text only on gradient/blue buttons and `.nav-cta`.
- `apply_light_theme.py` was a one-off conversion. Later contrast fixes live directly in the pages, so re-running it will not reproduce them.

### 4.2 Services: Hub + One Page per Service
- **`services.html` is the hub:** its own `WebPage` plus an `OfferCatalog` whose items reference the 8 `Service` `@id`s. It links every pillar and pricing tab to its service page and shows the 6-step process (Understand the problem &rarr; Plan and fixed price &rarr; Design the screens &rarr; Build with AI tools &rarr; Review and testing &rarr; Launch and hand-over).
- **8 service pages at `/services/<slug>`**, generated by `build_service_pages.py` from one `SERVICES` data list (header/footer copied from `services.html`):
  - `ai-agent-development`
  - `custom-software-saas-development`
  - `website-development`
  - `cloud-devops`
  - `email-deliverability`
  - `data-scraping-automation`
  - `geo-aeo-seo` (custom quote, no fixed price)
  - `fractional-cto-retainers`
- Each page: plain-language H1, short "what you get" answer block, who it's for, process, 3 priced plans with a `/contact?plan=<slug>` CTA, FAQ, related services. One `@graph`: `WebPage`, `BreadcrumbList`, `Service` (`@id` `https://tensix.in/services/<slug>#service`, `provider` &rarr; `#organization`, `offers` with the exact INR card price) and `FAQPage`.
- Edit service content in `build_service_pages.py`, not in the generated HTML, then re-run it.
- Every production page carries the "Services navigation" footer column (`inject_footer_links.py` adds it idempotently).

### 4.3 Comparison & Local Guides
- **`tensix-vs-traditional-agencies.html`:** plain-language comparison of a one-person studio vs a typical agency (who you talk to, fixed price, ownership), including when another option suits you better. No named competitors.
- **Local Industry Digital Survival Guides:** 6 long-form whitepapers targeting Ahmedabad's economic clusters (Textiles, Pharma, Machinery, Real Estate, Jewelry, Healthcare).

---

## 5. SCHEMA, SEO & AUDIT RULES — MANDATORY

### ✅ ALWAYS DO
- Use `@graph` arrays — never standalone `@type` blocks.
- Every page must contain: `WebPage/Article`, `BreadcrumbList`, and `FAQPage` where relevant.
- All 45 pages must pass `python validate_schemas.py` with 0 errors before pushing (it also flags any `@id` fully defined on more than one page).
- All internal links must pass `python screaming_frog_audit.py` with 0 broken links and 0 orphans.
- Keep `sitemap.xml` strictly updated with all canonical URLs.
- Exactly ONE `<link rel="canonical">` per page, equal to `https://www.tensix.in/<path>` (no `.html`). `screaming_frog_audit.py` enforces this.
- Internal links are root-relative and extensionless (`/about`, `/blogs/<slug>`).

### ✍️ CONTENT RULE — PLAIN LANGUAGE & HONESTY
- Write for a business owner: lead with the benefit, explain jargon in a parenthesis or drop it, one clear CTA per section.
- **TENSIX is a one-person studio** (Hemal Shah, working with AI tools). Never imply a team, pods or staff.
- **No unverifiable claims:** no guarantees (uptime, PageSpeed scores, inbox placement, "zero downtime"), no unsourced stats or percentages, no "N businesses served", no invented savings comparisons, no fake testimonials. Describe what is actually done instead ("we set up monitoring and automatic restarts").
- FAQ schema answers must match the visible text.

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

## 7. AGENT READINESS & DEPLOY ALLOWLIST

Target: isitagentready Content Site 6/7 and Level 4, using honest standards only. Cloudflare is DNS-only (responses come from Vercel), so everything below is served by Vercel.

| Item | Where | Notes |
|---|---|---|
| Content Signals | `robots.txt` (every bot group) + HTTP `Content-Signal` header (`vercel.json`) | `Content-Signal: ai-train=no, search=yes, ai-input=yes`. Existing AI-bot rules kept. |
| Link header | `vercel.json` on `/` | `/llms.txt` (describedby), `/md/index.md` (alternate, text/markdown), `/.well-known/api-catalog` (api-catalog), `/services` (service-doc). |
| Markdown negotiation | `middleware.js` + `md/**.md` mirrors | When `Accept` includes `text/markdown` and the path has no extension, middleware serves `/md/<path>.md` (adds `x-markdown-source`); otherwise it passes through. `vercel.json` sets `Content-Type: text/markdown`, `Vary: Accept` and CORS on `/md/*`. The earlier Accept-header rewrites were removed; middleware alone handles it. `md/` is generated by `build_agent_files.py`. |
| API catalog (RFC 9727) | `/.well-known/api-catalog` + `/openapi.json` | Linkset for the real `POST /api/contact`, served as `application/linkset+json`; `openapi.json` (OpenAPI 3.1) served as `application/openapi+json`. |
| Agent Skills | `/.well-known/agent-skills/index.json` + `request-a-quote/SKILL.md` | One real skill: pick a service/plan and send an inquiry. The `sha256` digest is written by `build_agent_files.py`; `.gitattributes` forces LF under `.well-known/**` so the digest stays stable. |
| AI catalog | `/.well-known/ai-catalog.json` + `<link rel="ai-catalog">` in `index.html` | Points to `openapi.json` and the SKILL.md with representative queries. |
| WebMCP (declarative) | `contact.html` form | `toolname="request-tensix-quote"`, `tooldescription`, `toolparamdescription` per field, hidden `plan` input (filled from `?plan=` by `script.js`; `api/contact.js` prefixes `Plan: <slug>` to the subject). |

**Intentionally NOT published** (there is no real endpoint or capability behind them, and fake files would be dishonest and could mislead agents): OAuth/OIDC discovery, oauth-protected-resource, auth.md, MCP server card, A2A agent card, commerce/payment protocols (x402, MPP, UCP, ACP), Web Bot Auth. **DNS-AID SVCB records are also not published**: there is no A2A/MCP endpoint to point them at, so that scanner check stays an honest fail.

**DNS records the owner adds in the Cloudflare dashboard:**
- TXT `_catalog._agents.tensix.in` = `"url=https://www.tensix.in/.well-known/ai-catalog.json"`
- TXT `_catalog._agents.www.tensix.in` = `"url=https://www.tensix.in/.well-known/ai-catalog.json"`
- Enable DNSSEC (DNS &rarr; Settings) and add the DS record at the registrar.

**`.vercelignore` is an allowlist.** It ignores `/*` and re-includes only public site files (`*.html`, `assets/`, `blogs/`, `services/`, `md/`, `api/`, `.well-known/`, `script.js`, `middleware.js`, `robots.txt`, sitemaps, `llms*.txt`, `openapi.json`, verification `.txt` keys, `vercel.json`, `package*.json`).
- **Every new public file or folder must be added there**, or it will 404 in production.
- Private notes, memory, knowledge base and scripts must never deploy (`/CLAUDE.md`, `/01_Memory/...`, `*.py` must return 404).
- **The GitHub repo is public:** anything committed, including history (e.g. `CLIENT_CASE_STUDIES_PRIVATE.md`, `MASTER_PROMPT.md`), is readable there regardless of `.vercelignore`. Keep truly private notes out of git.

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
