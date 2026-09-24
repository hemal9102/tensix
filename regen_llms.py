"""
Regenerate llms-full.txt from current clean HTML files.
Strips HTML tags, extracts visible text per page.
"""
import os, re

ROOT = r"H:\portfolio_website\tensix"

PAGES = [
    "index.html", "about.html", "services.html", "work.html",
    "contact.html", "team.html", "blogs.html", "whoami.html",
    "compare.html", "frameworks.html", "gallery.html", "resources.html",
    "wr1.html", "navrangpura.html", "ahmedabad-software-engineering.html",
    "hk-engineering-ahmedabad.html",
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

lines = [
    "TENSIX — Autonomous AI Swarms & Full-Stack Engineering Studio | Full Website Text Corpus",
    "Founded, Owned, and Architected Solely by Hemal Shah (Navrangpura, Ahmedabad, Gujarat, India)",
    "Coordinates: 23.0366° N, 72.5615° E",
    "Generated for AI crawlers (LLMs, SearchGPT, Perplexity, Claude, Gemini). Canonical: https://tensix.in/\n"
]

for page in PAGES:
    filepath = os.path.join(ROOT, page)
    if not os.path.exists(filepath):
        print(f"Warning: page missing {filepath}")
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
