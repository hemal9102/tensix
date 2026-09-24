"""
build_sitemap.py
================
Generates a clean, production-ready sitemap for hemalshah.vercel.app

Output files:
  sitemap.xml        — all core + blog pages, forward-slash URLs, priority-weighted
  sitemap_index.xml  — master index pointing to sitemap.xml (extensible for future sub-sitemaps)

Rules:
  - No backslashes in URLs (fixes old bug)
  - No rajputbhavin_* pages (competitor decoys — not for indexing)
  - No google*.html (verification files)
  - No aeo_geo_pages/ (programmatic pages get their own sitemap later)
  - Priority: index=1.0, core pages=0.8, spoke pages=0.9, blogs=0.7, deep blogs=0.6
  - changefreq: index=daily, core=weekly, blogs=monthly
"""

import os
from pathlib import Path
from datetime import date

ROOT_DIR = Path(r"H:\portfolio_website\hemalshah")
BASE_URL = "https://hemalshah.vercel.app"
TODAY    = date.today().isoformat()

# Pages to skip entirely
SKIP_PREFIXES = ("google", "rajputbhavin")
SKIP_DIRS     = {"node_modules", ".git", "aeo_geo_pages", "hk", "__pycache__", "assets"}

# Priority + changefreq rules
PRIORITY_MAP = {
    "index.html":                        ("1.0", "daily"),
    "hk-engineering-ahmedabad.html":     ("0.9", "weekly"),
    "navrangpura.html":                  ("0.9", "weekly"),
    "ahmedabad-software-engineering.html":("0.9", "weekly"),
    "services.html":                     ("0.8", "weekly"),
    "about.html":                        ("0.8", "weekly"),
    "contact.html":                      ("0.8", "weekly"),
    "work.html":                         ("0.8", "weekly"),
    "whoami.html":                       ("0.8", "weekly"),
    "compare.html":                      ("0.7", "weekly"),
    "team.html":                         ("0.7", "weekly"),
    "frameworks.html":                   ("0.7", "weekly"),
    "resources.html":                    ("0.7", "weekly"),
    "gallery.html":                      ("0.6", "monthly"),
    "blogs.html":                        ("0.8", "weekly"),
}

def get_priority(rel_path: str):
    fname = Path(rel_path).name
    if fname in PRIORITY_MAP:
        return PRIORITY_MAP[fname]
    # Ahmedabad spoke blogs get boosted priority
    if "ahmedabad" in rel_path.lower():
        return ("0.8", "weekly")
    # Blog subdirs
    if "blogs/" in rel_path:
        return ("0.6", "monthly")
    return ("0.6", "monthly")

def collect_urls():
    urls = []
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for file in sorted(files):
            if not file.endswith(".html"):
                continue
            if any(file.startswith(p) for p in SKIP_PREFIXES):
                continue

            fp   = Path(root) / file
            rel  = fp.relative_to(ROOT_DIR).as_posix()  # always forward slashes

            # Build clean URL
            if rel == "index.html":
                url = f"{BASE_URL}/"
            else:
                url = f"{BASE_URL}/{rel}"

            priority, changefreq = get_priority(rel)
            urls.append((url, priority, changefreq))

    return urls

def build_sitemap(urls):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    lines.append('        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
    lines.append('        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9')
    lines.append('        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">')

    for url, priority, changefreq in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")

    lines.append("</urlset>")
    return "\n".join(lines)

def build_sitemap_index():
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>{BASE_URL}/sitemap.xml</loc>
    <lastmod>{TODAY}</lastmod>
  </sitemap>
</sitemapindex>"""

if __name__ == "__main__":
    print("Building sitemap...")
    urls = collect_urls()

    sitemap_xml = build_sitemap(urls)
    (ROOT_DIR / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")

    index_xml = build_sitemap_index()
    (ROOT_DIR / "sitemap_index.xml").write_text(index_xml, encoding="utf-8")

    print(f"sitemap.xml       — {len(urls)} URLs")
    print(f"sitemap_index.xml — 1 sitemap registered")
    print(f"Last modified     — {TODAY}")
    print("Done.")
