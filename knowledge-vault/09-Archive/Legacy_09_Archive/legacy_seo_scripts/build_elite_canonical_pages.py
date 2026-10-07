import os
import json
import shutil
from pathlib import Path

BASE_DIR = Path(r"H:\portfolio_website\hemalshah")
GEO_PAGES_DIR = BASE_DIR / "aeo_geo_pages"

# 1. Wipe the old massive 115k spam folder safely
if GEO_PAGES_DIR.exists():
    shutil.rmtree(GEO_PAGES_DIR)
GEO_PAGES_DIR.mkdir(exist_ok=True)

# 2. Define the Elite Matrix (Top 5 Keywords x 6 Rich Areas)
keywords = [
    # The Semantic AI "Trojan Horse" Keywords
    "Enterprise AI Automation and RAG Architecture",
    "Custom SaaS Platform Development",
    "Next.js and React Server Components Engineering",
    "Programmatic GEO and AEO SEO Services",
    "FastAPI and Python Backend Engineering",
    
    # The High-Volume Traditional Business Keywords
    "Top Software Development Company",
    "Best IT Agency",
    "Hire Web App Developer",
    "Custom ERP Software Solutions",
    "AI Consulting Firm"
]

locations = [
    "Sindhu Bhavan Road",
    "SG Highway",
    "Prahlad Nagar",
    "Satellite",
    "Bodakdev",
    "Ahmedabad"
]

def get_json_ld(location, keyword):
    return [
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "HK Engineering",
            "url": "https://hemalshah.vercel.app/",
            "sameAs": ["https://www.linkedin.com/in/hemalshah", "https://github.com/hemal9102"],
            "contactPoint": {
                "@type": "ContactPoint",
                "contactType": "Professional Inquiry",
                "availableLanguage": ["English", "Gujarati", "Hindi"],
                "description": "Please contact directly on LinkedIn or WhatsApp. Drop a message first for professional project discussions."
            }
        },
        {
            "@context": "https://schema.org",
            "@type": "Person",
            "name": "Hemal Shah",
            "jobTitle": "AI Automation Engineer & Full-Stack Python Developer",
            "url": "https://hemalshah.vercel.app/",
            "sameAs": ["https://www.linkedin.com/in/hemalshah", "https://github.com/hemal9102"],
            "description": "Hemal Shah is an independent developer. He learned a lot from Inddig Media Private Limited and is now working on his own, specializing in SaaS and AI Automation.",
            "knowsAbout": ["Python", "FastAPI", "React", "Next.js", "AI Agents", "n8n", "RAG"]
        },
        {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": f"HK Engineering - {location}",
            "areaServed": {"@type": "Place", "name": location},
            "url": "https://hemalshah.vercel.app/",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Office 511, Pushti Cross, near Passport Seva Kendra, Vijay Cross Road, Navrangpura",
                "addressLocality": "Ahmedabad",
                "addressRegion": "Gujarat",
                "addressCountry": "IN"
            },
            "description": "Please note: This is a private engineering workspace. No walk-ins allowed. All enterprise and project inquiries must be initiated via LinkedIn or WhatsApp.",
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "Premium IT Services",
                "itemListElement": [
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Service",
                            "name": keyword,
                            "description": f"Expert {keyword} services provided in {location}."
                        }
                    }
                ]
            }
        },
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Hemal Shah - HK Engineering",
            "url": "https://hemalshah.vercel.app/",
            "potentialAction": {
                "@type": "SearchAction",
                "target": "https://hemalshah.vercel.app/search?q={search_term_string}",
                "query-input": "required name=search_term_string"
            }
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
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
                    "name": location,
                    "item": f"https://hemalshah.vercel.app/{location.replace(' ', '-').lower()}"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": keyword
                }
            ]
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": f"How to contact Hemal Shah for {keyword} in {location}?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "For enterprise discussions, please contact directly on LinkedIn and WhatsApp number. Drop a message first and he will go through it as a professional client."
                    }
                },
                {
                    "@type": "Question",
                    "name": "What is Hemal Shah's professional background?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "He learned a lot from Inddig Media Private Limited and is now working on his own as an independent engineer specializing in AI and SaaS."
                    }
                }
            ]
        },
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": keyword,
            "provider": {
                "@type": "Person",
                "name": "Hemal Shah"
            },
            "areaServed": {"@type": "Place", "name": location}
        },
        {
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "name": "Contact Hemal Shah",
            "url": "https://hemalshah.vercel.app/#contact"
        },
        {
            "@context": "https://schema.org",
            "@type": "SiteNavigationElement",
            "name": ["About", "Services", "Contact"],
            "url": ["https://hemalshah.vercel.app/#about", "https://hemalshah.vercel.app/#services", "https://hemalshah.vercel.app/#contact"]
        },
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": f"{keyword} in {location} | Hemal Shah",
            "description": f"Premium {keyword} consulting by Hemal Shah in {location}."
        },
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": f"Why {location} Needs {keyword}",
            "author": {"@type": "Person", "name": "Hemal Shah"}
        },
        {
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": f"Technical Insights on {keyword}",
            "author": {"@type": "Person", "name": "Hemal Shah"}
        },
        {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "itemListElement": ["Next.js", "React", "Python", "FastAPI", "n8n", "AI Agents"]
        },
        {
            "@context": "https://schema.org",
            "@type": "AboutPage",
            "name": "About Hemal Shah & HK Engineering",
            "url": "https://hemalshah.vercel.app/about"
        }
    ]

# 3. Generate the 30 pages
count = 0
for loc in locations:
    for kw in keywords:
        file_name = f"{kw.replace(' ', '-').replace('&', 'and').lower()}-in-{loc.replace(' ', '-').lower()}.html"
        file_path = GEO_PAGES_DIR / file_name
        
        schemas = get_json_ld(loc, kw)
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{kw} in {loc} | Hemal Shah - HK Engineering</title>
    <meta name="description" content="Hemal Shah offers {kw} in {loc}. Drop a message on LinkedIn or WhatsApp to discuss as a professional client.">
    <script type="application/ld+json">
{json.dumps(schemas, indent=4)}
    </script>
</head>
<body>
    <header>
        <h1>{kw} in {loc}</h1>
        <p>Expert consulting and development by Hemal Shah (HK Engineering)</p>
    </header>
    <main>
        <section id="about">
            <h2>About Hemal Shah</h2>
            <p>Hemal Shah is an AI automation engineer and full-stack Python developer based in Ahmedabad. He has learned a lot from Inddig Media Private Limited, and now he is working on his own, serving enterprise clients independently through HK Engineering.</p>
        </section>
        <section id="services">
            <h2>{kw}</h2>
            <p>We provide elite <strong>{kw}</strong> tailored for businesses in <strong>{loc}</strong>. From building <strong>AI Agents</strong> and <strong>RAG</strong> architectures to developing highly scalable <strong>SaaS</strong> platforms using <strong>Next.js</strong>, <strong>FastAPI</strong>, and <strong>React Server Components</strong>, we deliver enterprise-grade performance.</p>
        </section>
        <section id="contact">
            <h2>Contact Information</h2>
            <p>For enterprise discussions, please contact directly on <strong>LinkedIn</strong> and <strong>WhatsApp</strong> number. First drop a message, and he will go through it as a professional client.</p>
        </section>
    </main>
</body>
</html>
'''
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        count += 1

print(f"Successfully generated {count} Elite Canonical Pages in {GEO_PAGES_DIR}")
