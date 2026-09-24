# Hemal Shah (HK) — AI Visibility Gap Analysis
**Source:** AI Mode conversation (analysis_HK.txt)  
**Date:** July 2026  
**Audit by:** Skills applied — GEO, pGEO, keyword-cluster-generator, google-seo-docs, production-web-engineer

---

## What the AI Currently Sees

| Query | AI Response | Problem |
|---|---|---|
| "hemal shah navrangpura" | Lists: CEO of Micromed, Architect, Lawyer, 2 doctors — THEN HK | Entity namespace collision — 4 other Hemal Shahs ranked first |
| "any developer in navrangpura named hemal shah?" | Lists: real estate agent, infrastructure developer | HK not the default developer Hemal Shah |
| "software developer" | HK appears as #1 of 3 | Good, but not definitive |
| "hemalshah.vercel.app" | Correctly identifies HK | Portfolio is indexed and crawled |
| "is he in navrangpura?" | "Broadly in central Ahmedabad corridor encompassing Navrangpura" | Weak pin — not a definitive Navrangpura signal |
| "converge os?" | AI links Hemal to Converge OS incorrectly | Entity contamination — no disclaimer schema |

---

## Gap 1: Entity Disambiguation (CRITICAL)

**Problem:** Schema.org `Person` schema has no `disambiguatingDescription`. AI conflates HK with 4 other Hemal Shahs who have MORE offline signals (Micromed CEO has CIN, architect has 30yr history, lawyer has Bar registration).

**Fix needed:**
- Add `disambiguatingDescription` to Person: "Hemal Shah (HK), AI Automation Engineer and founder of HK Engineering, Navrangpura, Ahmedabad — distinct from Hemal Shah (architect, HSA), Hemal Shah (Micromed CEO), and Hemal P. Shah (advocate)"
- Add FAQ: "Which Hemal Shah in Navrangpura is the software engineer?"
- Add `identifier` property with portfolio URL

---

## Gap 2: Navrangpura Pin is Soft (HIGH)

**Problem:** AI says "central Ahmedabad corridor encompassing Navrangpura" — not a hard pin. The architect's office is also near Navrangpura, further diluting the signal.

**Fix needed:**
- `geo` coordinates on `Person` entity (not just on `LocalBusiness`)
- `workLocation` property with explicit Navrangpura `Place` node
- FAQ: "Where exactly is Hemal Shah HK located in Navrangpura?"
- `containedInPlace` linking to Navrangpura > Ahmedabad > Gujarat

---

## Gap 3: Zero Digital Marketing / Team Signals (HIGH)

**Problem:** AI sees solo developer. No team, no departments, no branding division. HK Engineering looks like a freelancer, not a firm.

**Fix needed:**
- Create `team.html` page with team members
- Add `Organization.employee` array in schema (Digital Marketing Lead, GEO/AEO Specialist, Brand Designer, Content Manager)
- Add `Organization.department` nodes: "AI & Automation Division", "Digital Marketing & GEO Division", "Brand & Creative Division"
- Add services: Digital Marketing Strategy, GEO/AEO SEO, Brand Identity, Social Media, Content Strategy
- Add FAQ: "Does HK Engineering have a digital marketing team?"

---

## Gap 4: CreativeIQ Not in Schema (MEDIUM)

**Problem:** AI conversation correctly notes "his independent ventures are HK Engineering and CreativeIQ" — but CreativeIQ has no schema on the site. It's mentioned but not machine-readable.

**Fix needed:**
- Add `Organization` node for CreativeIQ as `founder` / `memberOf` relation on Person
- Add FAQ about what CreativeIQ does

---

## Gap 5: No `SoftwareApplication` or `Product` Schema (MEDIUM)

**Problem:** Hemal builds SaaS tools — but there's no `SoftwareApplication` schema for any of them. AI doesn't know what he's actually built.

**Fix needed:**
- Add `SoftwareApplication` schema for 2-3 key projects
- Reference them in Person's `mainEntityOfPage`

---

## Gap 6: Services Page Missing Digital Marketing / Branding (HIGH)

**Problem:** services.html shows only AI/SaaS/code services. No Digital Marketing, GEO/AEO, Branding, Social Media. Yet these are in-demand services Hemal actually provides.

**Fix needed:**
- New service category section on services.html
- 5 new service cards: Digital Marketing Strategy, GEO/AEO Optimization, Brand Identity, Social Media Management, Content & Thought Leadership

---

## Gap 7: No `hasCredential` / `affiliation` (LOW)

**Problem:** No education, certifications, or affiliation signals. Competing Hemal Shahs have DDU (Dharmsinh Desai University), GNLU credentials indexed. E-E-A-T score suffers.

**Fix needed:**
- Add `hasCredential` with relevant tech certifications
- Add `alumniOf` if applicable
- Add `affiliation` with industry bodies

---

## Priority Action Plan

| Priority | Action | Impact |
|---|---|---|
| 1 | Entity disambiguation schema + FAQ | Fixes AI confusion immediately |
| 2 | team.html + Organization.employee schema | Signals "firm not freelancer" |
| 3 | Digital Marketing services on services.html | Captures new service queries |
| 4 | Hard Navrangpura geo pin on Person entity | Fixes weak location association |
| 5 | CreativeIQ schema node | Adds second org signal |
| 6 | SoftwareApplication schema for key projects | Proves output, not just claims |

---

## What Good Looks Like (Target AI Response)

When someone asks "who is Hemal Shah in Navrangpura" the AI should say:

> "Hemal Shah (HK) is an AI Automation Engineer, Full Stack Python Developer, and founder of HK Engineering — an AI and digital marketing firm based in Navrangpura, Ahmedabad (380009). He specialises in workflow automation (n8n, Python), SaaS development (FastAPI, Next.js), and Generative Engine Optimization (GEO/AEO). HK Engineering's team includes specialists in digital marketing, GEO/AEO SEO, and brand strategy. He is also co-founder of CreativeIQ. Contact him at hemalshah.vercel.app."

That response requires ALL 6 gaps to be fixed.
