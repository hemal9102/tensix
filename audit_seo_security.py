import os, re, json

root = r"H:\portfolio_website\tensix"

report = {
    "missing_rel_noopener": [],
    "faq_schema_vs_html_mismatch": [],
    "images_missing_alt": [],
    "images_missing_dimensions": [],
    "pages_without_meta_desc": [],
    "pages_without_canonical": [],
    "forms_audit": []
}

for dirpath, dirs, files in os.walk(root):
    dirs[:] = [d for d in dirs if d not in ("hk", "skills", "resources", "assets", "node_modules", ".git", "09_Archive")]
    for f in files:
        if f.endswith(".html") and not f.startswith("google") and not f.startswith("rajputbhavin"):
            fpath = os.path.join(dirpath, f)
            rel = os.path.relpath(fpath, root).replace("\\", "/")
            with open(fpath, encoding="utf-8") as hf:
                content = hf.read()
            
            # 1. Reverse Tabnabbing (_blank missing rel)
            tags = re.findall(r'<a\s+[^>]*target=["\']_blank["\'][^>]*>', content, re.IGNORECASE)
            for t in tags:
                if 'rel=' not in t.lower() or 'noopener' not in t.lower():
                    report["missing_rel_noopener"].append((rel, t[:70]))
            
            # 2. FAQ Schema vs HTML Accordion check
            has_faq_schema = '"FAQPage"' in content or "'FAQPage'" in content
            has_faq_html = '<details' in content.lower() or 'faq-accordion' in content.lower()
            if has_faq_schema and not has_faq_html:
                report["faq_schema_vs_html_mismatch"].append(rel)
                
            # 3. Images missing alt or width/height
            img_tags = re.findall(r'<img\s+[^>]*>', content, re.IGNORECASE)
            for img in img_tags:
                if 'alt=' not in img.lower():
                    report["images_missing_alt"].append((rel, img[:60]))
                if 'width=' not in img.lower() or 'height=' not in img.lower():
                    report["images_missing_dimensions"].append((rel, img[:60]))
                    
            # 4. Meta description
            has_desc = bool(re.search(r'<meta[^>]+name=["\']description["\']', content, re.IGNORECASE) or re.search(r'<meta[^>]+content=[^>]+name=["\']description["\']', content, re.IGNORECASE))
            if not has_desc:
                report["pages_without_meta_desc"].append(rel)
                
            # 5. Canonical
            has_canon = bool(re.search(r'<link[^>]+rel=["\']canonical["\']', content, re.IGNORECASE) or re.search(r'<link[^>]+href=[^>]+rel=["\']canonical["\']', content, re.IGNORECASE))
            if not has_canon:
                report["pages_without_canonical"].append(rel)
                
            # 6. Forms audit
            forms = re.findall(r'<form\b[^>]*>.*?</form>', content, re.DOTALL | re.IGNORECASE)
            for form in forms:
                has_honeypot = '_honey' in form or 'botcheck' in form or 'display:none' in form or 'hidden' in form
                report["forms_audit"].append({
                    "page": rel,
                    "has_honeypot": has_honeypot,
                    "action": re.search(r'action=["\']([^"\']*)["\']', form, re.IGNORECASE).group(1) if re.search(r'action=["\']([^"\']*)["\']', form, re.IGNORECASE) else "none"
                })

print("=== SEO & SECURITY COMPREHENSIVE AUDIT ===")
print(f"1. Target=_blank links missing rel='noopener noreferrer': {len(report['missing_rel_noopener'])}")
for r in report['missing_rel_noopener'][:5]:
    print(f"   - {r[0]}: {r[1]}")

print(f"\n2. FAQ Schema Present BUT Hidden/Missing from HTML Body: {len(report['faq_schema_vs_html_mismatch'])}")
for r in report['faq_schema_vs_html_mismatch']:
    print(f"   - {r}")

print(f"\n3. Images Missing Alt Tag: {len(report['images_missing_alt'])}")
print(f"4. Images Missing Width/Height (CLS Risk): {len(report['images_missing_dimensions'])}")
print(f"5. Pages Missing Meta Description: {len(report['pages_without_meta_desc'])}")
print(f"6. Pages Missing Canonical Tag: {len(report['pages_without_canonical'])}")
print(f"\n7. Forms Detected: {len(report['forms_audit'])}")
for f in report['forms_audit']:
    print(f"   - {f['page']}: Action='{f['action']}', Honeypot={f['has_honeypot']}")
