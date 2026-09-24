import os, re

ROOT = r"H:\portfolio_website\hemalshah"

# Remove Google Fonts lines (redundant — local woff2 is preloaded)
REMOVE_LINES = [
    '<link as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&amp;display=swap" rel="preload"/>',
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&amp;display=swap" media="print" onload="this.media=\'all\'" rel="stylesheet"/>',
    '<noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet"/></noscript>',
]

# font-display: swap → optional (preloaded font; no swap = no CLS)
OLD_FONTFACE = "font-display: swap;"
NEW_FONTFACE = "font-display: optional;"

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
        original = content

        for line in REMOVE_LINES:
            content = content.replace(line, "")
        content = content.replace(OLD_FONTFACE, NEW_FONTFACE)

        # Clean up leftover blank lines from removals
        content = re.sub(r'\n{3,}', '\n\n', content)

        if content != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            fixed += 1
            print(f"  Fixed: {os.path.relpath(path, ROOT)}")

print(f"\nTotal fixed: {fixed} files")
