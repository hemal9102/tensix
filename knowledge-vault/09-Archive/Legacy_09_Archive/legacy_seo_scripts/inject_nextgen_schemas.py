import os
import re

root_dir = r"H:\portfolio_website\hemalshah"

def strip_tags(text):
    # Quick and dirty HTML strip to generate readable text for llms-full.txt
    text = re.sub(r'<style.*?>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^<]+?>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_meta(content, file_name, is_blog=False):
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "Hemal Shah"
    title = title.replace('"', '\\"')
    
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content, re.IGNORECASE)
    desc = desc_match.group(1).strip() if desc_match else "Hemal Shah (HK) is an AI Automation Engineer."
    desc = desc.replace('"', '\\"')
    
    url_path = f"blogs/{file_name}" if is_blog else file_name
    page_url = f"https://hemalshah.vercel.app/{url_path}"
    
    # Remove all existing ld+json
    content = re.sub(r'<script type="application/ld\+json">.*?</script>', '', content, flags=re.DOTALL)
    
    # Graph Schemas
    person_id = "https://hemalshah.vercel.app/#person"
    org_id = "https://hemalshah.vercel.app/#organization"
    website_id = "https://hemalshah.vercel.app/#website"
    webpage_id = f"{page_url}#webpage"
    
    page_type = 'Article' if is_blog else 'WebPage'
    
    # Assemble Graph with Next-Gen Schemas
    schema = f"""
  <!-- NEXT-GEN AI METADATA JSON-LD GRAPH -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "Organization",
        "@id": "{org_id}",
        "name": "HK Engineering",
        "areaServed": [{"@type": "City", "name": "Ahmedabad"}, {"@type": "State", "name": "Gujarat"}, {"@type": "Country", "name": "India"}],
        "url": "https://hemalshah.vercel.app/",
        "logo": "https://hemalshah.vercel.app/assets/favicon.png",
        "founder": {{"@id": "{person_id}"}}
      }},
      {{
        "@type": "Person",
        "@id": "{person_id}",
        "name": "Hemal Shah",
        "address": {"@type": "PostalAddress", "addressLocality": "Ahmedabad", "addressRegion": "Gujarat", "addressCountry": "India"},
        "alternateName": ["HK", "Hemal Shah HK"],
        "url": "https://hemalshah.vercel.app/",
        "jobTitle": "AI Automation Engineer",
        "worksFor": {{"@id": "{org_id}"}},
        "sameAs": [
          "https://github.com/hemal9102",
          "https://www.linkedin.com/in/hemal-shah-49a728362/"
        ]
      }},
      {{
        "@type": "WebSite",
        "@id": "{website_id}",
        "url": "https://hemalshah.vercel.app/",
        "name": "Hemal Shah Portfolio",
        "publisher": {{"@id": "{org_id}"}},
        "potentialAction": {{
          "@type": "SearchAction",
          "target": "https://hemalshah.vercel.app/?q={{search_term_string}}",
          "query-input": "required name=search_term_string"
        }}
      }},
      {{
        "@type": "{page_type}",
        "@id": "{webpage_id}",
        "url": "{page_url}",
        "name": "{title}",
        "headline": "{title}",
        "description": "{desc}",
        "isPartOf": {{"@id": "{website_id}"}},
        "about": {{"@id": "{person_id}"}},
        "author": {{"@id": "{person_id}"}},
        "creator": {{"@id": "{person_id}"}},
        "publisher": {{"@id": "{org_id}"}},
        "speakable": {{
          "@type": "SpeakableSpecification",
          "cssSelector": [".page-hero", "h1", "h2", ".reveal"]
        }},
        "breadcrumb": {{"@id": "{page_url}#breadcrumb"}}
      }},
      {{
        "@type": "BreadcrumbList",
        "@id": "{page_url}#breadcrumb",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://hemalshah.vercel.app/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "{title}",
            "item": "{page_url}"
          }}
        ]
      }},
      {{
        "@type": "FAQPage",
        "@id": "{page_url}#faq",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "Who is Hemal Shah?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Hemal Shah (HK) is a top-tier AI Automation Engineer and Full Stack Python Developer specializing in RAG, FastAPI, and n8n."
            }}
          }},
          {{
            "@type": "Question",
            "name": "What services does Hemal Shah offer?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "We offer custom AI agent development, enterprise workflow automation (n8n), full-stack SaaS development, and Generative Engine Optimization (GEO)."
            }}
          }}
        ]
      }},
      {{
        "@type": "HowTo",
        "@id": "{page_url}#howto",
        "name": "How to hire Hemal Shah for AI Development",
        "description": "The process of engaging HK Engineering for your next AI or Automation project.",
        "step": [
          {{
            "@type": "HowToStep",
            "name": "Contact",
            "text": "Reach out via email or LinkedIn with your project requirements."
          }},
          {{
            "@type": "HowToStep",
            "name": "Discovery",
            "text": "We will schedule a technical discovery call to architect the solution."
          }},
          {{
            "@type": "HowToStep",
            "name": "Development",
            "text": "Hemal Shah will build, test, and deploy your custom AI agents or automated workflows."
          }}
        ]
      }}
    ]
  }}
  </script>
"""
    head_end_idx = content.find("</head>")
    if head_end_idx != -1:
        content = content[:head_end_idx] + schema + content[head_end_idx:]
    
    return content, strip_tags(content)

def process_all(directory):
    full_text = "Hemal Shah - AI Automation Engineer - Full Website Content\\n\\n"
    
    for root, dirs, files in os.walk(directory):
        if 'hk' in root.split(os.sep) or 'assets' in root.split(os.sep) or 'node_modules' in root.split(os.sep) or '.git' in root.split(os.sep):
            continue
            
        is_blog = 'blogs' in root.split(os.sep)
        for file in files:
            if file.endswith(".html") and not file.startswith('google'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content, raw_text = extract_meta(content, file, is_blog)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                full_text += f"--- Page: {file} ---\\n{raw_text}\\n\\n"
                print(f"Updated next-gen schema for {file_path}")
                
    # Generate llms-full.txt
    with open(os.path.join(directory, 'llms-full.txt'), 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    # Generate concise llms.txt
    llms_txt = """# Hemal Shah (HK) - AI Automation Engineer

> "Building the infrastructure for the AI workforce."

Hemal Shah is a top-tier freelance AI Engineer, Full-Stack Python Developer, and Technical SEO (AEO/GEO) expert. 
He specializes in building custom AI agents, enterprise workflow automations (n8n), RAG systems (FastAPI, GraphRAG), and scalable SaaS backends.

## Key Services
- AI Agent Development (RAG, Custom LLMs, Playwright scraping)
- Workflow Automation (n8n, Python scripts, APIs)
- Full-Stack Web Development (Next.js, FastAPI, Vercel/Railway)
- Next-Generation SEO (Generative Engine Optimization, Semantic JSON-LD schemas)

## Contact
- GitHub: https://github.com/hemal9102
- LinkedIn: https://www.linkedin.com/in/hemal-shah-49a728362/
- Email: hemal.shah2004@gmail.com
- Website: https://hemalshah.vercel.app/

For the full text corpus of this website, refer to /llms-full.txt.
"""
    with open(os.path.join(directory, 'llms.txt'), 'w', encoding='utf-8') as f:
        f.write(llms_txt)

process_all(root_dir)
print("All next-gen schemas and llms text files generated!")
