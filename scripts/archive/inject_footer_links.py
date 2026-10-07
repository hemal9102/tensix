"""Idempotently add the 8-service footer column to every production page.

Inserts the "Services navigation" block (same markup as services.html) before
<div class="footer-social">. Pages that already have it are skipped.
index.html uses its own studio footer, which already lists all 8 services.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = ("hk", "skills", "resources", "assets", "node_modules", ".git", "09_Archive")
MARKER = 'aria-label="Services navigation"'
ANCHOR = '<div class="footer-social">'

BLOCK = '''<nav aria-label="Services navigation" class="footer-nav">
<h3>Services</h3>
<ul>
<li><a href="/services/website-development">Websites</a></li>
<li><a href="/services/ai-agent-development">AI Agents and Assistants</a></li>
<li><a href="/services/custom-software-saas-development">Custom Software and SaaS</a></li>
<li><a href="/services/cloud-devops">Cloud and DevOps</a></li>
<li><a href="/services/email-deliverability">Email Deliverability</a></li>
<li><a href="/services/data-scraping-automation">Data and Automation</a></li>
<li><a href="/services/geo-aeo-seo">AI Search Visibility</a></li>
<li><a href="/services/fractional-cto-retainers">Retainers and Fractional CTO</a></li>
</ul>
</nav>
'''

for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if not f.endswith(".html") or f.startswith("google"):
            continue
        path = os.path.join(dirpath, f)
        with open(path, encoding="utf-8", newline="") as fh:
            html = fh.read()
        if MARKER in html or ANCHOR not in html:
            continue
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(html.replace(ANCHOR, BLOCK + ANCHOR, 1))
        print("Updated", os.path.relpath(path, ROOT))
