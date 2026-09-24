"""
Final cross-check fix — hemalshah portfolio
Skills applied: code-review, ponytail-review, structured-data-validator, geo-optimization, google-seo-docs

Issues fixed:
  [F1] Footer <p> "Co-Founder, CreativeIQ" on ALL 23 pages — unverified, remove
  [F2] index.html JSON-LD memberOf[] — CreativeIQ co-founder node — remove
  [F3] team.html JSON-LD description — "co-founder of CreativeIQ" — remove
  [F4] team.html visible text — "co-founder of CreativeIQ" — remove
  [F5] team.html footer <p> — "Co-Founder, CreativeIQ" — remove
  [F6] 3 blog titles with doubled "| Hemal Shah (HK) | Hemal Shah (HK)" suffix
  [F7] wr1.html canonical points to itself — duplicate of work.html — fix to work.html
  [F8] services.html + other inner pages: Person schema missing disambiguatingDescription & workLocation — add
"""

import os, re

ROOT = r"H:\portfolio_website\hemalshah"

HTML_FILES = []
for dirpath, _, filenames in os.walk(ROOT):
    if "node_modules" in dirpath: continue
    for fn in filenames:
        if fn.endswith(".html"):
            HTML_FILES.append(os.path.join(dirpath, fn))

fixed = 0

