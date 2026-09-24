"""
Regenerate llms-full.txt from current clean HTML files.
Strips HTML tags, extracts visible text per page.
"""
import os, re

ROOT = r"H:\portfolio_website\hemalshah"

PAGES = [
    "index.html", "about.html", "services.html", "work.html",
    "contact.html", "team.html", "blogs.html", "whoami.html",
    "compare.html", "frameworks.html", "gallery.html", "resources.html",
    "blogs/why-i-chose-automation-over-a-9-to-5.html",
    "blogs/what-is-our-life.html",
    "blogs/the-ultimate-local-business-seo-master-strategy.html",
    "blogs/the-future-of-seo-geo-and-search-engines.html",
    "blogs/n8n-vs-python-scripts-when-to-use-which.html",
    "blogs/building-my-first-ai-project-lessons-learned.html",
    "blogs/ai-engineering/building-ai-agents-with-fastapi.html",
]

def strip_tags(html):
    # Remove script and style blocks entirely
    html = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
    # Remove all remaining tags
    html = re.sub(r'<[^>]+>', ' ', html)
    # Decode common HTML entities
    html = html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>') \
               .replace('&nbsp;', ' ').replace('&#39;', "'").replace('&quot;', '"')
    # Collapse whitespace
    html = re.sub(r'\s+', ' ', html).strip()
    return html

lines = ["Hemal Shah (HK) — AI Automation Engineer | Full Website Text Corpus"]
lines.append("Generated for AI crawlers. Source: https://hemalshah.vercel.app/\n")

for page in PAGES:
    filepath = os.path.join(ROOT, page)
    if not os.path.exists(filepath):
        continue
    with open(filepath, encoding="utf-8") as f:
        html = f.read()
    text = strip_tags(html)
    lines.append(f"\n--- Page: {page} ---")
    lines.append(text)

output = "\n".join(lines)
out_path = os.path.join(ROOT, "llms-full.txt")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(output)

# Quick verify — no CreativeIQ should remain
if "CreativeIQ" in output or "Converge OS" in output:
    print("WARNING: stale content still present!")
    for term in ["CreativeIQ", "Converge OS"]:
        if term in output:
            idx = output.index(term)
            print(f"  Found '{term}' at char {idx}: ...{output[max(0,idx-60):idx+60]}...")
else:
    print(f"llms-full.txt regenerated — {len(output):,} chars, CLEAN.")
