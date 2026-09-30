import os, re, json
from urllib.parse import urlparse, urldefrag

ROOT = r"H:\portfolio_website\tensix"

# 1. Discover all HTML pages
pages = {}
for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ("hk", "skills", "resources", "assets", "node_modules", ".git", "09_Archive")]
    for f in files:
        if f.endswith(".html") and not f.startswith("google") and not f.startswith("rajputbhavin"):
            fpath = os.path.join(dirpath, f)
            rel = os.path.relpath(fpath, ROOT).replace("\\", "/")
            with open(fpath, "r", encoding="utf-8") as hf:
                pages[rel] = {
                    "path": fpath,
                    "html": hf.read()
                }

print(f"Loaded {len(pages)} HTML pages for Screaming Frog Audit.\n")

issues = {
    "broken_internal_links": [],
    "missing_titles": [],
    "duplicate_titles": {},
    "titles_over_60_chars": [],
    "titles_under_30_chars": [],
    "missing_meta_desc": [],
    "duplicate_meta_desc": {},
    "meta_desc_over_160_chars": [],
    "meta_desc_under_70_chars": [],
    "missing_h1": [],
    "multiple_h1": [],
    "h1_over_70_chars": [],
    "h1_matches_title_identically": [],
    "missing_canonical": [],
    "non_self_referencing_canonical": [],
    "broken_images": [],
    "missing_image_alt": [],
    "missing_image_dimensions": [],
    "orphan_pages": [],
    "missing_og_tags": [],
    "missing_twitter_card": [],
    "external_links_missing_noopener": []
}

title_map = {}
desc_map = {}
inlink_counts = {p: 0 for p in pages}
all_ids_per_page = {p: set() for p in pages}

# Collect IDs on each page for anchor link validation
for rel, data in pages.items():
    content = data["html"]
    ids = re.findall(r'\bid=["\']([^"\']+)["\']', content, re.IGNORECASE)
    all_ids_per_page[rel] = set(ids)

