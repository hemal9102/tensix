# 15 - Competitor Keyword Intelligence & TenSix Ranking Battle Plan

> **Document ID:** `OUTFLANK-15`
> **Date:** 2026-10-15
> **Related Architecture:** [[05 - Competitor Reverse-Engineering & Ranking Outflank Endpoints]], [[09 - The 48 Algorithmic Variables for Position 0, FAQ Schemas & AI Citation Dominance]], [[01 - Google Autocomplete & Real-Time Intent Harvesting Engine]]
> **Tags:** `#competitor-analysis` `#keyword-intelligence` `#rank-tracking` `#serpapi` `#apify` `#gsc` `#ga4` `#typesafe-jev` `#battle-plan` `#tensix`

---

## 🎯 Executive Summary

Research run on **2026-10-15** to answer one question: why does `tensix.in` rank only for its own brand name, and what must change to win CTO/CEO-level and high-value ("boring but rich") B2B keywords in Ahmedabad / India.

Three live, calibrated data sources were combined — no guesswork:

1. **Rank reality (SerpAPI → Apify):** where TenSix actually ranks on Google (India, then Ahmedabad-local) for 44 target keywords.
2. **Ground truth (Google Search Console + GA4):** TenSix's own real impressions, positions and page traffic — not scraped estimates.
3. **Calibrated judgment (TypeSafe Jev decisions model):** every competitor + keyword scored with typed Choice/Noul/Score primitives against the 48-variable Position-0 rubric from [[09 - The 48 Algorithmic Variables for Position 0, FAQ Schemas & AI Citation Dominance]].

**Verdict:** TenSix's pages are technically sound (answer blocks, FAQ schema, Service JSON-LD already present), but Google sees **zero impressions** for every money keyword — the site has no authority/relevance signal on them. The opportunity is the **CTO / tech-leadership cluster**: highest ticket, lowest competition, and TenSix already offers the service.

---

## 📊 1. Rank Reality — What Google Shows Today

### Google India (SerpAPI, top-100, 44 keywords)
Only brand terms rank. Every non-brand money keyword (fractional CTO, custom SaaS/CRM, AI agents, automation, scraping, devops, email, website dev) is **absent from the top 100**.

| Query | Position | Note |
| :--- | :--- | :--- |
| `tensix` | #2 | brand |
| `hemal shah tensix` | #1 | brand |
| all 40+ money keywords | — | not in top 100 |

### Google Ahmedabad-local (Apify Google Search Scraper, top-10)
Local SERP is slightly kinder — `tensix ahmedabad` hits #1, `hemal shah tensix` #3, and `tensix.in` surfaces in the top 10 for 4 keywords (vs 0 in the India run). Money keywords still absent.

**Top aggregated Ahmedabad competitors (appearances across 44 keywords):**

| Domain | Appears | Avg pos | Type |
| :--- | :--- | :--- | :--- |
| instagram.com | 9 | 2.4 | social |
| reddit.com | 8 | 4.6 | social |
| justdial.com | 8 | 5.0 | directory |
| dir.indiamart.com | 7 | 2.4 | directory |
| clutch.co | 6 | 4.3 | directory |
| **kanhasoft.com** | 5 | 4.0 | **real studio rival** |
| designrush.com | 5 | 6.4 | directory |
| **dngwebdeveloper.com** | 4 | 3.8 | **real studio rival** |
| tensix.in | 4 | 5.2 | us |

Half the top slots are **directories / social** — the correct move there is to get *listed*, not to outrank with a service page.

---

## 📡 2. Ground Truth — TenSix's Own Google Data (GSC + GA4, 90 days)

### Search Console (`sc-domain:tensix.in`)
Only **13 queries** generated any impressions. 34 impressions total, ~32 of them brand (`tensix`). Blog content (supabase pgvector, whatsapp system design, n8n) ranks pos 3–40 but attracts engineers, not buyers, and earns no clicks. Money queries sit at pos 67–100 — indexed but buried.

### GA4 (property `550016993`, "HK engineering")
354 users in 90 days; **309 (87%) land on the homepage**. Service pages see 1–5 users each. **keyEvents (conversions) = 0 on every page.** Traffic is brand/direct; CTO/CEO discovery and conversion are effectively zero.

---

## 🧮 3. Calibrated Competitor Judgment (TypeSafe Jev)

Each competitor result was scored by the Jev decisions model (`typesafe/jev-1.13`, OpenRouter `/api/alpha/decisions`) using typed primitives against the 48-variable rubric:

| Judgment | Type | What it measures |
| :--- | :--- | :--- |
| `result_type` | choice | studio / freelancer / directory / marketplace / editorial / big-brand |
| `intent_match` | choice | direct / partial / mismatch vs buyer intent |
| `beatability` | score 0–3 | entrenched → hard → winnable → soft |
| `answer_envelope` | noul | tight Position-0 answer present? (Layer 1) |
| `faq_signal` | noul | FAQ / PAA structure present? (Layer 3) |
| `info_density` | score 0–2 | generic → concrete checkable facts (Layer 4) |
| `local_corridor` | score 0–3 | Ahmedabad / local relevance (Layer 5) |
| `contestable_format` | noul | outrank head-to-head vs get-listed |

