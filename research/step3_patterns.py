"""Step 3: Identify 3-5 root patterns from all failures"""
import json

# Data from Steps 1-2
patterns = {
    "Pattern A: Missing direct answer": {
        "pages": ["index.html", "blogs.html", "services.html", "contact.html"],
        "symptom": "Opening is slogan/navigation, not a direct answer to the page's target query",
        "impact": "AI crawlers won't quote → no citations → rank lower in AI search",
        "fix": "First sentence must answer the title/query directly. Example: 'TENSIX builds production software for Ahmedabad founders in 7-14 days.' not 'We engineer the future.'",
        "verification": "citation_audit: answers_first >= 0.7"
    },
    "Pattern B: Entity not explicit (who/what/where)": {
        "pages": ["blogs.html", "contact.html", "frameworks.html", "gallery.html"],
        "symptom": "Opening doesn't say the company name, location, or what it does",
        "impact": "Google local ranking needs one clear identity. Ambiguous = low prominence.",
        "fix": "Every page's first paragraph must have: company name + offering + location. 'TENSIX (autonomous software studio, Navrangpura Ahmedabad)'",
        "verification": "citation_audit: entity_clear >= 0.7 + geo-kernel: all NAP fields have ONE value"
    },
    "Pattern C: Unbacked superlatives": {
        "pages": ["index.html", "about.html", "services.html", "saas-developer-ahmedabad.html"],
        "symptom": "'best', 'elite', 'top', 'fastest' without evidence in the same paragraph",
        "impact": "Semantic scoring flags as untrustworthy → lower citation probability",
        "fix": "Replace 'best' with facts: '7-14 day fixed scope' or '0-2 week delivery' or '18 clients in Ahmedabad'",
        "verification": "citation_audit: unbacked_superlative < 0.5"
    },
    "Pattern D: Gota page = second location": {
        "pages": ["best-software-company-in-gota.html"],
        "symptom": "Different address, postcode 382481, coords 23.1118 (8.7 km away)",
        "impact": "Google sees one business at two addresses → weakens Navrangpura ranking",
        "fix": "Either (a) use canonical Navrangpura address + say 'serves Gota' in text, OR (b) if you have a real Gota office, create a separate GBP listing",
        "verification": "geo-kernel: all coords same-L16 cell OR explicit disclaimer"
    },
    "Pattern E: NAP inconsistency = entity resolution failure": {
        "pages": ["all", "addressLocality has 3 versions", "streetAddress has 3 versions"],
        "symptom": "Ahmedabad vs Navrangpura, Gota-Navrangpura, C.G. Road variations",
        "impact": "Google's entity reconciliation engine can't fuse all pages into one business profile",
        "fix": "Standardize: pick ONE street address ('Navrangpura'), ONE city ('Ahmedabad'), ONE postcode ('380009'). Update JSON-LD schema everywhere.",
        "verification": "geo-kernel audit: each NAP field has exactly 1 unique value"
    }
}

print("=== STEP 3: ROOT PATTERN ANALYSIS ===\n")
for i, (pattern_name, p) in enumerate(patterns.items(), 1):
    print(f"{i}. {pattern_name}")
    print(f"   Pages affected: {', '.join(p['pages'][:2])}...")
    print(f"   Symptom: {p['symptom']}")
    print(f"   Impact on ranking: {p['impact']}")
    print(f"   Root fix: {p['fix']}")
    print(f"   Check: {p['verification']}")
    print()

print("=== PATTERN PRIORITY ===")
print("1. Pattern E (NAP) - blocks entity binding, affects ALL pages")
print("2. Pattern D (Gota) - creates rival location, confuses Google")
print("3. Pattern B (entity not explicit) - 25 pages fail")
print("4. Pattern A (no direct answer) - 23 pages fail")
print("5. Pattern C (superlatives) - 22 pages fail")
print("\nFix in this order: E → D → B → A → C. Each is independent once E is done.")

# Export for Step 4
import json
with open("patterns.json", "w") as f:
    json.dump(patterns, f, indent=2)
print("\n✓ Patterns saved to patterns.json for Step 4")
