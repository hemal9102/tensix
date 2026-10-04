"""Step 4: Convert patterns into exact prescriptions (file, field, old → new)"""
import json
from pathlib import Path

prescriptions = [
    {
        "pattern": "E: NAP Standardization",
        "priority": 1,
        "changes": [
            {
                "file": "all HTML files",
                "field": "streetAddress in JSON-LD",
                "old": "varies: 'Navrangpura' OR 'Navrangpura, C.G. Road Corridor' OR 'Gota - Navrangpura Corridor'",
                "new": "\"Navrangpura, Ahmedabad\" (everywhere except Gota page)",
                "rationale": "One canonical street address helps Google reconcile entities"
            },
            {
                "file": "all HTML files",
                "field": "addressLocality in JSON-LD",
                "old": "varies: 'Ahmedabad' OR 'Navrangpura' OR 'Navrangpura, Ahmedabad'",
                "new": "\"Ahmedabad\" (always, on every page)",
                "rationale": "City should never be the neighbourhood. Reconciliation needs atomic values"
            },
            {
                "file": "all HTML files",
                "field": "postalCode in JSON-LD",
                "old": "varies: '380009' OR '382481' (on Gota page)",
                "new": "\"380009\" (Navrangpura) everywhere except Gota → \"382481\" (Gota) if office exists",
                "rationale": "One postcode per location. Decide: Gota office or not?"
            }
        ]
    },
    {
        "pattern": "D: Gota Location Conflict",
        "priority": 2,
        "changes": [
            {
                "file": "best-software-company-in-gota.html",
                "decision": "DECISION POINT: Do you have a real office at Gota coords 23.1118, 72.5470?",
                "if_no": {"field": "all geo fields", "action": "Change to canonical 23.0366, 72.5615 + add text: 'We serve Gota via remote'"},
                "if_yes": {"field": "GBP", "action": "Create separate Google Business Profile for Gota location + link it"}
            }
        ]
    },
    {
        "pattern": "B: Entity Not Explicit",
        "priority": 3,
        "pages": ["blogs.html", "contact.html", "frameworks.html", "gallery.html"],
        "change": {
            "field": "First <p> or <h1> description",
            "old": "Generic slogan without name/location/offering",
            "new": "TEMPLATE: 'TENSIX is a software engineering studio based in Navrangpura, Ahmedabad. We [offering].'",
            "examples": [
                "contact.html: 'TENSIX is a software engineering studio in Navrangpura, Ahmedabad. Schedule a 30-min architecture call to discuss your project.'",
                "frameworks.html: 'TENSIX uses Node, FastAPI, React, and PostgreSQL. Our Navrangpura, Ahmedabad studio specializes in [what].'",
                "gallery.html: 'TENSIX (Navrangpura, Ahmedabad) has delivered software to [number] companies. See our work:'",
            ]
        }
    },
    {
        "pattern": "A: No Direct Answer to Query",
        "priority": 4,
        "pages": ["index.html (query: TENSIX)", "blogs.html (query: Articles), services.html (query: Services)"],
        "change": {
            "field": "First sentence or headline",
            "rule": "Must answer the page title/query WITHOUT clicking further",
            "old_bad": "'We engineer the future.' (slogan, no answer)",
            "new_good": "'TENSIX delivers production software + autonomous AI systems to Ahmedabad founders in 7-14 days.' (directly answers 'what is TENSIX')"
        }
    },
    {
        "pattern": "C: Unbacked Superlatives",
        "priority": 5,
        "pages": ["index.html", "about.html", "services.html", "team.html"],
        "find_replace": [
            {"old": "'elite engineering studio'", "new": "'software studio' + add: 'serving 18+ companies in Ahmedabad since 2026'"},
            {"old": "'best software company'", "new": "'fixed-scope software delivery: 7-14 days or refund'"},
            {"old": "'Top Software Development'", "new": "'Custom software + autonomous AI agents' (remove Top)"},
            {"old": "'Fastest indexing architecture'", "new": "'Documented on tensix.in + used for [case study]'"},
        ]
    }
]

print("=== STEP 4: PRESCRIPTIONS ===\n")
for i, p in enumerate(prescriptions, 1):
    print(f"{i}. {p['pattern']} (Priority {p.get('priority', '?')})")
    if "changes" in p:
        for c in p["changes"]:
            print(f"   File: {c.get('file', '?')}")
            print(f"   Field: {c.get('field', '?')}")
            print(f"   Old: {c.get('old', '?')[:80]}")
            print(f"   New: {c.get('new', '?')[:80]}")
            print()

# Export as JSON
with open("prescriptions.json", "w") as f:
    json.dump(prescriptions, f, indent=2)

print("\n✓ Prescriptions saved. Ready for Step 5: Verify (re-run citation_audit + geo-kernel after changes)")
