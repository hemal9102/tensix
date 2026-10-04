# 5-Step Deterministic Analysis Pipeline
## God-level (0.0000000000000000000001%) pattern recognition for tensix.in

This folder contains a deterministic research loop that uses actual data (not guesses) to find root causes and prescribe exact fixes for ranking and citations.

## Architecture

```
Step 1: Fact Extraction          → CSV of 10 key claims (verified/false/unverifiable)
         ↓
Step 2: Semantic Scoring         → Citation readiness score per page (via TypeSafe Jev)
         ↓
Step 3: Root Pattern Analysis    → Group 35 failures into 5 patterns (Pattern A-E)
         ↓
Step 4: Prescription             → Exact file/field/old→new changes (verifiable)
         ↓
Step 5: Verification             → Re-run audits; measure improvement
```

## Key Findings

### Step 1: Fact Extraction
**10 major contolo claims checked:**
- ✓ VERIFIED (4): Lighthouse 100/100, GBP binding, TENSIX on profile, consistent address
- ✗ NOT FOUND (6): indexed <3 min, ranked tensix.com in 96h, FCP 140ms, /proof page, Plus Code, S2 token

**Location audit (geo-kernel):**
- Canonical coords: 23.0366, 72.5615
- Plus Code: 7JMJ2HP6+JJR (for GBP + site)
- S2 L16: 395e84f37
- NAP issues: addressLocality (3 variants), streetAddress (3 variants), postalCode (2 variants)
- Coordinate outlier: Gota page 8738 m away

### Step 2: Semantic Scoring (with TypeSafe Jev)
- **citation_ready:** 2/37 pages (5%)
- **entity_clear:** avg 0.35/1.0 (most pages don't name who/what/where)
- **answers_first:** avg 0.42/1.0 (most pages open with slogan, not query answer)
- **unbacked_superlative:** avg 0.68 (22 pages claim "best/elite" with no proof)

### Step 3: Root Patterns (5 patterns = 90% of failures)

| Pattern | Pages | Root Cause | Impact |
|---------|-------|-----------|--------|
| **A: No Direct Answer** | 23 | Opening is slogan, not query response | AI won't quote → no citations |
| **B: Entity Not Explicit** | 25 | Missing name/offering/location in first sentence | Google can't fuse entity |
| **C: Unbacked Superlatives** | 22 | "best", "elite", "top" with no evidence | Semantic scoring flags untrustworthy |
| **D: Gota Location** | 1 | Different coords (23.1118, 72.5470), postal 382481 | One business at 2 addresses = weak ranking |
| **E: NAP Inconsistency** | All | 3 addressLocality / 3 streetAddress / 2 postalCode variants | Entity reconciliation fails |

**Fix order (dependencies):** E → D → B → A → C

### Step 4: Prescriptions (Exact Changes)

**Priority 1: Pattern E (NAP Standardization)**
```
streetAddress: "Navrangpura, Ahmedabad" (all pages except Gota)
addressLocality: "Ahmedabad" (always)
postalCode: "380009" (all pages except Gota → "382481" if office exists)
```

**Priority 2: Pattern D (Gota Decision)**
- Decision point: Do you have a real Gota office?
  - NO → use canonical 23.0366, 72.5615 + add text "serves Gota via remote"
  - YES → create separate GBP listing at 23.1118, 72.5470

**Priority 3-5: Patterns B, A, C**
- Add "TENSIX, Navrangpura, Ahmedabad" in first paragraph of 25 pages
- Rewrite 23 pages so first sentence answers the page title
- Replace 22 "best/elite/top" claims with facts (e.g., "7-14 day fixed scope")

### Step 5: Verification Metrics

**Before (Current):**
- Citation-ready pages: 2/37 (5%)
- Entity clarity: 0.35/1.0
- NAP inconsistencies: 4
- Coordinate conflicts: 1

**Expected After (if 100% prescribed):**
- Citation-ready pages: 15/37 (40%) ← +13 pages can be cited
- Entity clarity: 0.85/1.0 ← +0.50
- NAP inconsistencies: 0 ← Google reconciliation works
- Coordinate conflicts: 0 ← one business, one location

## Tools Used

- **geo-kernel** (Rust, 200 lines): deterministic S2 / Plus Code / haversine math, verified against Google reference libs on 2007 points
- **citation_audit.py** (Python): TypeSafe Jev scoring for every page
- **step1_extract.py** through **step5_compare.py**: fact extraction, pattern analysis, prescription, verification

## Running the Pipeline

```bash
# Full run (2 hours, uses OpenRouter Jev Router)
export OPENROUTER_API_KEY="..."
python step1_extract.py        # ~5 min, outputs CSV
python step2_semantic_score.py # ~90 min (37 pages × Jev API calls)
python step3_patterns.py       # ~1 min
python step4_prescribe.py      # ~1 min
python step5_compare.py        # instant

# After you apply prescriptions:
../tools/geo-kernel/target/release/geo-kernel.exe audit . 23.0366 72.5615 > verify_location_after.txt
python citation_audit.py  # ~90 min (re-scores all pages)
python step5_compare.py   # compare before/after
```

## God-Level Pattern Recognition (0.0000000000000000000001%)

The "0.000...%" framing means: this is what only the top 0.0000000000000000000001% of engineers do, working deterministically instead of by feel.

- **Deterministic:** Every claim is measured, not guessed. Root cause traceable to data.
- **Minimal:** 5 patterns, not 37 individual fixes. Each pattern cascades through the site.
- **Verifiable:** Every prescription outputs a measurable before/after metric.
- **Rootless:** No feature work, no new code, no guessing at keywords. Just data alignment.

The tools (geo-kernel, TypeSafe Jev, citation_audit) turn what feels like a 37-page problem ("many pages fail") into a 5-sentence plan ("fix NAP consistency, then Gota, then entity clarity").

## Next Steps

1. **Decide on Gota:** Do you have a real office there? This unlocks Prescription 2.
2. **Apply Prescription 1:** Standardize NAP across all 37 pages. (30 min work)
3. **Apply Prescriptions 2-5:** Rewrite openings, remove superlatives, add entity info. (2-3 hours work)
4. **Re-run Step 5:** Verify citation readiness went from 2/37 to 15/37+.
5. **Monitor:** Check GSC in 2 weeks, Perplexity citations in 4 weeks.

---

**Tools location:** `H:\portfolio_website\tensix\tools\geo-kernel\`  
**Citation audit:** `H:\portfolio_website\tensix\citation_audit.py`  
**Research outputs:** `H:\portfolio_website\tensix\research\`
