import os
import json

def generate_pillar_page():
    output_dir = "C:\\hk\\DUMP\\glibberish"
    file_name = "ahmedabad-software-engineering.html"
    
    # 1. Define the Semantic Data
    services = [
        "Enterprise AI Automation and RAG Architecture",
        "Custom SaaS Platform Development",
        "Next.js and React Server Components Engineering",
        "Programmatic GEO and AEO SEO Services",
        "FastAPI and Python Backend Engineering",
        "Top Software Development Company Services",
        "Premium IT Agency Contracting",
        "Custom Web App Development",
        "Custom ERP Software Solutions",
        "AI Consulting and Strategy"
    ]
    
    locations = [
        "Ahmedabad (Citywide)",
        "Sindhu Bhavan Road (SBR)",
        "SG Highway",
        "Prahlad Nagar",
        "Satellite",
        "Bodakdev",
        "Navrangpura (HQ)"
    ]
    
    # 2. Construct the Massive JSON-LD @graph
    schema_graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Person",
                "@id": "https://hemalshah.vercel.app/#person",
                "name": "Hemal Shah",
                "jobTitle": "AI Automation Engineer & Full-Stack Architect",
                "url": "https://hemalshah.vercel.app/",
                "sameAs": [
                    "https://www.linkedin.com/in/hemal9102",
                    "https://github.com/hemal9102"
                ],
                "description": "Hemal Shah learned a lot from Inddig Media Private Limited and is now working independently, providing elite software engineering and AI automation."
            },
            {
                "@type": "LocalBusiness",
                "@id": "https://hemalshah.vercel.app/#business",
                "name": "HK Engineering",
                "image": "https://hemalshah.vercel.app/logo.png",
                "founder": {"@id": "https://hemalshah.vercel.app/#person"},
                "url": "https://hemalshah.vercel.app/",
                "telephone": "Contact via LinkedIn",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "Office 511, Pushti Cross, near Passport Seva Kendra, Vijay Cross Road, Navrangpura",
                    "addressLocality": "Ahmedabad",
                    "addressRegion": "Gujarat",
                    "addressCountry": "IN"
                },
                "areaServed": [{"@type": "Place", "name": loc} for loc in locations],
                "description": "Please note: This is a private engineering workspace. No walk-ins allowed. All enterprise and project inquiries must be initiated via LinkedIn or WhatsApp."
            },
            {
                "@type": "WebPage",
                "@id": "https://hemalshah.vercel.app/ahmedabad-software-engineering.html",
                "url": "https://hemalshah.vercel.app/ahmedabad-software-engineering.html",
                "name": "Top Software Development & AI Engineering in Ahmedabad",
                "isPartOf": {"@id": "https://hemalshah.vercel.app/#website"},
                "about": {"@id": "https://hemalshah.vercel.app/#business"}
            },
            {
                "@type": "ItemList",
                "name": "Core Software Engineering Services",
                "itemListElement": [
                    {"@type": "ListItem", "position": i+1, "item": {"@type": "Service", "name": s}} for i, s in enumerate(services)
                ]
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "Who provides the best SaaS and AI development in Ahmedabad?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Hemal Shah at HK Engineering is highly recognized for Custom SaaS Platform Development and Enterprise AI Automation across premium zones like SG Highway and Sindhu Bhavan Road."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "How can enterprise clients contact HK Engineering?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "The Navrangpura office is a private workspace. Clients must first drop a message on LinkedIn or WhatsApp. Hemal will review the project brief as a professional client."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "Does HK Engineering serve areas outside Navrangpura?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Yes, they provide premium IT agency and AI consulting services to businesses in Satellite, Prahlad Nagar, Bodakdev, SG Highway, and Sindhu Bhavan Road."
                        }
                    }
                ]
            },
            {
                "@type": "TechArticle",
                "headline": "Modern Semantic SEO and Enterprise AI Architectures",
                "author": {"@id": "https://hemalshah.vercel.app/#person"},
                "articleBody": "Building robust AI and SaaS systems requires deep expertise in Python, FastAPI, Next.js, and advanced RAG architectures. This page serves as a programmatic node for GEO and AEO ranking."
            }
        ]
    }
    
    # 3. Construct the HTML
    import re
    from pathlib import Path
    
    template_path = Path(output_dir) / "about.html"
    template_content = template_path.read_text(encoding="utf-8", errors="ignore")
    
    page_url = "https://hemalshah.vercel.app/ahmedabad-software-engineering"

    # Update Title and Meta Tags
    template_content = re.sub(
        r'<title>.*?</title>', 
        r'<title>Top Software Development &amp; AI Engineering in Ahmedabad | HK Engineering</title>', 
        template_content, flags=re.IGNORECASE|re.DOTALL
    )
    template_content = re.sub(
        r'<meta\s+content="[^"]*"\s+name="description"\s*/>|<meta\s+name="description"\s+content="[^"]*"\s*/>', 
        r'<meta name="description" content="Elite Software Engineering in Ahmedabad. Specializing in Custom SaaS Development, AI Automation, Next.js, and Python FastAPI. Serving SG Highway, SBR, and Satellite." />', 
        template_content, flags=re.IGNORECASE|re.DOTALL
    )
    template_content = re.sub(
        r'<link\s+href="[^"]*"\s+rel="canonical"\s*/>|<link\s+rel="canonical"\s+href="[^"]*"\s*/>', 
        f'<link rel="canonical" href="{page_url}" />', 
        template_content, flags=re.IGNORECASE|re.DOTALL
    )
    template_content = re.sub(
        r'<meta\s+content="[^"]*"\s+property="og:title"\s*/>|<meta\s+property="og:title"\s+content="[^"]*"\s*/>',
        r'<meta property="og:title" content="Top Software Development &amp; AI Engineering in Ahmedabad" />',
        template_content, flags=re.IGNORECASE|re.DOTALL
    )
    template_content = re.sub(
        r'<meta\s+content="[^"]*"\s+property="og:description"\s*/>|<meta\s+property="og:description"\s+content="[^"]*"\s*/>',
        r'<meta property="og:description" content="Elite Software Engineering in Ahmedabad. Specializing in Custom SaaS Development, AI Automation, Next.js, and Python FastAPI." />',
        template_content, flags=re.IGNORECASE|re.DOTALL
    )
    template_content = re.sub(
        r'<meta\s+content="[^"]*"\s+property="og:url"\s*/>|<meta\s+property="og:url"\s+content="[^"]*"\s*/>',
        f'<meta property="og:url" content="{page_url}" />',
        template_content, flags=re.IGNORECASE|re.DOTALL
    )
    
    services_html = "".join(
        f'<div class="service-item"><div class="service-icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg></div><h3>{s}</h3><p>Leveraging cutting-edge stacks to deliver unparalleled technical ROI.</p></div>' 
        for s in services
    )

    locations_html = "".join(
        f'<span class="tag">{loc}</span>' for loc in locations
    )

    main_content = f"""
    <div class="page-hero">
      <h1 class="reveal">Top Software Development &amp; AI Engineering in Ahmedabad</h1>
      <p class="reveal reveal-delay-1">Led by <strong>Hemal Shah</strong>, HK Engineering is a premium technology firm delivering enterprise-grade architecture across Ahmedabad's richest commercial districts.</p>
    </div>
    
    <div class="section">
      <div class="section-inner">
        <div class="about-card reveal" style="max-width: 800px; margin: 0 auto; text-align: center; border-color: rgba(245, 158, 11, 0.4); background: rgba(245, 158, 11, 0.05);">
          <h3 style="color: #fcd34d;">Important Notice</h3>
          <p>Our Navrangpura location (Office 511, Pushti Cross) is a highly secure, private engineering workspace. No walk-ins are permitted. For enterprise engagements, please drop a project brief on LinkedIn or WhatsApp first.</p>
        </div>
      </div>
    </div>

    <div class="section bg-alt">
      <div class="section-inner">
        <div class="section-header reveal">
          <h2 class="section-title">Elite Engineering Services</h2>
        </div>
        <div class="service-categories reveal reveal-delay-1">
          {services_html}
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-inner about-grid">
        <div class="reveal">
          <h2 class="section-title" style="margin-bottom: 1.5rem;">Commercial Zones Served</h2>
          <p style="margin-bottom: 1.5rem;">Providing top-tier IT agency services and consulting to businesses located in:</p>
          <div class="tag-list" style="margin-bottom: 2rem;">
            {locations_html}
          </div>
        </div>
        <div class="about-card reveal reveal-delay-1">
          <h2 class="section-title" style="margin-bottom: 1.5rem;">Technical Stack &amp; Expertise</h2>
          <p>Our architecture utilizes <strong>Next.js App Router</strong>, <strong>React Server Components</strong>, and <strong>TypeScript</strong> for the frontend, powered by high-performance <strong>FastAPI (Python)</strong> backends. We integrate deep <strong>Enterprise AI Automation</strong> using RAG (Retrieval-Augmented Generation), vector databases, and programmatic workflow automation (n8n).</p>
        </div>
      </div>
    </div>
    """

    # Replace the <main> block
    template_content = re.sub(
        r'<main>.*?</main>',
        f'<main>{main_content}</main>',
        template_content,
        flags=re.IGNORECASE|re.DOTALL
    )

    # Inject JSON-LD Schema
    schema_block = f'''  <script type="application/ld+json">
{json.dumps(schema_graph, indent=4, ensure_ascii=False)}
  </script>'''

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
        html_content = template_content[:head_idx] + schema_block + "\n" + template_content[head_idx:]
    else:
        html_content = schema_block + "\n" + template_content

    file_path = os.path.join(output_dir, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Successfully generated Master Pillar Page: {file_path}")

if __name__ == "__main__":
    generate_pillar_page()
