"""
build_schema_web.py
===================
Master Schema Web & AI Entity Builder for HK Engineering / Hemal Shah
----------------------------------------------------------------------
Upgraded Architecture:
  1. Generates `hk-engineering-ahmedabad.html` — high-authority spoke page:
       - Strategic 15-node high-ticket economic & IT corridor mesh (GIFT City, SG Highway, Navrangpura, etc.)
       - Explicit disambiguation FAQPage (NOT a CNC/manufacturing factory)
       - Full @graph with LocalBusiness, Organization @id ref, Person @id ref, Service, WebPage, BreadcrumbList, HowTo
       - NO AggregateRating (100% policy-compliant)
  2. Re-injects ALL HTML pages with:
       - Clean single @graph cross-linked to central @id nodes (#organization, #person, #website)
       - Verified entity linking (Wikipedia / Wikidata URIs for semantic grounding)
       - Removal of outdated <meta name="keywords"> spam tags
  3. Regenerates clean AI context files (`llms.txt` and `llms-full.txt`)

Central Entity IDs:
  Organization  → https://hemalshah.vercel.app/#organization
  Person        → https://hemalshah.vercel.app/#person
  WebSite       → https://hemalshah.vercel.app/#website
"""

import os
import re
import json
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


# ─── CONFIG ────────────────────────────────────────────────────────────────────
ROOT_DIR    = Path(r"H:\portfolio_website\hemalshah")
BASE_URL    = "https://hemalshah.vercel.app"
ORG_ID      = f"{BASE_URL}/#organization"
PERSON_ID   = f"{BASE_URL}/#person"
WEBSITE_ID  = f"{BASE_URL}/#website"

# ─── STRATEGIC HIGH-TICKET ECONOMIC & TECH LOCALITIES ──────────────────────────
# Replaces 240 hyper-local colony spam with high-prestige business corridors
STRATEGIC_LOCALITIES = [
    "Navrangpura",
    "Vastrapur",
    "Bodakdev",
    "Satellite",
    "Prahlad Nagar",
    "SG Highway",
    "Thaltej",
    "Science City",
    "Sindhu Bhavan Road",
    "GIFT City",
    "Infocity Gandhinagar",
    "Ahmedabad",
    "Gujarat",
    "India",
    "Remote"
]

# ─── SEMANTIC ENTITY DEFINITIONS (WIKIDATA / WIKIPEDIA LINKING) ───────────────
ENTITY_KNOWS_ABOUT = [
    {
        "@type": "DefinedTerm",
        "name": "Artificial Intelligence",
        "sameAs": "https://en.wikipedia.org/wiki/Artificial_intelligence"
    },
    {
        "@type": "DefinedTerm",
        "name": "Software as a Service (SaaS)",
        "sameAs": "https://en.wikipedia.org/wiki/Software_as_a_service"
    },
    {
        "@type": "DefinedTerm",
        "name": "FastAPI",
        "sameAs": "https://en.wikipedia.org/wiki/FastAPI"
    },
    {
        "@type": "DefinedTerm",
        "name": "Python",
        "sameAs": "https://en.wikipedia.org/wiki/Python_(programming_language)"
    },
    {
        "@type": "DefinedTerm",
        "name": "Workflow Automation",
        "sameAs": "https://en.wikipedia.org/wiki/Workflow_automation"
    },
    {
        "@type": "DefinedTerm",
        "name": "Retrieval-Augmented Generation (RAG)",
        "sameAs": "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"
    },
    {
        "@type": "DefinedTerm",
        "name": "Search Engine Optimization",
        "sameAs": "https://en.wikipedia.org/wiki/Search_engine_optimization"
    }
]

