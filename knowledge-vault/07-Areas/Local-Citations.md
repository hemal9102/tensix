---
title: Local Citations & NAP Consistency
tags: [seo, local, area, todo]
updated: 2026-07-20
---

# Local Citations & NAP Consistency

**Purpose:** Track every external directory listing for JobRecruitment and keep NAP identical across all of them.

**Summary:** Inconsistent NAP (Name/Address/Phone) actively weakens local ranking and Map Pack trust. Verified 2026-07-20 by fetching each listing — **3 real mismatches found**, plus one listing that belongs to a different business entirely.

## Canonical NAP (source of truth — matches site schema)
- **Name:** JobRecruitment
- **Address:** Fairdeal house, B-910, Chimanlal Girdharlal Rd, nr. Swastik Cross Road, Shital Kunj Society, Vasant Vihar, Navrangpura, Ahmedabad, Gujarat **380009**
- **Phone:** +91 90998 76985
- **Geo:** 23.0366, 72.5615

## Audit — verified 2026-07-20

| Directory | Name | Address | Phone | Status |
|---|---|---|---|---|
| **PlacementIndia** | "Job Recruitment" | ✅ exact match, 380009 | ❌ `08048778688` | **Fix phone** |
| **Sulekha** | "jobrecruitment" | ❌ vague; **PIN 380006** (should be 380009); "**Farideal**" vs "Fairdeal" | ❌ none listed | **Fix address + PIN + add phone** |
| **JustDial** | — | — | — | Unverified (JS-rendered, fetch returned empty) |
| **Hotfrog** | — | — | — | Unverified (HTTP 403 on fetch) |
| **IndiaMART** `company/257585383` | ⛔ **"Atozgadgetz"** | different business | — | **NOT our entity — removed from `sameAs`** |

## Actions
- [ ] **PlacementIndia** — change phone to +91 90998 76985 (currently an IndiaMART-style tracking number).
- [ ] **Sulekha** — correct address to canonical, fix PIN 380006 → **380009**, fix "Farideal" → "Fairdeal", add phone, standardize name to "JobRecruitment".
- [ ] **JustDial / Hotfrog** — verify NAP manually in-browser (bot-blocked).
- [ ] **IndiaMART** — if a JobRecruitment listing exists separately, find its real URL; do NOT reuse the Atozgadgetz one.
- [ ] **Google Business Profile + reviews** — still the biggest remaining gap (Place1india has 550 reviews / 4.9★).

## Where these are used in code
Declared in `sameAs` of the `EmploymentAgency` schema (entity consolidation, **not** backlinks):
- `../../index.html` · `../../locality-template.php` · `../../job-consultancy-template.php`

Currently declared: LinkedIn, Instagram, JustDial, Sulekha, PlacementIndia, Hotfrog, WhatsApp. **IndiaMART deliberately excluded** (wrong entity).

## Lessons
- Always verify a directory URL actually resolves to *this* business before putting it in `sameAs` — a wrong entry teaches Google the wrong entity.
- `sameAs` aids entity consolidation; it does **not** add link equity.

## Related
- [[SEO]] · [[SEO-Ranking-Strategy]] · [[Home]]
