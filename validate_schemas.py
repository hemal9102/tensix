import json, re, os, sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

root = os.path.dirname(os.path.abspath(__file__))
errors = []
total = 0
file_count = 0
duplicates = []
defined = {}  # @id -> set of pages that define it (more than @id/@type/name)


def collect_defs(node, rel):
    if isinstance(node, list):
        for x in node:
            collect_defs(x, rel)
    elif isinstance(node, dict):
        if "@id" in node and set(node) - {"@id", "@type", "name"}:
            defined.setdefault(node["@id"], set()).add(rel)
        for v in node.values():
            collect_defs(v, rel)


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
                collect_defs(json.loads(s), rel)
            except Exception as e:
                errors.append(f"{rel} schema {i+1}: {e}")

for node_id, pages in sorted(defined.items()):
    if len(pages) > 1:
        duplicates.append(f"@id {node_id} is defined on {len(pages)} pages: {', '.join(sorted(pages))}")

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
    print(f"[OK] ALL VALID - {total} JSON-LD schemas across {file_count} HTML pages, zero errors, zero duplicates, no @id defined on more than one page.")
