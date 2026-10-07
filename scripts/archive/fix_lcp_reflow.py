import os, re

ROOT = r"H:\portfolio_website\hemalshah"

OLD = "body{animation:pageFadeIn 0.6s ease forwards;}"
NEW = "body{animation:none;}main,.page-content,.site-footer{animation:pageFadeIn 0.6s ease forwards;}"

fixed = 0
for dirpath, _, filenames in os.walk(ROOT):
    if "node_modules" in dirpath:
        continue
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        path = os.path.join(dirpath, fn)
        with open(path, encoding="utf-8") as f:
            content = f.read()
        if OLD in content:
            content = content.replace(OLD, NEW)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            fixed += 1
            print(f"  Fixed: {os.path.relpath(path, ROOT)}")

print(f"\nTotal fixed: {fixed} files")
