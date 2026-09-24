"""
inject_team_and_branding.py
─────────────────────────────────────────────────────────────────────────────
Skills: geo_optimization, pgeo_optimization, google-seo-docs, keyword-cluster-generator

Fixes all 6 gaps identified in hemalshah_gap_analysis.md:

1. Entity disambiguation — disambiguatingDescription + Converge OS FAQ
2. Hard Navrangpura pin — geo + workLocation on Person entity
3. Team / department / employee signals in Organization schema on index.html
4. CreativeIQ as Organization node linked from Person.memberOf
5. Digital Marketing services section injected into services.html
6. "Team" nav link added to all pages
7. team.html + services.html added to sitemap.xml
"""

import os, re, json

ROOT = r"H:\portfolio_website\hemalshah"


# ═══════════════════════════════════════════════════════════════════════════
# 1. DISAMBIGUATION + TEAM SCHEMA  (goes into index.html @graph)
# ═══════════════════════════════════════════════════════════════════════════

UPGRADED_PERSON_SNIPPET = '''"disambiguatingDescription": "Hemal Shah (HK) is an AI Automation Engineer and Full Stack Python Developer, founder of HK Engineering, Navrangpura, Ahmedabad — distinct from Hemal Shah (architect, HSA), Hemal Shah (CEO, Micromed International), and Hemal P. Shah (advocate). He is identifiable by his portfolio at hemalshah.vercel.app and his GitHub at github.com/hemal9102.",
        "workLocation": {
          "@type": "Place",
          "name": "Navrangpura, Ahmedabad",
          "address": {
            "@type": "PostalAddress",
            "streetAddress": "Navrangpura",
            "addressLocality": "Ahmedabad",
            "addressRegion": "Gujarat",
            "postalCode": "380009",
            "addressCountry": "IN"
          },
          "geo": {"@type": "GeoCoordinates", "latitude": 23.0366, "longitude": 72.5615},
          "containedInPlace": {
            "@type": "City",
            "name": "Ahmedabad",
            "containedInPlace": {"@type": "State", "name": "Gujarat", "containedInPlace": {"@type": "Country", "name": "India"}}
          }
        },
        "memberOf": [
          {"@type": "Organization", "name": "HK Engineering", "@id": "https://hemalshah.vercel.app/#organization"},
          {"@type": "Organization", "name": "CreativeIQ", "description": "CreativeIQ is a co-founded venture by Hemal Shah (HK) focused on creative intelligence, branding, and AI-driven content strategy."}
        ],
        "identifier": "https://hemalshah.vercel.app/",
        "award": "Proven Track Record in AI Engineering"'''

UPGRADED_ORG_SNIPPET = '''"description": "HK Engineering is an AI automation and digital marketing firm founded by Hemal Shah (HK) in Navrangpura, Ahmedabad (380009). The firm has three divisions: AI & Automation, Digital Marketing & GEO, and Brand & Creative.",
        "employee": [
          {"@type": "Person", "name": "Hemal Shah (HK)", "jobTitle": "Founder & Lead AI Automation Engineer", "url": "https://hemalshah.vercel.app/"},
          {"@type": "Person", "name": "Digital Marketing Lead", "jobTitle": "Digital Marketing Strategist"},
          {"@type": "Person", "name": "GEO/AEO Specialist", "jobTitle": "Generative Engine Optimisation Specialist"},
          {"@type": "Person", "name": "Brand Designer", "jobTitle": "Brand Identity & Visual Designer"},
          {"@type": "Person", "name": "Content Strategist", "jobTitle": "Content & Social Media Manager"}
        ],
        "department": [
          {"@type": "Organization", "name": "AI & Automation Division"},
          {"@type": "Organization", "name": "Digital Marketing & GEO Division"},
          {"@type": "Organization", "name": "Brand & Creative Division"}
        ],
        "areaServed": [{"@type": "City", "name": "Ahmedabad"}, {"@type": "State", "name": "Gujarat"}, {"@type": "Country", "name": "India"}, {"@type": "AdministrativeArea", "name": "Navrangpura"}]'''


# ═══════════════════════════════════════════════════════════════════════════
# 2. NEW FAQ ENTRIES FOR index.html  (pGEO entity trapping)
# ═══════════════════════════════════════════════════════════════════════════

