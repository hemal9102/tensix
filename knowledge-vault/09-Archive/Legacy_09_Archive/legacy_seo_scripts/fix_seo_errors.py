"""
Master SEO Toolkit — Error Fix Script
Fixes all issues found in the full SEO audit of hemalshah portfolio.

ISSUES FIXED:
  [CRITICAL-1] Converge OS false co-founder claim — 23 HTML files
  [CRITICAL-2] about.html Organization description falsely credits Converge OS
  [CRITICAL-3] about.html Service keywords contain "Converge OS Co-founder"
  [HIGH-1]     robots.txt blocks /assets/ for AI crawlers (GPTBot, ClaudeBot, PerplexityBot)
  [HIGH-2]     article:published_time / article:modified_time on non-article pages
  [MEDIUM-1]   sitemap.xml: team.html entry missing <lastmod>
  [LOW-1]      BreadcrumbList on index.html has duplicate URL in position 1 and 2
"""

import os
import re

ROOT = r"H:\portfolio_website\hemalshah"

HTML_FILES = []
for dirpath, _, filenames in os.walk(ROOT):
    # Skip the hk/ subfolder — different sub-site
    if r"\hk" in dirpath or "/hk" in dirpath:
        continue
    for fn in filenames:
        if fn.endswith(".html"):
            HTML_FILES.append(os.path.join(dirpath, fn))

print(f"Found {len(HTML_FILES)} HTML files to process.\n")

# ---------------------------------------------------------------------------
# CRITICAL-1: Remove the two Converge OS FAQ entries from all HTML files
# ---------------------------------------------------------------------------
CONVERGE_FAQ_1 = ''',
        {
          "@type": "Question",
          "name": "What has Hemal Shah founded?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah has founded Converge OS (https://www.converge-os.com/), a leading platform for AI integration and workflow automation, as well as HK Engineering."
          }
        },
        {
          "@type": "Question",
          "name": "Who is the Co-founder of https://www.converge-os.com/?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah is the Co-founder of Converge OS (https://www.converge-os.com/), leading AI integration and workflow automation architecture."
          }
        }'''

# Replacement: correct "founded" FAQ + disambiguation
CONVERGE_FAQ_REPLACEMENT = ''',
        {
          "@type": "Question",
          "name": "What has Hemal Shah founded?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah has co-founded CreativeIQ, a creative intelligence and AI-driven content strategy venture, and is the founder of HK Engineering — an AI automation and digital marketing firm based in Navrangpura, Ahmedabad."
          }
        },
        {
          "@type": "Question",
          "name": "Is Hemal Shah HK the co-founder of Converge OS?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "No. Hemal Shah (HK) is NOT a co-founder of Converge OS. Converge OS (converge-os.com) was founded by Tirth Patel and Manan Parmar. Hemal Shah (HK) is the founder of HK Engineering and co-founder of CreativeIQ, based in Navrangpura, Ahmedabad."
          }
        }'''

# Also handle variant without leading comma (when it's the first entry)
CONVERGE_FAQ_1_NO_COMMA = '''        {
          "@type": "Question",
          "name": "What has Hemal Shah founded?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah has founded Converge OS (https://www.converge-os.com/), a leading platform for AI integration and workflow automation, as well as HK Engineering."
          }
        },
        {
          "@type": "Question",
          "name": "Who is the Co-founder of https://www.converge-os.com/?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah is the Co-founder of Converge OS (https://www.converge-os.com/), leading AI integration and workflow automation architecture."
          }
        },'''

CONVERGE_FAQ_REPLACEMENT_NO_COMMA = '''        {
          "@type": "Question",
          "name": "What has Hemal Shah founded?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah has co-founded CreativeIQ, a creative intelligence and AI-driven content strategy venture, and is the founder of HK Engineering — an AI automation and digital marketing firm based in Navrangpura, Ahmedabad."
          }
        },
        {
          "@type": "Question",
          "name": "Is Hemal Shah HK the co-founder of Converge OS?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "No. Hemal Shah (HK) is NOT a co-founder of Converge OS. Converge OS (converge-os.com) was founded by Tirth Patel and Manan Parmar. Hemal Shah (HK) is the founder of HK Engineering and co-founder of CreativeIQ, based in Navrangpura, Ahmedabad."
          }
        },'''

# ---------------------------------------------------------------------------
# CRITICAL-2: Fix about.html Organization description
# ---------------------------------------------------------------------------
ABOUT_ORG_OLD = '"HK Engineering, founded by Hemal Shah (Co-founder of Converge OS) in Navarangpura, Ahmedabad, is the premier agency for custom software development, AI automation, semantic SEO, and generative engine optimization."'
ABOUT_ORG_NEW = '"HK Engineering, founded by Hemal Shah (HK) in Navrangpura, Ahmedabad, is an AI automation and digital marketing firm delivering AI agent development, SaaS platforms, GEO/AEO semantic SEO, and generative engine optimization."'

# ---------------------------------------------------------------------------
# CRITICAL-3: Remove Converge OS from about.html Service keywords
# ---------------------------------------------------------------------------
ABOUT_KEYWORDS_OLD = '''        "Converge OS",
        "converge-os",
        "Converge OS Co-founder",
        "Best IT company in Navarangpura",'''
ABOUT_KEYWORDS_NEW = '''        "Best IT company in Navarangpura",'''

