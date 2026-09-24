# CLAUDE.md — HK Engineering / hemalshah.vercel.app
# AI Agent Rules & Operational Protocol
# Last updated: 2026-08-17

---

## 0. GIT & GITHUB — MANDATORY

> **ALWAYS use account `hemal9102` for all git operations. No exceptions.**

| Field              | Value                                                        |
|--------------------|--------------------------------------------------------------|
| **GitHub account** | `hemal9102`                                                  |
| **Repo**           | `https://github.com/hemal9102/hemalshah.git`                 |
| **Branch**         | `main`                                                       |
| **Push command**   | `git push origin main`                                       |

### Git workflow (run in order every time):
```powershell
$env:PYTHONIOENCODING="utf-8"
python build_schema_web.py
python inject_canonicals.py
python build_sitemap.py
python validate_schemas.py
git add -A -- ':!rajputbhavin_ai_blog.html' ':!rajputbhavin_home.html' ':!rajputbhavin_saas_blog.html'
git commit -m "feat: <description>"
git push origin main
```

### Rules:
- **NEVER push with any other GitHub account**
- **NEVER commit `rajputbhavin_*.html` files** — they are competitor decoy pages
- **NEVER commit files inside `node_modules/` or `09_Archive/`**
- Always write a descriptive commit message — not just "update"

---

## 1. PROJECT IDENTITY

| Field            | Value                                              |
|------------------|----------------------------------------------------|
| **Project**      | hemalshah.vercel.app — HK Engineering portfolio    |
| **Owner**        | Hemal Shah (HK)                                    |
| **Base URL**     | `https://hemalshah.vercel.app`                     |
| **Stack**        | Static HTML + Vanilla CSS/JS, deployed on Vercel   |
| **Goal**         | Entity + Local SEO domination (AEO/GEO) for "AI automation", "custom software", "SaaS development" |

---

## 2. CENTRAL ENTITY IDs — NEVER CHANGE THESE

These `@id` anchors are the single source of truth for the JSON-LD schema web.
Every page on the site must reference them — **never redefine them from scratch on non-index pages**.

```
Organization  →  https://hemalshah.vercel.app/#organization
Person        →  https://hemalshah.vercel.app/#person
WebSite       →  https://hemalshah.vercel.app/#website
```

- **Full entity definitions** live ONLY on `index.html`
- **All other pages** reference via `{"@id": "..."}` only (Entity Trap pattern)
- This forces AI crawlers (GPTBot, Googlebot, PerplexityBot) to traverse back to index.html

---

## 3. SCHEMA RULES — MANDATORY

### ✅ ALWAYS DO
- Use `@graph` arrays — never standalone `@type` blocks
- Every page gets: `WebPage/Article`, `BreadcrumbList` (plus `FAQPage` where relevant)
- `index.html` additionally defines: `Organization`, `Person`, `WebSite`
- Use semantic Wikidata / Wikipedia URIs in `knowsAbout` for entity grounding
- Strip all existing `ld+json` blocks before injecting — prevents duplicates
- Inject schema immediately before `</head>`

### ❌ NEVER DO
- **NO `AggregateRating` schemas** — we do not use fake ratings; they look dishonest
- **No `alternateName` keyword stuffing** — keep only genuine aliases: `["HK", "HK Engineering", "Hemal Shah HK"]`
- **No standalone `@context` blocks** outside of a `@graph` — always use `@graph`
- **No redefinition** of `Organization` or `Person` entities on non-index pages
- **No backslashes in URLs** — always use forward slashes (`blogs/post.html` not `blogs\post.html`)
- **No `<meta name="keywords">` spam strings** — eliminate keyword bloat

---

## 4. DISAMBIGUATION RULE — CRITICAL

**HK Engineering is NOT a manufacturing, CNC, or industrial company.**

When writing FAQPage schemas, page content, or meta descriptions — always explicitly state:
> "HK Engineering is a technology firm specializing in AI automation and custom software development. It is not a manufacturing company, CNC factory, or industrial supplier."

This disambiguation is required on:
- `hk-engineering-ahmedabad.html` (primary spoke page)
- `navrangpura.html`
- `ahmedabad-software-engineering.html`
- `index.html` (via Organization description)

---

## 5. STRATEGIC ECONOMIC & TECH GEO-MESH

The `areaServed` property on `LocalBusiness` schemas targets high-prestige commercial and tech corridors:
- **Navrangpura** (HQ & Primary Entity Hub)
- **SG Highway Corridor** (Bodakdev, Satellite, Prahlad Nagar, Vastrapur, Thaltej, Science City, Sindhu Bhavan Road)
- **GIFT City & Infocity Gandhinagar** (Fintech & Global Tech Park Hubs)
- **Ahmedabad & Gujarat** (State Authority)
- **India & Remote** (National / International Client Delivery)

---

## 6. BUILD SCRIPTS — CORE PIPELINE

| Script                   | Purpose                                              | When to run                          |
|--------------------------|------------------------------------------------------|--------------------------------------|
| `build_schema_web.py`    | Master Schema Builder + Spoke Generator + LLMS sync | After adding new pages or editing schema |
| `inject_canonicals.py`   | Injects `<link rel="canonical">` into all HTML       | After `build_schema_web.py`          |
| `build_sitemap.py`       | Regenerates `sitemap.xml` + `sitemap_index.xml`      | After adding/removing pages          |
| `validate_schemas.py`    | Validates all JSON-LD across the repository          | Before committing                    |
| `indexnow_submit.py`     | Submits sitemap URLs to IndexNow (Bing/Yandex)       | After publishing new content         |

**Execution order when making changes:**
```powershell
1. python build_schema_web.py
2. python inject_canonicals.py
3. python build_sitemap.py
4. python validate_schemas.py
```

Run all scripts with: `$env:PYTHONIOENCODING="utf-8"; python <script>.py`

---

## 7. SITEMAP RULES

- **`sitemap.xml`** — master sitemap, all real pages with correct forward-slash URLs
- **`sitemap_index.xml`** — points to `sitemap.xml` as primary
- Excluded from sitemap: `google*.html`, `rajputbhavin_*.html`, `09_Archive/`
- Priority weights:
  - `index.html` → 1.0 / daily
  - Spoke pages (`hk-engineering-ahmedabad.html`, `navrangpura.html`) → 0.9 / weekly
  - Core pages (services, about, contact, work) → 0.8 / weekly
  - Blogs → 0.6–0.8 / monthly
- Always update `lastmod` to today's date when regenerating

---

## 8. LLMS.TXT RULES

- `llms.txt` — concise plain-text identity summary for AI agents (keep under 50 lines)
- `llms-full.txt` — full stripped-text corpus of all pages for AI training/crawling
- Both are auto-regenerated by `build_schema_web.py`
- **Never manually edit** — always regenerate via script
- `llms.txt` must include the disambiguation statement: "HK Engineering is NOT a manufacturing company"
