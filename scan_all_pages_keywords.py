import os
import re
import json

ROOT = r"D:\projects\tensix"
html_files = []
for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '09_Archive', 'legacy_seo_scripts')]
    for f in files:
        if f.endswith('.html') and not f.startswith('google') and not f.startswith('rajputbhavin'):
            html_files.append(os.path.join(dirpath, f))

page_targets = []
all_meta_kws = set()

for path in sorted(html_files):
    rel = os.path.relpath(path, ROOT).replace('\\', '/')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Title
    t_m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    title = t_m.group(1).strip() if t_m else ''
    
    # Meta Description
    d_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE | re.DOTALL)
    desc = d_m.group(1).strip() if d_m else ''
    
    # Meta Keywords
    k_m = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE | re.DOTALL)
    kws = [k.strip() for k in k_m.group(1).split(',')] if k_m else []
    for k in kws:
        if k:
            all_meta_kws.add(k.lower())
        
    # H1
    h_m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    h1 = re.sub(r'<[^>]+>', '', h_m.group(1)).strip() if h_m else ''
    
    page_targets.append({
        'url': rel,
        'title': title,
        'h1': h1,
        'meta_keywords_count': len(kws),
        'keywords': kws
    })

print(f"Total HTML Web Pages Scanned: {len(page_targets)}")
print(f"Total Unique Meta Tag Keywords across pages: {len(all_meta_kws)}")

output_file = r"D:\projects\tensix\page_keyword_inventory.json"
with open(output_file, 'w', encoding='utf-8') as out:
    json.dump({'total_pages': len(page_targets), 'unique_meta_keywords': len(all_meta_kws), 'pages': page_targets}, out, indent=2)

print(f"Inventory saved successfully to {output_file}")