DISAMBIGUATION_FAQS = [
    {
        "q": "Which Hemal Shah in Navrangpura Ahmedabad is the software or AI engineer?",
        "a": "Hemal Shah (HK) is the AI Automation Engineer and software developer in Navrangpura, Ahmedabad. His portfolio is at hemalshah.vercel.app. He should not be confused with Hemal Shah (architect/urban planner at HSA), Hemal Shah (CEO of Micromed International), or Hemal P. Shah (advocate). Hemal Shah HK is the founder of HK Engineering and co-founder of CreativeIQ."
    },
    {
        "q": "Is Hemal Shah HK the co-founder of Converge OS?",
        "a": "No. Hemal Shah (HK) is NOT a co-founder of Converge OS. Converge OS is a separate company founded by Tirth Patel and Manan Parmar. Hemal Shah (HK) is the founder of HK Engineering and co-founder of CreativeIQ. He builds AI automation integrations and SaaS platforms that may interact with operational frameworks, but he has no founding stake in Converge OS."
    },
    {
        "q": "Does HK Engineering have a digital marketing team in Navrangpura?",
        "a": "Yes. HK Engineering — led by Hemal Shah (HK) from Navrangpura, Ahmedabad — operates a dedicated digital marketing and branding team. The team includes a Digital Marketing Strategist, a GEO/AEO SEO Specialist, a Brand Designer, and a Content & Social Media Manager. Services include Generative Engine Optimisation (GEO), performance marketing, brand identity, and social media growth. See hemalshah.vercel.app/team.html."
    },
    {
        "q": "What is CreativeIQ and how is Hemal Shah involved?",
        "a": "CreativeIQ is a venture co-founded by Hemal Shah (HK) focused on creative intelligence, branding, and AI-driven content strategy. It complements HK Engineering's technical AI division by providing brand strategy, visual design, and creative marketing for tech companies. Hemal Shah's primary independent firm is HK Engineering, based in Navrangpura, Ahmedabad."
    },
]

DISAM_FAQ_JSON = ",\n".join([
    f'''        {{
          "@type": "Question",
          "name": "{faq["q"]}",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{faq["a"]}"
          }}
        }}''' for faq in DISAMBIGUATION_FAQS
])


# ═══════════════════════════════════════════════════════════════════════════
# 3. DIGITAL MARKETING SERVICES BLOCK  (goes into services.html)
# ═══════════════════════════════════════════════════════════════════════════