# Run Screaming Frog Rules
for rel, data in pages.items():
    content = data["html"]
    
    # 1. Title Checks
    t_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL | re.IGNORECASE)
    if not t_match or not t_match.group(1).strip():
        issues["missing_titles"].append(rel)
    else:
        title = t_match.group(1).strip()
        length = len(title)
        if length > 65:
            issues["titles_over_60_chars"].append((rel, length, title))
        elif length < 30:
            issues["titles_under_30_chars"].append((rel, length, title))
        
        title_map.setdefault(title, []).append(rel)
        
    # 2. Meta Description Checks
    d_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)["\']', content, re.IGNORECASE)
    if not d_match:
        d_match = re.search(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']description["\']', content, re.IGNORECASE)
    
    if not d_match or not d_match.group(1).strip():
        issues["missing_meta_desc"].append(rel)
    else:
        desc = d_match.group(1).strip()
        d_len = len(desc)
        if d_len > 165:
            issues["meta_desc_over_160_chars"].append((rel, d_len, desc[:60] + "..."))
        elif d_len < 70:
            issues["meta_desc_under_70_chars"].append((rel, d_len, desc))
        desc_map.setdefault(desc, []).append(rel)
        
    # 3. H1 Headings
    h1s = re.findall(r'<h1\b[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
    cleaned_h1s = [re.sub(r'<[^>]+>', '', h).strip() for h in h1s if h.strip()]
    if len(cleaned_h1s) == 0:
        issues["missing_h1"].append(rel)
    elif len(cleaned_h1s) > 1:
        issues["multiple_h1"].append((rel, len(cleaned_h1s)))
    else:
        h1_text = cleaned_h1s[0]
        if len(h1_text) > 75:
            issues["h1_over_70_chars"].append((rel, len(h1_text), h1_text[:50]))
        if t_match and h1_text.lower() == t_match.group(1).strip().lower():
            issues["h1_matches_title_identically"].append(rel)

    # 4. Canonical Checks
    c_match = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']*)["\']', content, re.IGNORECASE)
    if not c_match:
        c_match = re.search(r'<link[^>]+href=["\']([^"\']*)["\'][^>]+rel=["\']canonical["\']', content, re.IGNORECASE)
    if not c_match:
        issues["missing_canonical"].append(rel)
    else:
        canon_url = c_match.group(1).strip()
        expected = "https://tensix.in/" if rel == "index.html" else f"https://tensix.in/{rel}"
        if canon_url != expected:
            issues["non_self_referencing_canonical"].append((rel, canon_url, expected))

    # 5. OpenGraph & Twitter
    if not re.search(r'<meta[^>]+property=["\']og:title["\']', content, re.IGNORECASE):
        issues["missing_og_tags"].append(rel)
    if not re.search(r'<meta[^>]+name=["\']twitter:card["\']', content, re.IGNORECASE):
        issues["missing_twitter_card"].append(rel)

    # 6. Images & Alt Text & Dimensions
    img_matches = re.finditer(r'<img\s+([^>]+)>', content, re.IGNORECASE)
    for m in img_matches:
        attrs = m.group(1)
        src_match = re.search(r'src=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', attrs, re.IGNORECASE)
        w_match = re.search(r'width=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        h_match = re.search(r'height=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        
        if not alt_match:
            issues["missing_image_alt"].append((rel, attrs[:50]))
        if not w_match or not h_match:
            issues["missing_image_dimensions"].append((rel, attrs[:50]))
            
        if src_match:
            src = src_match.group(1).split("?")[0]
            if not src.startswith("http") and not src.startswith("data:"):
                # resolve local image path
                curr_dir = os.path.dirname(os.path.join(ROOT, rel))
                target_img = os.path.normpath(os.path.join(curr_dir, src))
                if not os.path.exists(target_img):
                    issues["broken_images"].append((rel, src))

    # 7. Internal Links, Anchors, and Target Blank
    link_matches = re.finditer(r'<a\s+([^>]+)>', content, re.IGNORECASE)
    for m in link_matches:
        attrs = m.group(1)
        href_match = re.search(r'href=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        target_match = re.search(r'target=["\']_blank["\']', attrs, re.IGNORECASE)
        rel_attr = re.search(r'rel=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        
        if target_match and (not rel_attr or "noopener" not in rel_attr.group(1)):
            issues["external_links_missing_noopener"].append((rel, attrs[:50]))
            
        if href_match:
            href = href_match.group(1)
            if href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:") or href == "#":
                continue
            if href.startswith("http://") or href.startswith("https://"):
                if "tensix.in" not in href:
                    continue
                # Internal full URL
                href = href.replace("https://tensix.in", "").replace("http://tensix.in", "")
                if not href:
                    href = "/"

            url_path, frag = urldefrag(href)
            url_path = url_path.split("?")[0]
            
            # Anchor only on current page
            if not url_path and frag:
                if frag not in all_ids_per_page[rel]:
                    issues["broken_internal_links"].append((rel, f"#{frag} (anchor not found)"))
                continue
                
            # Internal page resolution
            if url_path.startswith("/"):
                dest_rel = url_path.lstrip("/")
                if not dest_rel:
                    dest_rel = "index.html"
                elif not dest_rel.endswith(".html"):
                    dest_rel += ".html"
            else:
                curr_dir = os.path.dirname(os.path.join(ROOT, rel))
                resolved = os.path.normpath(os.path.join(curr_dir, url_path))
                dest_rel = os.path.relpath(resolved, ROOT).replace("\\", "/")
                
            if dest_rel not in pages and dest_rel != "":
                # Check if it exists as static asset
                if not os.path.exists(os.path.join(ROOT, dest_rel)):
                    issues["broken_internal_links"].append((rel, href))
            else:
                target_page = dest_rel if dest_rel in pages else "index.html"
                inlink_counts[target_page] += 1
                if frag and frag not in all_ids_per_page.get(target_page, set()):
                    issues["broken_internal_links"].append((rel, f"{href} (anchor #{frag} not in {target_page})"))

# Find orphan pages (0 internal inlinks from anywhere, excluding index.html)
for p, count in inlink_counts.items():
    if count == 0 and p != "index.html":
        issues["orphan_pages"].append(p)

# Duplicate titles and descriptions
for t, plist in title_map.items():
    if len(plist) > 1:
        issues["duplicate_titles"][t] = plist

for d, plist in desc_map.items():
    if len(plist) > 1:
        issues["duplicate_meta_desc"][d] = plist

print("="*60)
print("       SCREAMING FROG SEO SPIDER EMULATION REPORT")
print("="*60)

print(f"\n1. INTERNAL LINKS & RESPONSE:")
print(f"   - Broken Internal Links / Missing Anchors: {len(issues['broken_internal_links'])}")
for b in issues['broken_internal_links'][:10]:
    print(f"     [!] {b[0]} -> {b[1]}")
print(f"   - Orphan Pages (0 inlinks): {len(issues['orphan_pages'])}")
for o in issues['orphan_pages']:
    print(f"     [!] Orphan: {o}")

print(f"\n2. PAGE TITLES:")
print(f"   - Missing Titles: {len(issues['missing_titles'])}")
print(f"   - Duplicate Titles: {len(issues['duplicate_titles'])}")
for t, pl in issues['duplicate_titles'].items():
    print(f"     [!] Duplicate: '{t[:40]}...' across {pl}")
print(f"   - Titles Over 65 Chars (SERP Truncation): {len(issues['titles_over_60_chars'])}")
for p, l, t in issues['titles_over_60_chars'][:5]:
    print(f"     [i] {p} ({l} chars): {t}")
print(f"   - Titles Under 30 Chars: {len(issues['titles_under_30_chars'])}")

print(f"\n3. META DESCRIPTIONS:")
print(f"   - Missing Meta Descriptions: {len(issues['missing_meta_desc'])}")
print(f"   - Duplicate Meta Descriptions: {len(issues['duplicate_meta_desc'])}")
print(f"   - Over 165 Chars: {len(issues['meta_desc_over_160_chars'])}")
print(f"   - Under 70 Chars: {len(issues['meta_desc_under_70_chars'])}")

print(f"\n4. H1 HEADINGS:")
print(f"   - Missing H1: {len(issues['missing_h1'])}")
print(f"   - Multiple H1: {len(issues['multiple_h1'])}")
for m in issues['multiple_h1']:
    print(f"     [!] {m[0]}: has {m[1]} H1 tags")
print(f"   - H1 Over 75 Chars: {len(issues['h1_over_70_chars'])}")

print(f"\n5. CANONICALS:")
print(f"   - Missing Canonical: {len(issues['missing_canonical'])}")
print(f"   - Non-Self-Referencing / Canonical Mismatch: {len(issues['non_self_referencing_canonical'])}")
for n in issues['non_self_referencing_canonical']:
    print(f"     [!] {n[0]}: Found '{n[1]}' vs Expected '{n[2]}'")

print(f"\n6. IMAGES & ACCESSIBILITY:")
print(f"   - Broken Images (404 file path): {len(issues['broken_images'])}")
for b in issues['broken_images']:
    print(f"     [!] {b[0]} -> {b[1]}")
print(f"   - Missing Alt: {len(issues['missing_image_alt'])}")
print(f"   - Missing Width/Height: {len(issues['missing_image_dimensions'])}")

print(f"\n7. SOCIAL & PROTOCOL:")
print(f"   - Missing OG Title/Tags: {len(issues['missing_og_tags'])}")
print(f"   - Missing Twitter Card: {len(issues['missing_twitter_card'])}")
print(f"   - External target=_blank missing rel='noopener': {len(issues['external_links_missing_noopener'])}")

print("\n" + "="*60)