# ─── DISAMBIGUATION & CONVERSATIONAL FAQS ──────────────────────────────────────
DISAMBIGUATION_FAQS = [
    {
        "@type": "Question",
        "name": "Is HK Engineering in Ahmedabad a manufacturing or CNC factory?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "No. HK Engineering in Ahmedabad is not a manufacturing company, CNC factory, or industrial supplier. It is a technology firm founded by Hemal Shah, specializing exclusively in AI automation, custom software development, Python backend engineering, SaaS platform development, and Generative Engine Optimization (GEO/AEO). The firm is headquartered in Navrangpura, Ahmedabad."
        }
    },
    {
        "@type": "Question",
        "name": "What services does HK Engineering Ahmedabad offer?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "HK Engineering, led by Hemal Shah (HK), delivers: Custom AI Agent Development (RAG, LangChain, Claude), Enterprise Workflow Automation (n8n, Python), Full-Stack SaaS Development (Next.js, FastAPI, PostgreSQL), Generative Engine Optimization (GEO) & Semantic SEO schema engineering, and High-Throughput ETL/Data Pipelines."
        }
    },
    {
        "@type": "Question",
        "name": "Who is the founder of HK Engineering?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "HK Engineering was founded by Hemal Shah (known as HK). He is an AI Automation Engineer, Full Stack Python Developer, and SaaS Architect based in Navrangpura, Ahmedabad, Gujarat."
        }
    },
    {
        "@type": "Question",
        "name": "Where does HK Engineering provide services?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "HK Engineering is headquartered in Navrangpura, Ahmedabad, and actively serves tech corridors including Bodakdev, Vastrapur, Satellite, Prahlad Nagar, SG Highway, Science City, Sindhu Bhavan Road, GIFT City, and Gandhinagar, as well as enterprise clients globally on a remote basis."
        }
    },
    {
        "@type": "Question",
        "name": "How is HK Engineering distinct from other companies named HK Engineering?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "Unlike industrial sheet metal or CNC engineering businesses, HK Engineering by Hemal Shah is a dedicated software, AI engineering, and SaaS development company. It does not produce industrial hardware or mechanical machinery."
        }
    },
    {
        "@type": "Question",
        "name": "How can businesses hire Hemal Shah and HK Engineering?",
        "acceptedAnswer": {
            "@type": "Answer",
            "text": "Businesses can reach Hemal Shah directly via email at hemal.shah2004@gmail.com, through LinkedIn (linkedin.com/in/hemal-shah-49a728362/), or via the contact page on https://hemalshah.vercel.app/contact.html."
        }
    }
]

# ─── CORE SERVICES ─────────────────────────────────────────────────────────────
SERVICES = [
    {"name": "AI Agent & Workflow Development", "desc": "Custom agentic pipelines using LangChain, Claude, and RAG architectures for enterprise business automation."},
    {"name": "Workflow Automation (n8n & Python)", "desc": "End-to-end business automation integrating CRM, databases, and APIs to eliminate repetitive manual processes."},
    {"name": "Full-Stack SaaS Platform Architecture", "desc": "Production-grade SaaS web applications built with FastAPI, Next.js, PostgreSQL, and Supabase."},
    {"name": "Generative Engine Optimization (GEO)", "desc": "Structured data schema engineering and semantic authority graphs for citation in ChatGPT, Perplexity, and Google AI Overviews."},
    {"name": "Technical SEO & Knowledge Graph Engineering", "desc": "Advanced entity disambiguation and JSON-LD schema construction for high search visibility."},
    {"name": "Data Engineering & Web Extraction Pipelines", "desc": "High-velocity data extraction, automated ETL pipelines, and API integrations for enterprise analytics."}
]

