"""
fix_navrangpura_seo.py
Apply GEO/AEO + Local SEO targeting for "Hemal Shah Navrangpura" across all portfolio pages.

Fixes:
  1. Broken JSON-LD syntax (double commas, missing commas after areaServed/address blocks)
  2. Person.address → adds streetAddress: Navrangpura
  3. Organization.areaServed → adds Navrangpura neighborhood
  4. geo.placename → Navrangpura, Ahmedabad
  5. geo.position / ICBM → Navrangpura coordinates (23.0366, 72.5615)
  6. keywords meta → appends Navrangpura terms
  7. LocalBusiness JSON-LD → injected once on index.html only
"""

import os, re

ROOT = r"H:\portfolio_website\hemalshah"

# ── Navrangpura coords ────────────────────────────────────────────────────────
NAV_LAT  = "23.0366"
NAV_LNG  = "72.5615"
NAV_POS  = f"{NAV_LAT};{NAV_LNG}"
NAV_ICBM = f"{NAV_LAT}, {NAV_LNG}"

LOCAL_BUSINESS_SCHEMA = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "@id": "https://hemalshah.vercel.app/#localbusiness",
  "name": "Hemal Shah – AI Automation Engineer",
  "alternateName": "HK Engineering",
  "url": "https://hemalshah.vercel.app/",
  "image": "https://hemalshah.vercel.app/assets/favicon.png",
  "description": "Hemal Shah is an AI Automation Engineer and Full Stack Python Developer based in Navrangpura, Ahmedabad. Services include SaaS development, workflow automation, GEO/AEO semantic SEO, and custom web scraping.",
  "telephone": "+91-9000000000",
  "email": "contact@hemalshah.dev",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Navrangpura",
    "addressLocality": "Ahmedabad",
    "addressRegion": "Gujarat",
    "postalCode": "380009",
    "addressCountry": "IN"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 23.0366,
    "longitude": 72.5615
  },
  "areaServed": [
    {"@type": "City",  "name": "Ahmedabad"},
    {"@type": "State", "name": "Gujarat"},
    {"@type": "Country", "name": "India"},
    {"@type": "AdministrativeArea", "name": "Navrangpura"}
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "AI & Tech Services",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "AI Workflow Automation"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "SaaS Development"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "GEO / AEO Semantic SEO"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Full Stack Python Development"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Custom Web Scraping & Automation"}}
    ]
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
    "opens": "09:00",
    "closes": "20:00"
  },
  "priceRange": "₹₹",
  "sameAs": [
    "https://github.com/hemal9102",
    "https://www.linkedin.com/in/hemal-shah-49a728362/"
  ]
}
</script>"""


def fix_json_syntax(html: str) -> str:
    """Fix double-comma and missing-comma bugs inserted by inject_hemal_shah_schema.py"""
    # Fix: "name": "HK Engineering",, → single comma
    html = re.sub(r'"name":\s*"HK Engineering",,', '"name": "HK Engineering",', html)
    html = re.sub(r'"name":\s*"Hemal Shah",,', '"name": "Hemal Shah",', html)

    # Fix: areaServed: [...] missing comma before "url":
    html = re.sub(
        r'("areaServed"\s*:\s*\[[^\]]*\])\s*\n(\s*"url"\s*:)',
        r'\1,\n\2',
        html
    )
    # Fix: "address": {...} missing comma before "alternateName":
    html = re.sub(
        r'("address"\s*:\s*\{[^}]*\})\s*\n(\s*"alternateName"\s*:)',
        r'\1,\n\2',
        html
    )
    return html


def upgrade_person_address(html: str) -> str:
    """
    Replace Person address block to add streetAddress: Navrangpura
    and use postalCode for Navrangpura.
    """
    old_addr = (
        r'"address":\s*\{"@type":\s*"PostalAddress",\s*'
        r'"addressLocality":\s*"Ahmedabad",\s*'
        r'"addressRegion":\s*"Gujarat",\s*'
        r'"addressCountry":\s*"India"\}'
    )
    new_addr = (
        '"address": {"@type": "PostalAddress", '
        '"streetAddress": "Navrangpura", '
        '"addressLocality": "Ahmedabad", '
        '"addressRegion": "Gujarat", '
        '"postalCode": "380009", '
        '"addressCountry": "IN"}'
    )
    return re.sub(old_addr, new_addr, html)


def upgrade_org_area_served(html: str) -> str:
    """Add Navrangpura to Organization.areaServed"""
    old = (
        r'"areaServed":\s*\[\{"@type":\s*"City",\s*"name":\s*"Ahmedabad"\},\s*'
        r'\{"@type":\s*"State",\s*"name":\s*"Gujarat"\},\s*'
        r'\{"@type":\s*"Country",\s*"name":\s*"India"\}\]'
    )
    new = (
        '"areaServed": ['
        '{"@type": "City", "name": "Ahmedabad"}, '
        '{"@type": "State", "name": "Gujarat"}, '
        '{"@type": "Country", "name": "India"}, '
        '{"@type": "AdministrativeArea", "name": "Navrangpura"}]'
    )
    return re.sub(old, new, html)


def upgrade_geo_meta(html: str) -> str:
    """Update geo meta tags to Navrangpura"""
    html = re.sub(
        r'(<meta\s+content=")[^"]*"(\s+name="geo\.placename"/>)',
        r'\1Navrangpura, Ahmedabad"\2',
        html
    )
    html = re.sub(
        r'(<meta\s+content=")[^"]*"(\s+name="geo\.position"/>)',
        rf'\g<1>{NAV_POS}"\2',
        html
    )
    html = re.sub(
        r'(<meta\s+content=")[^"]*"(\s+name="ICBM"/>)',
        rf'\g<1>{NAV_ICBM}"\2',
        html
    )
    return html


def upgrade_keywords(html: str) -> str:
    """Append Navrangpura keywords if not already present"""
    nav_kw = "Hemal Shah Navrangpura, AI Engineer Navrangpura, Python Developer Navrangpura Ahmedabad, HK Engineering Navrangpura, Software Developer Navrangpura"
    def replacer(m):
        existing = m.group(1)
        if "Navrangpura" in existing:
            return m.group(0)
        return f'<meta content="{existing}, {nav_kw}" name="keywords"/>'
    return re.sub(
        r'<meta content="([^"]+)" name="keywords"/>',
        replacer,
        html
    )


def inject_local_business(html: str) -> str:
    """Inject LocalBusiness schema before </head> — only if not already present"""
    if "ProfessionalService" in html or "#localbusiness" in html:
        return html
    return html.replace("</head>", LOCAL_BUSINESS_SCHEMA + "\n</head>", 1)


def process_file(path: str, is_index: bool):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    original = html
    html = fix_json_syntax(html)
    html = upgrade_person_address(html)
    html = upgrade_org_area_served(html)
    html = upgrade_geo_meta(html)
    html = upgrade_keywords(html)

    if is_index:
        html = inject_local_business(html)

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  [UPDATED] {os.path.relpath(path, ROOT)}")
    else:
        print(f"  [no change] {os.path.relpath(path, ROOT)}")


def main():
    print("=== fix_navrangpura_seo.py ===\n")
    for root, dirs, files in os.walk(ROOT):
        # skip hk subfolder and skills
        dirs[:] = [d for d in dirs if d not in ("hk", "skills", "resources", "assets")]
        for fname in files:
            if not fname.endswith(".html"):
                continue
            if fname.startswith("google"):   # verification files
                continue
            fpath = os.path.join(root, fname)
            is_index = (fname == "index.html" and root == ROOT)
            process_file(fpath, is_index)
    print("\nDone.")


if __name__ == "__main__":
    main()