**Pattern across all keywords:** ranking competitor pages consistently score **low on answer_envelope and faq_signal** — a direct, honest Position-0 card + FAQPage schema is TenSix's cheapest lever to out-rank them.

---

## 🧭 4. Free Keyword-Intent Clustering (8 Rival Studios)

Reconnaissance of 8 real studio rivals (kanhasoft, dngwebdeveloper, duplextech, suntecindia, areinfotech, esparkinfo, orangemantra, greencubes) using only free endpoints (techniques from [[05 - Competitor Reverse-Engineering & Ranking Outflank Endpoints]]):

- **Sitemap crawl (`curl.exe -sL`)** → 4,584 pages across 8 rivals; slugs + `<lastmod>`.
- **Title/H1 scan** → what each rival actually targets.
- **Google Suggest** (`suggestqueries.google.com`, free, no key) → 606 real search stems.
- **Header fingerprint (`curl.exe -sIL`)** → TTFB / cache / server.
- **Jev clustering** → 432 relevant keywords (junk filtered) classified by intent + value.

### Cluster results

| Cluster | Keywords | High-value | Note |
| :--- | :--- | :--- | :--- |
| **CTO / Tech Leadership** | 4 | 3 | highest ticket, lowest competition |
| Money Service (build) | 120 | 36 | custom CRM/SaaS/ERP dominate |
| Comparison / Alternatives | 16 | 1 | "best/top companies" listicles |
| Local (Ahmedabad) | 7 | 0 | weak rival local signal = TenSix edge |
| Informational | 59 | 0 | how-to/definition |
| Irrelevant | 14 | 0 | filtered junk |

### Speed edge (TTFB fingerprint)
`kanhasoft.com` (0.86s), `suntecindia.com` (0.84s) and `areinfotech.com` (1.20s) are slow. TenSix's static edge (<50ms) is a direct Core Web Vitals lever against them (doc §1C/§6).

---

## 🚀 5. TenSix Priority Action Plan

1. **Own the CTO / leadership cluster.** Build dedicated, honest pages for `fractional cto`, `fractional cto india`, `fractional cto cost`. Highest ticket, lowest competition, and the service already exists.
2. **Win local intent.** Rivals' pages lack strong Ahmedabad / Navrangpura signal — add genuine local context (48-variable Layer 5 corridors).
3. **Out-specify money-service keywords** (custom CRM / SaaS / ERP, AI agent, automation). Each page needs a **45–55 word Position-0 answer card + FAQPage schema + fixed-price plan** (doc §4; CLAUDE.md §4.2 / §5). Real figures only — no fabricated stats/guarantees.
4. **Capture comparison intent.** 16 "best/top companies" queries exist; extend the existing `tensix-vs-traditional-agencies` page honestly.
5. **After publishing, force indexing** via Google Indexing API + IndexNow (doc §5) for crawl within minutes.

---

## ⚙️ 6. Reusable Pipeline (this repo)

| Component | Path | Purpose |
| :--- | :--- | :--- |
| Rank checker | `check_ranks.py` | SerpAPI Google-India rank sweep |
| Battle plan | `keyword_battle_plan.py` | SerpAPI/Apify + GSC + GA4 + Jev per-keyword competitor judgment & action plan |
| Competitor outflank | `competitor_outflank.py` | Free curl sitemap crawl + Google Suggest + Jev intent/value clustering of rival studios |
| SERP cache | `serp_cache.json` | cached SERPs (keyed by location/depth/keyword) to protect API quota |
| Reports | `keyword_battle_plan_*.md`, `competitor_outflank_plan.md` | dated outputs |

**Data sources & keys** (all via env vars / flags, never hardcoded): `SERPAPI_KEY`, `APIFY_TOKEN`, `OPENROUTER_API_KEY` (Jev), Google service-account JSON for GSC + GA4 (`sc-domain:tensix.in`, GA4 property `550016993`).

Example runs:
```powershell
python keyword_battle_plan.py --provider apify --location "Ahmedabad,Gujarat,India" --creds <sa.json> --gsc-site sc-domain:tensix.in --ga4-property 550016993
python competitor_outflank.py --limit-pages 35 --suggest-seeds 15
```

---
**Backlinks:**
* [[00 - Index|Domain Index]]
* [[05 - Competitor Reverse-Engineering & Ranking Outflank Endpoints|05 - Competitor Reverse-Engineering]]
* [[09 - The 48 Algorithmic Variables for Position 0, FAQ Schemas & AI Citation Dominance|09 - The 48 Algorithmic Variables]]