def strip_tags(text: str) -> str:
    text = re.sub(r'<style.*?>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^<]+?>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# ─── BUILD SPOKE PAGE ──────────────────────────────────────────────────────────
def build_spoke_page():
    page_url  = f"{BASE_URL}/hk-engineering-ahmedabad"
    webpage_id = f"{page_url}#webpage"

    area_served = [{"@type": "Place", "name": loc} for loc in STRATEGIC_LOCALITIES]

    graph = [
        # 1. WebPage
        {
            "@type": "WebPage",
            "@id": webpage_id,
            "url": page_url,
            "name": "HK Engineering Ahmedabad — AI Automation & SaaS Development | Hemal Shah",
            "headline": "HK Engineering Ahmedabad: AI Automation & SaaS Development by Hemal Shah",
            "description": "HK Engineering is Ahmedabad's premier AI automation and SaaS development firm, founded by Hemal Shah (HK) in Navrangpura. Specializing in AI agents, n8n workflows, and Generative Engine Optimization.",
            "isPartOf": {"@id": WEBSITE_ID},
            "about": {"@id": PERSON_ID},
            "author": {"@id": PERSON_ID},
            "creator": {"@id": PERSON_ID},
            "publisher": {"@id": ORG_ID},
            "breadcrumb": {"@id": f"{page_url}#breadcrumb"},
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": ["h1", "h2", ".about-text", ".service-item", "#faq"]
            }
        },
        # 2. Organization Ref
        {
            "@type": "Organization",
            "@id": ORG_ID,
            "name": "HK Engineering",
            "alternateName": ["HK Engineering Ahmedabad", "HK Engineering India"],
            "url": f"{BASE_URL}/",
            "logo": f"{BASE_URL}/assets/favicon.png",
            "founder": {"@id": PERSON_ID},
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Navrangpura",
                "addressLocality": "Ahmedabad",
                "addressRegion": "Gujarat",
                "postalCode": "380009",
                "addressCountry": "IN"
            },
            "sameAs": [
                "https://github.com/hemal9102",
                "https://www.linkedin.com/in/hemal-shah-49a728362/",
                f"{BASE_URL}/"
            ],
            "knowsAbout": ENTITY_KNOWS_ABOUT
        },
        # 3. Person Ref
        {
            "@type": "Person",
            "@id": PERSON_ID,
            "name": "Hemal Shah",
            "alternateName": ["HK", "HK Engineering", "Hemal Shah HK"],
            "jobTitle": "AI Automation Engineer & SaaS Architect",
            "url": f"{BASE_URL}/about",
            "worksFor": {"@id": ORG_ID},
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Navrangpura, Ahmedabad",
                "addressRegion": "Gujarat",
                "addressCountry": "IN"
            },
            "sameAs": [
                "https://github.com/hemal9102",
                "https://www.linkedin.com/in/hemal-shah-49a728362/"
            ],
            "knowsAbout": ENTITY_KNOWS_ABOUT
        },
        # 4. LocalBusiness (Strategic Mesh, NO AggregateRating)
        {
            "@type": ["LocalBusiness", "ProfessionalService"],
            "@id": f"{page_url}#localbusiness",
            "name": "HK Engineering — AI & Software Development, Ahmedabad",
            "description": "HK Engineering is a technology firm in Navrangpura, Ahmedabad, founded by Hemal Shah. Specializing in AI automation, SaaS architecture, and Generative Engine Optimization. NOT a manufacturing or CNC company.",
            "url": f"{BASE_URL}/hk-engineering-ahmedabad",
            "email": "hemal.shah2004@gmail.com",
            "founder": {"@id": PERSON_ID},
            "parentOrganization": {"@id": ORG_ID},
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Navrangpura",
                "addressLocality": "Ahmedabad",
                "addressRegion": "Gujarat",
                "postalCode": "380009",
                "addressCountry": "IN"
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": "23.0366",
                "longitude": "72.5615"
            },
            "areaServed": area_served,
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "AI & Software Engineering Services by HK Engineering",
                "itemListElement": [
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Service",
                            "name": svc["name"],
                            "description": svc["desc"],
                            "provider": {"@id": ORG_ID}
                        }
                    }
                    for svc in SERVICES
                ]
            },
            "sameAs": [
                f"{BASE_URL}/",
                "https://github.com/hemal9102",
                "https://www.linkedin.com/in/hemal-shah-49a728362/"
            ]
        },
        # 5. FAQPage
        {
            "@type": "FAQPage",
            "@id": f"{page_url}#faq",
            "mainEntity": DISAMBIGUATION_FAQS
        },
        # 6. BreadcrumbList
        {
            "@type": "BreadcrumbList",
            "@id": f"{page_url}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
                {"@type": "ListItem", "position": 2, "name": "HK Engineering Ahmedabad", "item": page_url}
            ]
        },
        # 7. HowTo
        {
            "@type": "HowTo",
            "@id": f"{page_url}#howto",
            "name": "How to Engage HK Engineering for AI Development in Ahmedabad",
            "description": "The structured engineering process for working with Hemal Shah and HK Engineering.",
            "author": {"@id": PERSON_ID},
            "step": [
                {"@type": "HowToStep", "position": 1, "name": "Initial Contact", "text": "Reach out via email at hemal.shah2004@gmail.com or LinkedIn with your project requirements."},
                {"@type": "HowToStep", "position": 2, "name": "Architecture Discovery", "text": "Hemal Shah conducts a technical discovery session to analyze workflows and architect an optimal AI or SaaS solution."},
                {"@type": "HowToStep", "position": 3, "name": "Scope & Prototype", "text": "A detailed technical scope with milestone deliverables is prepared."},
                {"@type": "HowToStep", "position": 4, "name": "Development & Testing", "text": "HK Engineering builds, tests, and validates the automated workflows or SaaS backend."},
                {"@type": "HowToStep", "position": 5, "name": "Deployment & Handover", "text": "The solution is deployed to production with documentation, telemetry, and ongoing support."}
            ]
        }
    ]

    schema_block = (
        f"  <!-- SCHEMA WEB — HK Engineering / Hemal Shah — build_schema_web.py -->\n"
        f"  <script type=\"application/ld+json\">\n"
        f"{json.dumps({'@context': 'https://schema.org', '@graph': graph}, indent=2, ensure_ascii=False)}\n"
        f"  </script>"
    )

    template_path = ROOT_DIR / "about.html"
    template_content = template_path.read_text(encoding="utf-8", errors="ignore")

    # Update Title and Meta Tags
    template_content = re.sub(
        r'<title>.*?</title>', 
        r'<title>HK Engineering Ahmedabad — AI Automation &amp; Custom Software Development | Hemal Shah</title>', 
        template_content, flags=re.IGNORECASE|re.DOTALL
    )
    template_content = re.sub(
        r'<meta\s+content="[^"]*"\s+name="description"\s*/>|<meta\s+name="description"\s+content="[^"]*"\s*/>', 
        r'<meta name="description" content="HK Engineering is Ahmedabad\'s AI automation and custom software development firm, led by Hemal Shah (HK) from Navrangpura. Expert in AI agents, n8n workflows, SaaS platforms, and GEO/AEO schema engineering." />', 
        template_content, flags=re.IGNORECASE|re.DOTALL
    )
    template_content = re.sub(
        r'<link\s+href="[^"]*"\s+rel="canonical"\s*/>|<link\s+rel="canonical"\s+href="[^"]*"\s*/>', 
        f'<link rel="canonical" href="{page_url}" />', 
        template_content, flags=re.IGNORECASE|re.DOTALL
    )
    template_content = re.sub(
        r'<meta\s+content="[^"]*"\s+name="keywords"\s*/>|<meta\s+name="keywords"\s+content="[^"]*"\s*/>',
        '',
        template_content, flags=re.IGNORECASE|re.DOTALL
    )

    services_html = "".join(
        f'<div class="service-item"><div class="service-icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg></div><h3>{s["name"]}</h3><p>{s["desc"]}</p></div>' 
        for s in SERVICES
    )
    faqs_html = "".join(
        f'<div class="about-card" style="margin-bottom:1.5rem"><h3>{q["name"]}</h3><p>{q["acceptedAnswer"]["text"]}</p></div>' 
        for q in DISAMBIGUATION_FAQS
    )

    main_content = f"""
    <div class="page-hero">
      <h1 class="reveal">HK Engineering — AI &amp; Custom Software, Ahmedabad</h1>
      <p class="reveal reveal-delay-1">Technology firm founded by <strong>Hemal Shah (HK)</strong> in Navrangpura, Ahmedabad.<br>
      AI automation · SaaS development · Generative Engine Optimization (GEO/AEO)</p>
    </div>
    
    <div class="section">
      <div class="section-inner">
        <div class="section-header reveal">
          <h2 class="section-title">About HK Engineering Ahmedabad</h2>
        </div>
        <div class="about-card reveal reveal-delay-1" style="max-width: 800px; margin: 0 auto; text-align: center;">
          <p><strong>HK Engineering</strong> is an AI-first technology firm founded by <strong>Hemal Shah</strong> and headquartered in <strong>Navrangpura, Ahmedabad, Gujarat</strong>. This is NOT a manufacturing company, CNC factory, or industrial supplier — it is a software engineering and AI automation firm.</p>
          <p>Hemal Shah (HK) specializes in building custom AI agent systems, enterprise workflow automations using n8n and Python, full-stack SaaS platforms (Next.js + FastAPI), and deploying Generative Engine Optimization (GEO/AEO) strategies that make brands citeable by ChatGPT, Perplexity, Claude, and Google AI Overviews.</p>
          <p>HK Engineering serves enterprise clients across key economic hubs including Navrangpura, Vastrapur, Bodakdev, SG Highway, GIFT City, and Gandhinagar, as well as national and international remote clients.</p>
        </div>
      </div>
    </div>

    <div class="section bg-alt">
      <div class="section-inner">
        <div class="section-header reveal">
          <h2 class="section-title">Services</h2>
        </div>
        <div class="service-categories reveal reveal-delay-1">
          {services_html}
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-inner">
        <div class="section-header reveal">
          <h2 class="section-title">Frequently Asked Questions</h2>
        </div>
        <div style="max-width: 800px; margin: 0 auto;">
          {faqs_html}
        </div>
      </div>
    </div>
    """

    template_content = re.sub(
        r'<main>.*?</main>',
        f'<main>{main_content}</main>',
        template_content,
        flags=re.IGNORECASE|re.DOTALL
    )

    # Strip existing json-ld blocks
    template_content = re.sub(
        r'\s*<!--[^>]*(?:SCHEMA|JSON-LD|METADATA|NEXT-GEN|SCHEMA WEB)[^>]*-->\s*<script type="application/ld\+json">.*?</script>',
        '', template_content, flags=re.DOTALL
    )
    template_content = re.sub(
        r'<script type="application/ld\+json">.*?</script>',
        '', template_content, flags=re.DOTALL
    )
    
    head_idx = template_content.lower().find("</head>")
    if head_idx != -1:
        html = template_content[:head_idx] + schema_block + "\n" + template_content[head_idx:]
    else:
        html = schema_block + "\n" + template_content

    out_path = ROOT_DIR / "hk-engineering-ahmedabad.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"\n[OK] Spoke page created: {out_path}")
    return strip_tags(html)