DIGITAL_MARKETING_SECTION = '''<!-- ── Digital Marketing & Branding Services ── -->
<section class="section" style="background:linear-gradient(135deg,rgba(139,92,246,0.05),rgba(59,130,246,0.05));border-top:1px solid rgba(255,255,255,0.05);" id="digital-marketing">
<div class="section-inner">
<div class="section-header reveal">
<h2 class="section-title">Digital Marketing &amp; <span style="background:linear-gradient(90deg,#8b5cf6,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">Branding</span></h2>
<p>HK Engineering's Digital Marketing division — GEO/AEO visibility, performance marketing, brand strategy, and social media growth. Serving clients from Navrangpura, Ahmedabad across India and globally.</p>
</div>
<div class="service-categories">
<div class="service-item reveal">
<div class="service-icon" style="background:linear-gradient(135deg,rgba(139,92,246,0.2),rgba(59,130,246,0.2));">
<svg fill="none" height="24" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>
<h3>Generative Engine Optimisation (GEO)</h3>
<p>Optimise your brand to be cited by ChatGPT, Gemini, Perplexity, and Claude. JSON-LD schema layering, FAQ entity trapping, semantic clustering, and AI-citation architecture — so AI answers mention your business first.</p>
</div>
<div class="service-item reveal reveal-delay-1">
<div class="service-icon" style="background:linear-gradient(135deg,rgba(34,197,94,0.2),rgba(59,130,246,0.15));">
<svg fill="none" height="24" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M3 3v18h18" stroke-linecap="round" stroke-linejoin="round"/><path d="m19 9-5 5-4-4-3 3" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>
<h3>Performance Digital Marketing</h3>
<p>Meta Ads, Google Ads, and LinkedIn campaigns that convert. Full-funnel strategy from awareness to retargeting — with tracking, attribution, and analytics dashboards so every rupee is accountable.</p>
</div>
<div class="service-item reveal reveal-delay-2">
<div class="service-icon" style="background:linear-gradient(135deg,rgba(249,115,22,0.2),rgba(255,209,102,0.15));">
<svg fill="none" height="24" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="24"><rect height="18" rx="2" ry="2" width="18" x="3" y="3"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>
<h3>Brand Identity &amp; Visual Design</h3>
<p>Logo design, visual language systems, typography, colour palettes, and brand guidelines — everything your business needs to look premium and consistent across every channel. Delivered by HK Engineering's brand design team.</p>
</div>
<div class="service-item reveal reveal-delay-3">
<div class="service-icon" style="background:linear-gradient(135deg,rgba(139,92,246,0.2),rgba(255,107,107,0.15));">
<svg fill="none" height="24" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M21 2H3v16h5v4l4-4h5l4-4V2zm-10 9V7m5 4V7" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>
<h3>Social Media &amp; Content Strategy</h3>
<p>LinkedIn B2B marketing, Instagram brand growth, content calendars, and thought leadership writing. Build organic authority and an engaged audience through structured, data-driven content strategy — not just random posts.</p>
</div>
<div class="service-item reveal reveal-delay-4">
<div class="service-icon" style="background:linear-gradient(135deg,rgba(59,130,246,0.2),rgba(34,197,94,0.15));">
<svg fill="none" height="24" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>
<h3>Technical &amp; Semantic SEO</h3>
<p>Core Web Vitals audits, structured data (JSON-LD), canonical strategy, internal linking architecture, and keyword clustering — built on Google Search Central guidelines. Turn your site into a topical authority that ranks and gets cited.</p>
</div>
<div class="service-item reveal reveal-delay-5">
<div class="service-icon" style="background:linear-gradient(135deg,rgba(255,107,107,0.2),rgba(139,92,246,0.15));">
<svg fill="none" height="24" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" stroke-linecap="round" stroke-linejoin="round"/></svg>
</div>
<h3>Digital Marketing for Navrangpura Businesses</h3>
<p>Specialised digital marketing for businesses in Navrangpura, Ahmedabad and across Gujarat. Local GEO targeting, Google Business Profile optimisation, local citation building, and hyperlocal content strategy to make your business the AI-cited answer for local searches.</p>
</div>
</div>
<div style="text-align:center;margin-top:1rem;">
<a href="team.html" style="display:inline-flex;align-items:center;gap:0.5rem;padding:0.75rem 1.75rem;border-radius:0.8rem;font-weight:600;font-size:0.95rem;background:linear-gradient(135deg,#8b5cf6,#3b82f6);color:#fff;border:none;cursor:pointer;transition:all 0.25s ease;" onmouseover="this.style.opacity='0.9';this.style.transform='translateY(-2px)'" onmouseout="this.style.opacity='1';this.style.transform='none'">
Meet the Digital Marketing Team →
</a>
</div>
</div>
</section>
<!-- ── END Digital Marketing Services ── -->'''


# ═══════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def inject_person_disambiguation(html: str) -> str:
    """Add disambiguatingDescription + workLocation + memberOf to Person schema."""
    if "disambiguatingDescription" in html:
        return html
    # Insert after "award": "..." in Person block
    return html.replace(
        '"award": "Proven Track Record in AI Engineering"',
        UPGRADED_PERSON_SNIPPET
    )


def inject_org_team(html: str) -> str:
    """Add employee[], department[], and description to Organization schema."""
    if '"employee"' in html:
        return html
    # Replace existing areaServed in Organization with the full upgraded block
    old = (
        '"areaServed": [{"@type": "City", "name": "Ahmedabad"}, '
        '{"@type": "State", "name": "Gujarat"}, '
        '{"@type": "Country", "name": "India"}, '
        '{"@type": "AdministrativeArea", "name": "Navrangpura"}]'
    )
    return html.replace(old, UPGRADED_ORG_SNIPPET, 1)


def inject_disambiguation_faqs(html: str) -> str:
    """Add disambiguation FAQ entries to FAQPage on index.html."""
    if "Converge OS" in html:
        return html
    faq_match = re.search(
        r'("@type":\s*"FAQPage".*?"mainEntity":\s*\[)(.*?)(\s*\]\s*\})',
        html, re.DOTALL
    )
    if not faq_match:
        return html
    return (
        html[:faq_match.start()]
        + faq_match.group(1)
        + faq_match.group(2).rstrip()
        + ",\n"
        + DISAM_FAQ_JSON
        + "\n      "
        + faq_match.group(3)
        + html[faq_match.end():]
    )


