# -*- coding: utf-8 -*-
"""
Audits all competitor pages on https://rajputbhavin.engineer using curl.exe
Extracts keywords, headings, meta tags, schemas, and structure.
"""

import subprocess
import xml.etree.ElementTree as ET
import json
import re
from bs4 import BeautifulSoup

def get_sitemap_urls():
    res = subprocess.run(['curl.exe', '-sL', 'https://rajputbhavin.engineer/sitemap.xml'], capture_output=True)
    root = ET.fromstring(res.stdout)
    urls = [elem.text for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    return urls

urls = get_sitemap_urls()
print(f"Total competitor URLs extracted from sitemap: {len(urls)}")

# Group URLs
core_urls = [u for u in urls if '/locations/' not in u and '/blog/' not in u]
location_urls = [u for u in urls if '/locations/' in u]
blog_urls = [u for u in urls if '/blog/' in u]

print(f"Core: {len(core_urls)} | Locations: {len(location_urls)} | Blogs: {len(blog_urls)}")

# Sample key URLs across all categories to fetch with curl.exe
target_urls = [
    # Core
    "https://rajputbhavin.engineer",
    "https://rajputbhavin.engineer/about-ceo",
    "https://rajputbhavin.engineer/case-studies",
    "https://rajputbhavin.engineer/services/saas-development",
    "https://rajputbhavin.engineer/services/ai-automation",
    "https://rajputbhavin.engineer/services/custom-software-erp",
    "https://rajputbhavin.engineer/services/enterprise-seo",
    # Ahmedabad Locations
    "https://rajputbhavin.engineer/locations/ahmedabad/best-it-company-in-ahmedabad",
    "https://rajputbhavin.engineer/locations/ahmedabad/custom-software-development-company-in-ahmedabad",
    "https://rajputbhavin.engineer/locations/ahmedabad/generative-engine-optimization-ahmedabad",
    "https://rajputbhavin.engineer/locations/gota-ahmedabad",
    # USA Locations
    "https://rajputbhavin.engineer/locations/usa/california/los-angeles/it-company-in-los-angeles",
    "https://rajputbhavin.engineer/locations/usa/texas/austin/it-company-in-austin",
    "https://rajputbhavin.engineer/locations/usa/new-york/new-york-city/it-company-in-new-york-city",
    # Top Blogs
    "https://rajputbhavin.engineer/blog/who-is-rajput-bhavin",
    "https://rajputbhavin.engineer/blog/saas-developer-ahmedabad",
    "https://rajputbhavin.engineer/blog/best-it-company-gota-ahmedabad",
    "https://rajputbhavin.engineer/blog/generative-ai-search-optimization",
    "https://rajputbhavin.engineer/blog/advanced-prompt-engineering-saas"
]

all_keywords = set()
all_titles = []
all_faqs = []
all_schemas_types = set()

print("\nFetching and analyzing pages via curl.exe...")
for u in target_urls:
    res = subprocess.run(['curl.exe', '-sL', u], capture_output=True, text=True, encoding='utf-8', errors='ignore')
    soup = BeautifulSoup(res.stdout, 'html.parser')
    
    title = soup.title.string.strip() if soup.title else 'No Title'
    all_titles.append((u, title))
    
    # Meta keywords
    m_kw = soup.find('meta', {'name': 'keywords'})
    if m_kw and m_kw.get('content'):
        kws = [k.strip() for k in m_kw.get('content').split(',') if k.strip()]
        all_keywords.update(kws)
        
    # Schemas
    schemas = soup.find_all('script', type='application/ld+json')
    for s in schemas:
        try:
            d = json.loads(s.string)
            if '@type' in d:
                all_schemas_types.add(d['@type'] if isinstance(d['@type'], str) else tuple(d['@type']))
            if '@graph' in d:
                for n in d['@graph']:
                    if '@type' in n:
                        all_schemas_types.add(n['@type'] if isinstance(n['@type'], str) else tuple(n['@type']))
            # Check for FAQ
            if d.get('@type') == 'FAQPage' or any(n.get('@type') == 'FAQPage' for n in d.get('@graph', [])):
                faqs = d.get('mainEntity', [])
                for f in faqs:
                    all_faqs.append((f.get('name'), f.get('acceptedAnswer', {}).get('text')))
        except Exception:
            pass

print(f"\nUnique Keywords extracted across pages: {len(all_keywords)}")
print("Sample Keywords:", list(all_keywords)[:25])
print(f"\nSchema types discovered: {all_schemas_types}")
print(f"Total FAQs extracted: {len(all_faqs)}")
print("Sample page titles:")
for u, t in all_titles[:10]:
    print(f"  [{u.replace('https://rajputbhavin.engineer', '')}] -> {t}")

with open(r'H:\portfolio_website\tensix\competitor_audit.json', 'w', encoding='utf-8') as f:
    json.dump({
        "urls_count": len(urls),
        "keywords": sorted(list(all_keywords)),
        "page_titles": all_titles,
        "sample_faqs": all_faqs[:20]
    }, f, indent=2)

print("\nAudit saved to competitor_audit.json")
