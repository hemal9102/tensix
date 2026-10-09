import os
import re
import glob

ROOT = r"D:\projects\tensix"
html_files = []
for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '09_Archive', 'legacy_seo_scripts')]
    for f in files:
        if f.endswith('.html') and not f.startswith('google') and not f.startswith('rajputbhavin'):
            html_files.append(os.path.join(dirpath, f))

modified = 0

for p in html_files:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content

    # 1. Remove repo link in work.html
    content = re.sub(r'<a\s+class=["\']card-link["\']\s+href=["\']https?://github\.com/hemal9102/book_generator["\'][^>]*>.*?</a>', '', content, flags=re.DOTALL)

    # 2. Remove repo link in blog
    content = content.replace('<a href="https://github.com/hemal9102/ChessAI-Glasses" rel="noopener" style="color:#1D4ED8;" target="_blank">on GitHub</a>', 'available as open source')

    # 3. Remove footer GitHub link
    content = re.sub(r'<a\s+href=["\']https?://github\.com/hemal9102/?["\'][^>]*>GitHub</a>\s*<span\s+class=["\']footer-sep["\']>·</span>\s*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*<span\s+class=["\']footer-sep["\']>·</span>\s*<a\s+href=["\']https?://github\.com/hemal9102/?["\'][^>]*>GitHub</a>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<a\s+href=["\']https?://github\.com/hemal9102/?["\'][^>]*>GitHub</a>', '', content, flags=re.IGNORECASE)

    # 4. Remove rel="me" GitHub tag from <head>
    content = re.sub(r'<link\s+href=["\']https?://github\.com/hemal9102/?["\']\s+rel=["\']me["\'][^>]*/>\s*', '', content, flags=re.IGNORECASE)

    # 5. Remove from JSON-LD schema sameAs array
    content = re.sub(r'"https?://github\.com/hemal9102/?",?\s*', '', content)

    # Clean up trailing comma in JSON arrays if any: [ ..., ] -> [ ... ]
    content = re.sub(r',(\s*\])', r'\1', content)

    if content != orig:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        modified += 1

print(f"Successfully processed. Modified {modified} HTML files.")
