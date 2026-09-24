import json, re, os, sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

root = r"H:\portfolio_website\hemalshah"
errors = []
total = 0
file_count = 0
duplicates = []

for dirpath, dirs, files in os.walk(root):
    dirs[:] = [d for d in dirs if d not in ("hk", "skills", "resources", "assets", "node_modules", ".git", "09_Archive")]
    for fname in files:
        if not fname.endswith(".html") or fname.startswith("google") or fname.startswith("rajputbhavin"):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, encoding="utf-8") as f:
            html = f.read()
        schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
        total += len(schemas)
        file_count += 1
        rel = os.path.relpath(fpath, root)
        
        if len(schemas) > 1:
            duplicates.append(f"{rel} has {len(schemas)} JSON-LD blocks (expected 1)")
            
        for i, s in enumerate(schemas):
            try:
                json.loads(s)
            except Exception as e:
                errors.append(f"{rel} schema {i+1}: {e}")

if errors or duplicates:
    if duplicates:
        print("[WARN] Duplicates Found:")
        for d in duplicates:
            print(f"  - {d}")
    if errors:
        print("[ERROR] Schema Syntax Errors:")
        for e in errors:
            print(f"  - {e}")
else:
    print(f"[OK] ALL VALID - {total} JSON-LD schemas across {file_count} HTML pages, zero errors, zero duplicates.")