for filepath in sorted(HTML_FILES):
    rel = os.path.relpath(filepath, ROOT)
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    original = content

    # ------------------------------------------------------------------
    # F1: Footer <p> — remove "Co-Founder, CreativeIQ |" from all pages
    # Pattern: "Founder, HK Engineering | Co-Founder, CreativeIQ | AI Agent..."
    # ------------------------------------------------------------------
    content = content.replace(
        "Founder, HK Engineering | Co-Founder, CreativeIQ | AI Agent &amp; Full-Stack Python Engineer",
        "Founder, HK Engineering | AI Agent &amp; Full-Stack Python Developer"
    )
    # team.html footer variant
    content = content.replace(
        "HK Engineering — AI, Digital Marketing &amp; Branding | Navrangpura, Ahmedabad | Co-Founder, CreativeIQ",
        "HK Engineering — AI Automation &amp; Digital Marketing | Navrangpura, Ahmedabad"
    )

    # ------------------------------------------------------------------
    # F2: index.html memberOf — remove CreativeIQ node
    # ------------------------------------------------------------------
    MEMBEROF_OLD = '''        "memberOf": [
          {"@type": "Organization", "name": "HK Engineering", "@id": "https://hemalshah.vercel.app/#organization"},
          {"@type": "Organization", "name": "CreativeIQ", "description": "CreativeIQ is a co-founded venture by Hemal Shah (HK) focused on creative intelligence, branding, and AI-driven content strategy."}
        ],'''
    MEMBEROF_NEW = '''        "memberOf": [
          {"@type": "Organization", "name": "HK Engineering", "@id": "https://hemalshah.vercel.app/#organization"}
        ],'''
    content = content.replace(MEMBEROF_OLD, MEMBEROF_NEW)

    # ------------------------------------------------------------------
    # F3: team.html JSON-LD Person description
    # ------------------------------------------------------------------
    content = content.replace(
        '"Hemal Shah is the founder of HK Engineering and co-founder of CreativeIQ, based in Navrangpura, Ahmedabad. He leads all AI, SaaS, and GEO/AEO strategy."',
        '"Hemal Shah is the founder of HK Engineering, an AI automation and digital marketing firm based in Navrangpura, Ahmedabad. He leads all AI, SaaS, and GEO/AEO strategy."'
    )

    # ------------------------------------------------------------------
    # F4: team.html visible card text
    # ------------------------------------------------------------------
    content = content.replace(
        "Founder of HK Engineering and co-founder of CreativeIQ, based in Navrangpura, Ahmedabad.",
        "Founder of HK Engineering, an AI automation and digital marketing firm based in Navrangpura, Ahmedabad."
    )

    # ------------------------------------------------------------------
    # F6: Duplicate title suffixes on blog pages
    #     "Title | Hemal Shah (HK) | Hemal Shah (HK)" -> "Title | Hemal Shah (HK)"
    # ------------------------------------------------------------------
    content = re.sub(
        r'(\| Hemal Shah \(HK\)) \| Hemal Shah \(HK\)',
        r'\1',
        content
    )

    # ------------------------------------------------------------------
    # F7: wr1.html canonical — point to work.html (it's a duplicate page)
    # ------------------------------------------------------------------
    if "wr1.html" in filepath:
        content = content.replace(
            '<link href="https://hemalshah.vercel.app/wr1.html" rel="canonical"/>',
            '<link href="https://hemalshah.vercel.app/work.html" rel="canonical"/>'
        )
        # Also fix hreflang on wr1.html
        content = content.replace(
            '<link href="https://hemalshah.vercel.app/wr1.html" hreflang="en" rel="alternate"/>',
            '<link href="https://hemalshah.vercel.app/work.html" hreflang="en" rel="alternate"/>'
        )
        content = content.replace(
            '<link href="https://hemalshah.vercel.app/wr1.html" hreflang="x-default" rel="alternate"/>',
            '<link href="https://hemalshah.vercel.app/work.html" hreflang="x-default" rel="alternate"/>'
        )

    # ------------------------------------------------------------------
    # F8: Inner pages (not index.html) — Person schema missing
    #     disambiguatingDescription and workLocation — add them
    #     Pattern: pages that have minimal Person node (no disambiguating)
    # ------------------------------------------------------------------
    PERSON_MINIMAL = '''"award": "Proven Track Record in AI Engineering"
      }'''
    PERSON_FULL = '''"award": "Proven Track Record in AI Engineering",
        "disambiguatingDescription": "Hemal Shah (HK) is an AI Automation Engineer and Full Stack Python Developer, founder of HK Engineering, Navrangpura, Ahmedabad — distinct from Hemal Shah (architect, HSA) and other persons named Hemal Shah in Ahmedabad.",
        "workLocation": {
          "@type": "Place",
          "name": "Navrangpura, Ahmedabad",
          "geo": {"@type": "GeoCoordinates", "latitude": 23.0366, "longitude": 72.5615},
          "address": {"@type": "PostalAddress", "streetAddress": "Navrangpura", "addressLocality": "Ahmedabad", "addressRegion": "Gujarat", "postalCode": "380009", "addressCountry": "IN"}
        }
      }'''
    if PERSON_MINIMAL in content and "disambiguatingDescription" not in content:
        content = content.replace(PERSON_MINIMAL, PERSON_FULL)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        fixed += 1
        print(f"  Fixed: {rel}")

print(f"\nTotal files fixed: {fixed}")

# ------------------------------------------------------------------
# Verify: zero remaining unverified claims
# ------------------------------------------------------------------
print("\n--- Verification ---")
checks = {
    "CreativeIQ co-founder (footer)": "Co-Founder, CreativeIQ",
    "CreativeIQ co-founded (JSON-LD)": "co-founded venture",
    "co-founder of CreativeIQ (text)":  "co-founder of CreativeIQ",
    "Duplicate title suffix":           "Hemal Shah (HK) | Hemal Shah (HK)",
    "wr1 self-canonical":               'href="https://hemalshah.vercel.app/wr1.html" rel="canonical"',
}

all_clean = True
for label, pattern in checks.items():
    hits = []
    for filepath in HTML_FILES:
        with open(filepath, encoding="utf-8") as f:
            c = f.read()
        if pattern in c:
            hits.append(os.path.relpath(filepath, ROOT))
    if hits:
        print(f"  STILL PRESENT — {label}:")
        for h in hits: print(f"    {h}")
        all_clean = False
    else:
        print(f"  CLEAN — {label}")

if all_clean:
    print("\nALL CHECKS PASSED — site is clean.")
