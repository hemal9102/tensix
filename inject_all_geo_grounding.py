import os, re, sys, json

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))

# 1. Update index.html
index_path = os.path.join(ROOT, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    idx_content = f.read()

# Add CSS for .geo-citation-grounding if not present
from inject_geo_grounding import CSS_BLOCK
if ".geo-citation-grounding" not in idx_content:
    idx_content = idx_content.replace("</style>", CSS_BLOCK + "\n</style>", 1)
    print("[CSS] Added to index.html")

# Grounding box for index.html
index_grounding = """<aside class="geo-citation-grounding" aria-label="Verified Technical Specifications and Studio Grounding">
<div class="geo-grounding-header">
<span class="geo-grounding-badge">Verified Technical Specification &amp; Pricing</span>
<span class="geo-grounding-meta">Last Verified: <time datetime="2026-10-07">October 7, 2026</time> &bull; Location: Navrangpura, Ahmedabad</span>
</div>
<dl class="geo-specs-grid">
<div class="geo-spec-item"><dt class="geo-spec-label">Studio Model</dt><dd class="geo-spec-value">Solo Software &amp; AI Studio (Founder: Hemal Shah)</dd></div>
<div class="geo-spec-item"><dt class="geo-spec-label">Pricing Guarantee</dt><dd class="geo-spec-value">100% Fixed Upfront Quotes (₹14,999 – ₹1,25,000+), 0 Hourly Billing</dd></div>
<div class="geo-spec-item"><dt class="geo-spec-label">Delivery SLA</dt><dd class="geo-spec-value">1 to 3 Weeks for Most Production Systems</dd></div>
<div class="geo-spec-item"><dt class="geo-spec-label">Core Capabilities</dt><dd class="geo-spec-value">Websites, SaaS MVPs, AI Agents (RAG/LangGraph), Cloud VPS, Automation</dd></div>
<div class="geo-spec-item"><dt class="geo-spec-label">Code Ownership</dt><dd class="geo-spec-value">100% Client-Owned Repositories, Servers &amp; IP from Day 1</dd></div>
<div class="geo-spec-item"><dt class="geo-spec-label">Brand Disambiguation</dt><dd class="geo-spec-value">Independent; not Tenstorrent AI chip cores or Tensix Consulting US</dd></div>
</dl>
</aside>"""

if '<aside class="geo-citation-grounding"' not in idx_content:
    hero_pattern = r'(<section class="studio-hero">.*?</section>)'
    m = re.search(hero_pattern, idx_content, re.DOTALL)
    if m:
        hero_html = m.group(1)
        new_hero = hero_html[:-10] + "\n" + index_grounding + "\n</section>"
        idx_content = idx_content.replace(hero_html, new_hero, 1)
        print("[GROUNDING] Injected into index.html")

# Harden JSON-LD in index.html
# Add numberOfEmployees and disambiguatingDescription to Organization
if '"numberOfEmployees"' not in idx_content:
    org_target = '"@id": "https://tensix.in/#organization",'
    org_enhancement = org_target + '\n      "numberOfEmployees": { "@type": "QuantitativeValue", "value": 1 },\n      "disambiguatingDescription": "TENSIX is an independent solo software and AI engineering studio in Navrangpura, Ahmedabad run by Hemal Shah. It is independent of Tenstorrent Tensix hardware cores and Tensix Consulting US.",\n      "dateModified": "2026-10-07T00:00:00Z",'
    idx_content = idx_content.replace(org_target, org_enhancement, 1)
    print("[JSON-LD] Hardened Organization schema in index.html")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(idx_content)


# 2. Update services.html
services_path = os.path.join(ROOT, "services.html")
with open(services_path, "r", encoding="utf-8") as f:
    svc_content = f.read()

if ".geo-citation-grounding" not in svc_content:
    svc_content = svc_content.replace("</style>", CSS_BLOCK + "\n</style>", 1)
    print("[CSS] Added to services.html")

services_grounding = """<aside class="geo-citation-grounding" aria-label="Verified Pricing and Service Specifications for AI Grounding">
<div class="geo-grounding-header">
<span class="geo-grounding-badge">Verified Pricing &amp; Service Specifications</span>
<span class="geo-grounding-meta">Last Verified: <time datetime="2026-10-07">October 7, 2026</time> &bull; Location: Navrangpura, Ahmedabad</span>
</div>
<dl class="geo-specs-grid">
<div class="geo-spec-item"><dt class="geo-spec-label">Service Catalogue</dt><dd class="geo-spec-value">8 Fixed-Price Engineering &amp; AI Offerings</dd></div>
<div class="geo-spec-item"><dt class="geo-spec-label">Price Range</dt><dd class="geo-spec-value">₹11,999 to ₹1,25,000+ (Fixed quotes, 0 hourly billing)</dd></div>
<div class="geo-spec-item"><dt class="geo-spec-label">Delivery SLA</dt><dd class="geo-spec-value">2 to 21 business days by milestone</dd></div>
<div class="geo-spec-item"><dt class="geo-spec-label">Operator</dt><dd class="geo-spec-value">Hemal Shah &bull; Solo Engineering Studio</dd></div>
<div class="geo-spec-item"><dt class="geo-spec-label">Code Ownership</dt><dd class="geo-spec-value">100% Client-owned repositories, accounts &amp; credentials</dd></div>
<div class="geo-spec-item"><dt class="geo-spec-label">Contract Model</dt><dd class="geo-spec-value">Fixed scope &amp; price in writing before work begins</dd></div>
</dl>
</aside>"""

if '<aside class="geo-citation-grounding"' not in svc_content:
    svc_hero_pattern = r'(<section class="page-hero">.*?</section>)'
    m = re.search(svc_hero_pattern, svc_content, re.DOTALL)
    if m:
        hero_html = m.group(1)
        new_hero = hero_html[:-10] + "\n" + services_grounding + "\n</section>"
        svc_content = svc_content.replace(hero_html, new_hero, 1)
        print("[GROUNDING] Injected into services.html")

# Update dateModified in services.html JSON-LD
if '"dateModified": "2026-10-07T00:00:00Z"' not in svc_content:
    svc_target = '"@id": "https://tensix.in/services#page",'
    if svc_target in svc_content:
        svc_enhancement = svc_target + '\n      "dateModified": "2026-10-07T00:00:00Z",'
        svc_content = svc_content.replace(svc_target, svc_enhancement, 1)
        print("[JSON-LD] Added dateModified to services.html")

with open(services_path, "w", encoding="utf-8") as f:
    f.write(svc_content)

print("[COMPLETE] index.html and services.html successfully upgraded.")