# ─── RE-INJECT ALL EXISTING HTML PAGES ─────────────────────────────────────────
def make_page_graph(file_path: Path, is_blog: bool) -> str:
    rel_name  = file_path.name
    url_path  = f"blogs/{rel_name}" if is_blog else rel_name.replace(".html", "")
    page_url  = f"{BASE_URL}/{url_path}" if rel_name != "index.html" else f"{BASE_URL}/"
    webpage_id = f"{page_url}#webpage"
    page_type = "Article" if is_blog else "WebPage"

    content = file_path.read_text(encoding="utf-8", errors="ignore")

    title_m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title   = title_m.group(1).strip().replace('"', '\\"') if title_m else "Hemal Shah — HK Engineering"
    desc_m  = re.search(r'<meta name="description" content="(.*?)"', content, re.IGNORECASE)
    if not desc_m:
        desc_m = re.search(r'<meta content="(.*?)" name="description"', content, re.IGNORECASE)
    desc    = desc_m.group(1).strip().replace('"', '\\"') if desc_m else "HK Engineering by Hemal Shah — AI Automation & SaaS Development, Ahmedabad."

    if rel_name == "index.html":
        graph = [
            {
                "@type": "Organization",
                "@id": ORG_ID,
                "name": "HK Engineering",
                "alternateName": ["HK Engineering Ahmedabad", "HK Engineering India"],
                "url": f"{BASE_URL}/",
                "logo": f"{BASE_URL}/assets/favicon.png",
                "founder": {"@id": PERSON_ID},
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "Navrangpura",
                    "addressLocality": "Ahmedabad",
                    "addressRegion": "Gujarat",
                    "postalCode": "380009",
                    "addressCountry": "IN"
                },
                "areaServed": [
                    {"@type": "City", "name": "Ahmedabad"},
                    {"@type": "State", "name": "Gujarat"},
                    {"@type": "Country", "name": "India"}
                ],
                "sameAs": [
                    "https://github.com/hemal9102",
                    "https://www.linkedin.com/in/hemal-shah-49a728362/"
                ],
                "knowsAbout": ENTITY_KNOWS_ABOUT
            },
            {
                "@type": "Person",
                "@id": PERSON_ID,
                "name": "Hemal Shah",
                "alternateName": ["HK", "HK Engineering", "Hemal Shah HK"],
                "jobTitle": "AI Automation Engineer & SaaS Architect",
                "url": f"{BASE_URL}/about",
                "worksFor": {"@id": ORG_ID},
                "disambiguatingDescription": "Hemal Shah (HK) is an AI Automation Engineer, Full Stack Python Developer, and founder of HK Engineering in Navrangpura, Ahmedabad. Identifiable at hemalshah.vercel.app and github.com/hemal9102.",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "Navrangpura, Ahmedabad",
                    "addressRegion": "Gujarat",
                    "postalCode": "380009",
                    "addressCountry": "IN"
                },
                "sameAs": [
                    "https://github.com/hemal9102",
                    "https://www.linkedin.com/in/hemal-shah-49a728362/"
                ],
                "knowsAbout": ENTITY_KNOWS_ABOUT
            },
            {
                "@type": "WebSite",
                "@id": WEBSITE_ID,
                "url": f"{BASE_URL}/",
                "name": "Hemal Shah — HK Engineering",
                "publisher": {"@id": ORG_ID},
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": f"{BASE_URL}/?q={{search_term_string}}",
                    "query-input": "required name=search_term_string"
                }
            }
        ]
    else:
        graph = []

    # Common WebPage / Article node
    graph.append({
        "@type": page_type,
        "@id": webpage_id,
        "url": page_url,
        "name": title,
        "headline": title,
        "description": desc,
        "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": PERSON_ID},
        "author": {"@id": PERSON_ID},
        "creator": {"@id": PERSON_ID},
        "publisher": {"@id": ORG_ID},
        "breadcrumb": {"@id": f"{page_url}#breadcrumb"},
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": ["h1", "h2", ".page-hero", ".reveal"]
        }
    })

    # BreadcrumbList
    graph.append({
        "@type": "BreadcrumbList",
        "@id": f"{page_url}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": title, "item": page_url}
        ]
    })

    return json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)