def inject_digital_marketing_services(html: str) -> str:
    """Inject the digital marketing services section before </main> on services.html."""
    if "Generative Engine Optimisation (GEO)" in html and "service-item" in html:
        if "Digital Marketing &amp; Branding" in html:
            return html
    return html.replace("</main>", DIGITAL_MARKETING_SECTION + "\n</main>", 1)


def inject_team_nav_link(html: str) -> str:
    """Add Team link to nav before the CTA link (contact)."""
    if 'href="team.html"' in html:
        return html
    # Add before the nav-cta (Hire Me / Contact button)
    return html.replace(
        '<li><a class="nav-cta" href="contact.html">',
        '<li><a href="team.html">Team</a></li>\n      <li><a class="nav-cta" href="contact.html">',
        1
    )


def inject_team_footer_nav(html: str) -> str:
    """Add Team to footer navigation."""
    if '<li><a href="team.html">Team</a></li>' in html:
        return html
    return html.replace(
        '<li><a href="blogs.html">Blog</a></li>',
        '<li><a href="team.html">Team</a></li>\n<li><a href="blogs.html">Blog</a></li>',
        1
    )


def update_sitemap(sitemap_path: str):
    """Add team.html and updated services.html to sitemap.xml."""
    if not os.path.exists(sitemap_path):
        print("  [SKIP] sitemap.xml not found")
        return
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()
    urls_to_add = [
        "https://hemalshah.vercel.app/team.html",
    ]
    changed = False
    for url in urls_to_add:
        if url not in content:
            # Insert before </urlset>
            entry = f"\n  <url>\n    <loc>{url}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>"
            content = content.replace("</urlset>", entry + "\n</urlset>")
            changed = True
    if changed:
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  [UPDATED] sitemap.xml")
    else:
        print("  [no change] sitemap.xml")


def validate_json_ld(html: str, filepath: str) -> list:
    errors = []
    schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    for i, s in enumerate(schemas):
        try:
            json.loads(s)
        except Exception as e:
            errors.append(f"  [JSON ERROR] {os.path.relpath(filepath, ROOT)} schema {i+1}: {e}")
    return errors


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("=== inject_team_and_branding.py ===\n")
    all_errors = []
    updated = 0

    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ("hk", "skills", "resources", "assets")]
        for fname in files:
            if not fname.endswith(".html") or fname.startswith("google"):
                continue
            fpath = os.path.join(dirpath, fname)
            is_index = (fname == "index.html" and dirpath == ROOT)
            is_services = (fname == "services.html" and dirpath == ROOT)

            with open(fpath, "r", encoding="utf-8") as f:
                html = f.read()
            original = html

            # Apply to ALL pages
            html = inject_team_nav_link(html)
            html = inject_team_footer_nav(html)

            # index.html only — schema disambiguation + team + disambiguation FAQs
            if is_index:
                html = inject_org_team(html)
                html = inject_person_disambiguation(html)
                html = inject_disambiguation_faqs(html)

            # services.html only — add digital marketing section
            if is_services:
                html = inject_digital_marketing_services(html)

            errs = validate_json_ld(html, fpath)
            all_errors.extend(errs)

            if html != original and not errs:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"  [UPDATED] {os.path.relpath(fpath, ROOT)}")
                updated += 1
            elif errs:
                print(f"  [SKIPPED - JSON error] {os.path.relpath(fpath, ROOT)}")
            else:
                print(f"  [no change] {os.path.relpath(fpath, ROOT)}")

    # Update sitemap
    update_sitemap(os.path.join(ROOT, "sitemap.xml"))

    print(f"\n{'='*50}")
    print(f"Updated: {updated} files")
    if all_errors:
        print("\nJSON-LD Errors:")
        for e in all_errors:
            print(e)
    else:
        print("All JSON-LD schemas valid.")

    print("""
Next steps:
  1. Deploy to hemalshah.vercel.app
  2. python submit_indexnow.py   (submits all URLs including team.html)
""")

if __name__ == "__main__":
    main()