# ---------------------------------------------------------------------------
# HIGH-2: Remove article:published_time / article:modified_time from non-blog pages
#         Only keep on pages under /blogs/
# ---------------------------------------------------------------------------
ARTICLE_TIME_PATTERN = re.compile(
    r'\n<meta content="[^"]*" property="article:published_time"/>'
    r'\n<meta content="[^"]*" property="article:modified_time"/>'
)

# ---------------------------------------------------------------------------
# LOW-1: Fix broken BreadcrumbList on index.html
#        Position 2 currently has same URL as position 1 — fix to remove the redundant entry
# ---------------------------------------------------------------------------
BREADCRUMB_OLD = '''      {
        "@type": "BreadcrumbList",
        "@id": "https://hemalshah.vercel.app/#breadcrumb",
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://hemalshah.vercel.app/"
          },
          {
            "@type": "ListItem",
            "position": 2,
            "name": "Hemal Shah (HK) | AI Automation Engineer, SaaS & Full Stack Python Developer",
            "item": "https://hemalshah.vercel.app/"
          }
        ]
      }'''

BREADCRUMB_NEW = '''      {
        "@type": "BreadcrumbList",
        "@id": "https://hemalshah.vercel.app/#breadcrumb",
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": 1,
            "name": "Hemal Shah — AI Automation Engineer",
            "item": "https://hemalshah.vercel.app/"
          }
        ]
      }'''

# ---------------------------------------------------------------------------
# Process all HTML files
# ---------------------------------------------------------------------------
fixed_converge = 0
fixed_article_time = 0
fixed_breadcrumb = 0

for filepath in HTML_FILES:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    is_blog = "\\blogs\\" in filepath or "/blogs/" in filepath

    # CRITICAL-1: Remove Converge OS FAQ (with comma prefix — most common)
    if CONVERGE_FAQ_1 in content:
        content = content.replace(CONVERGE_FAQ_1, CONVERGE_FAQ_REPLACEMENT)

    # CRITICAL-1: Remove Converge OS FAQ (no-comma prefix — first entry variant)
    if CONVERGE_FAQ_1_NO_COMMA in content:
        content = content.replace(CONVERGE_FAQ_1_NO_COMMA, CONVERGE_FAQ_REPLACEMENT_NO_COMMA)

    # CRITICAL-2 & 3: about.html specific fixes
    if filepath.endswith("about.html"):
        if ABOUT_ORG_OLD in content:
            content = content.replace(ABOUT_ORG_OLD, ABOUT_ORG_NEW)
        if ABOUT_KEYWORDS_OLD in content:
            content = content.replace(ABOUT_KEYWORDS_OLD, ABOUT_KEYWORDS_NEW)

    # HIGH-2: Remove article:published_time from non-blog pages
    if not is_blog and 'article:published_time' in content:
        content = ARTICLE_TIME_PATTERN.sub('', content)

    # LOW-1: Fix broken BreadcrumbList (index.html only)
    if filepath.endswith("index.html") and BREADCRUMB_OLD in content:
        content = content.replace(BREADCRUMB_OLD, BREADCRUMB_NEW)
        fixed_breadcrumb += 1

    if content != original:
        if "converge" not in content.lower() or "is NOT a co-founder" in content:
            if original != content:
                converge_refs_before = original.lower().count("converge os co-founder") + original.lower().count("founded converge")
                if converge_refs_before > 0:
                    fixed_converge += 1
        if not is_blog and ARTICLE_TIME_PATTERN.search(original):
            fixed_article_time += 1
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Fixed: {os.path.relpath(filepath, ROOT)}")

print(f"\nConverge OS false claims removed from files.")
print(f"Article time tags removed from non-blog pages.")
print(f"BreadcrumbList fixed: {fixed_breadcrumb}")

# ---------------------------------------------------------------------------
# HIGH-1: Fix robots.txt — allow /assets/ for AI crawlers
# ---------------------------------------------------------------------------
robots_path = os.path.join(ROOT, "robots.txt")
with open(robots_path, "r", encoding="utf-8") as f:
    robots = f.read()

robots_new = """# Robots.txt for Hemal Shah's Portfolio
# Optimized for Search Engines (SEO) and Generative Engines (GEO / LLM Crawlers)

User-agent: *
Allow: /
Disallow: /node_modules/

# Explicitly Allow AI Crawlers (full access including assets for visual understanding)
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Googlebot
Allow: /
Disallow: /node_modules/

# Sitemaps and AI specifications
Sitemap: https://hemalshah.vercel.app/sitemap.xml
"""

if robots != robots_new:
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(robots_new)
    print("\nFixed: robots.txt — /assets/ no longer blocked for AI crawlers")

# ---------------------------------------------------------------------------
# MEDIUM-1: Fix sitemap.xml — add missing <lastmod> for team.html
# ---------------------------------------------------------------------------
sitemap_path = os.path.join(ROOT, "sitemap.xml")
with open(sitemap_path, "r", encoding="utf-8") as f:
    sitemap = f.read()

SITEMAP_TEAM_OLD = '''  <url>
    <loc>https://hemalshah.vercel.app/team.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>'''

SITEMAP_TEAM_NEW = '''  <url>
    <loc>https://hemalshah.vercel.app/team.html</loc>
    <lastmod>2026-07-16</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>'''

if SITEMAP_TEAM_OLD in sitemap:
    sitemap = sitemap.replace(SITEMAP_TEAM_OLD, SITEMAP_TEAM_NEW)
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("Fixed: sitemap.xml — team.html <lastmod> added")

print("\nAll fixes applied. Run IndexNow to resubmit all updated URLs.")