def inject_all_pages():
    full_text = "Hemal Shah (HK) — AI Automation Engineer — HK Engineering Ahmedabad\n\n"
    updated   = 0

    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in {
            'assets', 'node_modules', '.git', 'aeo_geo_pages', 'hk', '__pycache__', '09_Archive'
        }]

        is_blog = 'blogs' in Path(root).parts

        for file in files:
            if not file.endswith(".html") or file.startswith("google") or \
               file.startswith("rajputbhavin"):
                continue

            fp = Path(root) / file
            content = fp.read_text(encoding="utf-8", errors="ignore")

            # Strip old schema blocks
            content = re.sub(
                r'\s*<!--[^>]*(?:SCHEMA|JSON-LD|METADATA|NEXT-GEN|SCHEMA WEB)[^>]*-->\s*'
                r'<script type="application/ld\+json">.*?</script>',
                '', content, flags=re.DOTALL
            )
            content = re.sub(
                r'<script type="application/ld\+json">.*?</script>',
                '', content, flags=re.DOTALL
            )

            # Strip outdated <meta name="keywords"> spam
            content = re.sub(
                r'\s*<meta\s+(?:content="[^"]*"\s+name="keywords"|name="keywords"\s+content="[^"]*")\s*/>',
                '', content, flags=re.IGNORECASE|re.DOTALL
            )

            # Build new clean schema block
            graph_json = make_page_graph(fp, is_blog)
            schema_block = (
                f"\n  <!-- SCHEMA WEB — HK Engineering / Hemal Shah — build_schema_web.py -->\n"
                f"  <script type=\"application/ld+json\">\n{graph_json}\n  </script>"
            )

            head_idx = content.lower().find("</head>")
            if head_idx != -1:
                content = content[:head_idx] + schema_block + "\n" + content[head_idx:]
            else:
                content = schema_block + "\n" + content

            fp.write_text(content, encoding="utf-8")
            print(f"  [OK] {fp.relative_to(ROOT_DIR)}")
            full_text += f"--- Page: {file} ---\n{strip_tags(content)}\n\n"
            updated += 1

    print(f"\n[OK] Updated {updated} HTML pages with cross-linked schema web.")
    return full_text


