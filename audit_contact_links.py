import os
import re
import json
from collections import defaultdict

ROOT = r"D:\projects\tensix"
html_files = []
for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '09_Archive', 'legacy_seo_scripts')]
    for f in files:
        if f.endswith('.html') and not f.startswith('google') and not f.startswith('rajputbhavin'):
            html_files.append(os.path.join(dirpath, f))

links_found = defaultdict(lambda: defaultdict(list))

for path in html_files:
    rel = os.path.relpath(path, ROOT).replace('\\', '/')
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # LinkedIn
    for m in set(re.findall(r'href=["\'](https?://[^"\']*linkedin\.com[^"\']*)["\']', html)):
        links_found['LinkedIn'][m].append(rel)
    # GitHub
    for m in set(re.findall(r'href=["\'](https?://[^"\']*github\.com[^"\']*)["\']', html)):
        links_found['GitHub'][m].append(rel)
    # WhatsApp
    for m in set(re.findall(r'href=["\'](https?://[^"\']*(?:wa\.me|api\.whatsapp\.com)[^"\']*)["\']', html)):
        links_found['WhatsApp'][m].append(rel)
    # Mailto
    for m in set(re.findall(r'href=["\'](mailto:[^"\']*)["\']', html)):
        links_found['Email'][m].append(rel)
    # Phone / Tel
    for m in set(re.findall(r'href=["\'](tel:[^"\']*)["\']', html)):
        links_found['Phone'][m].append(rel)
    # Other Socials (Instagram, Twitter / X)
    for m in set(re.findall(r'href=["\'](https?://[^"\']*(?:instagram\.com|twitter\.com|x\.com)[^"\']*)["\']', html)):
        links_found['Socials'][m].append(rel)

report = {}
for category, items in links_found.items():
    report[category] = []
    for link, pages_list in items.items():
        report[category].append({
            "target": link,
            "page_count": len(pages_list),
            "sample_pages": pages_list[:3]
        })

print(json.dumps(report, indent=2))
