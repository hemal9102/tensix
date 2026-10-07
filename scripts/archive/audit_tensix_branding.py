import os, re, json

ROOT = r"H:\portfolio_website\tensix"

branding_audit = {
    "total_pages": 0,
    "pages_with_tensix_title": [],
    "pages_with_tensix_meta": [],
    "pages_with_brand_schema": [],
    "entity_disambiguation_checks": {
        "tenstorrent_disambiguation": False,
        "tensix_consulting_disambiguation": False,
        "hemal_shah_brand_association": False,
        "navrangpura_hq_association": False
    },
    "brand_keywords_density": {}
}

# Scan llms.txt and llms-full.txt
with open(os.path.join(ROOT, "llms.txt"), "r", encoding="utf-8") as f:
    llms_txt = f.read()

with open(os.path.join(ROOT, "llms-full.txt"), "r", encoding="utf-8") as f:
    llms_full_txt = f.read()

branding_audit["entity_disambiguation_checks"]["hemal_shah_brand_association"] = (
    "Hemal Shah" in llms_txt and "TENSIX" in llms_txt
)
branding_audit["entity_disambiguation_checks"]["navrangpura_hq_association"] = (
    "Navrangpura" in llms_txt and "23.0366" in llms_txt
)
branding_audit["entity_disambiguation_checks"]["tenstorrent_disambiguation"] = (
    "Tenstorrent" in llms_txt or "Tenstorrent" in llms_full_txt
)
branding_audit["entity_disambiguation_checks"]["tensix_consulting_disambiguation"] = (
    "Primavera" in llms_txt or "Tensix Consulting" in llms_full_txt
)

for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ("hk", "skills", "resources", "assets", "node_modules", ".git", "09_Archive")]
    for f in files:
        if f.endswith(".html") and not f.startswith("google"):
            fpath = os.path.join(dirpath, f)
            rel = os.path.relpath(fpath, ROOT).replace("\\", "/")
            branding_audit["total_pages"] += 1
            with open(fpath, "r", encoding="utf-8") as hf:
                c = hf.read()
            
            # Count keyword appearances
            tensix_count = len(re.findall(r'\bTENSIX\b', c, re.IGNORECASE))
            branding_audit["brand_keywords_density"][rel] = tensix_count
            
            # Title
            t_match = re.search(r'<title>(.*?)</title>', c, re.IGNORECASE)
            if t_match and "TENSIX" in t_match.group(1).upper():
                branding_audit["pages_with_tensix_title"].append(rel)
                
            # Meta
            d_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)["\']', c, re.IGNORECASE)
            if not d_match:
                d_match = re.search(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']description["\']', c, re.IGNORECASE)
            if d_match and "TENSIX" in d_match.group(1).upper():
                branding_audit["pages_with_tensix_meta"].append(rel)
                
            # Schema
            if '"Brand"' in c or '"Organization"' in c:
                branding_audit["pages_with_brand_schema"].append(rel)

print("="*60)
print("      TENSIX BRANDING & COMPETITOR ENTITY AUDIT")
print("="*60)
print(f"Total HTML Pages Audited: {branding_audit['total_pages']}")
print(f"Pages with 'TENSIX' in <title>: {len(branding_audit['pages_with_tensix_title'])} / {branding_audit['total_pages']}")
print(f"Pages with 'TENSIX' in <meta description>: {len(branding_audit['pages_with_tensix_meta'])} / {branding_audit['total_pages']}")
print(f"Pages with Organization/Brand Schema: {len(branding_audit['pages_with_brand_schema'])} / {branding_audit['total_pages']}")

print("\n--- Entity Disambiguation Signals (AEO/GEO/Google Knowledge Graph) ---")
for k, v in branding_audit["entity_disambiguation_checks"].items():
    print(f"  [{'PASS' if v else 'ACTION NEEDED'}] {k}: {v}")

print("\nTop 10 Pages by Brand Keyword Density:")
sorted_density = sorted(branding_audit["brand_keywords_density"].items(), key=lambda x: -x[1])
for p, count in sorted_density[:10]:
    print(f"  - {p}: {count} occurrences of 'TENSIX'")