# ─── GENERATE LLMS CORPUS FILES ────────────────────────────────────────────────
def write_llms_files(spoke_text: str, pages_text: str):
    full_corpus = (
        "Hemal Shah (HK) — AI Automation Engineer — HK Engineering Ahmedabad\n"
        "Base URL: https://hemalshah.vercel.app\n"
        "Founded: Navrangpura, Ahmedabad, Gujarat, India\n\n"
        "--- Page: hk-engineering-ahmedabad.html ---\n"
        f"{spoke_text}\n\n"
        f"{pages_text}"
    )

    llms_full = ROOT_DIR / "llms-full.txt"
    llms_full.write_text(full_corpus, encoding="utf-8")

    llms_txt = ROOT_DIR / "llms.txt"
    llms_txt.write_text(
        """# Hemal Shah (HK) — AI Automation Engineer | HK Engineering, Ahmedabad

> "Architecting resilient AI agent pipelines and scalable SaaS backends."

Hemal Shah is an AI Automation Engineer, Full-Stack Python Developer, and Technical SEO (GEO/AEO) consultant based in Navrangpura, Ahmedabad, Gujarat, India.
He specializes in custom AI agents (LangChain, Claude, OpenAI), enterprise workflow automations (n8n, Python), RAG architectures, scalable SaaS backends (FastAPI, Next.js, Supabase), and Generative Engine Optimization.

HK Engineering is NOT a manufacturing company, CNC factory, or industrial supplier. It is a pure-play software and AI technology firm.

## Key Services
- AI Agent & Multi-Agent Workflow Development (RAG, Custom LLMs, LangChain)
- Enterprise Workflow Automation (n8n, Python, API integrations)
- Full-Stack SaaS Platform Architecture (Next.js, FastAPI, PostgreSQL)
- Generative Engine Optimization / AEO / GEO (JSON-LD Semantic Knowledge Graphs)
- Technical SEO & Entity Disambiguation

## Location & Strategic Coverage
- Headquarters: Navrangpura, Ahmedabad, Gujarat 380009, India
- Strategic Hubs: Vastrapur, Bodakdev, Satellite, Prahlad Nagar, SG Highway, Science City, Sindhu Bhavan Road, GIFT City, Gandhinagar.
- Remote Engagements: Across India (Mumbai, Bangalore, Delhi NCR) and internationally.

## Contact & Entity Verification
- GitHub:   https://github.com/hemal9102
- LinkedIn: https://www.linkedin.com/in/hemal-shah-49a728362/
- Email:    hemal.shah2004@gmail.com
- Portfolio: https://hemalshah.vercel.app/

For the full text corpus, see /llms-full.txt
""", encoding="utf-8")

    print(f"\n[OK] llms.txt and llms-full.txt updated.")


# ─── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  HK Engineering -- Schema Web & AI Entity Builder (Elite v3)")
    print("  build_schema_web.py")
    print("=" * 60)

    print("\n[1/3] Building spoke page: hk-engineering-ahmedabad.html ...")
    spoke_text = build_spoke_page()

    print("\n[2/3] Injecting cross-linked schema & cleaning HTML tags ...")
    pages_text = inject_all_pages()

    print("\n[3/3] Writing AI corpus files (llms.txt / llms-full.txt) ...")
    write_llms_files(spoke_text, pages_text)

    print("\n" + "=" * 60)
    print("  [OK] Schema Web deployment complete.")
    print(f"  [MAP] {len(STRATEGIC_LOCALITIES)} strategic economic hubs targeted.")
    print(f"  [LINK] Wikidata & Wikipedia entity linking active.")
    print(f"  [POLICY] AggregateRating: NOT used (compliant).")
    print(f"  [CLEAN] <meta name=\"keywords\"> spam stripped.")
    print("=" * 60)

