import os
import re
from datetime import datetime

root_dir = r"H:\portfolio_website\hemalshah"
current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
publish_date = "2024-01-01T08:00:00+00:00"

def strip_tags(text):
    text = re.sub(r'<style.*?>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^<]+?>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def inject_metadata(content, file_name, is_blog=False):
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "Hemal Shah"
    title_clean = title.replace('"', '\\"')
    
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content, re.IGNORECASE)
    desc = desc_match.group(1).strip() if desc_match else "Hemal Shah (HK) is an AI Automation Engineer."
    desc_clean = desc.replace('"', '\\"')
    
    url_path = f"blogs/{file_name}" if is_blog else file_name
    # Handle index.html edge case for canonicals
    if file_name == "index.html" and not is_blog:
        url_path = ""
    page_url = f"https://hemalshah.vercel.app/{url_path}"
    
    # 1. Clean up old schemas and canonicals
    content = re.sub(r'<script type="application/ld\+json">.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<link rel="canonical" href=".*?"\s*/?>', '', content)
    content = re.sub(r'<meta name="author" content=".*?"\s*/?>', '', content)
    content = re.sub(r'<meta property="article:published_time".*?>', '', content)
    content = re.sub(r'<meta property="article:modified_time".*?>', '', content)

    # 2. Add Meta Tags (Canonical, Author, Dates)
    head_end_idx = content.find("</head>")
    if head_end_idx != -1:
        meta_injection = f"""
  <link rel="canonical" href="{page_url}" />
  <meta name="author" content="Hemal Shah" />
  <meta property="article:published_time" content="{publish_date}" />
  <meta property="article:modified_time" content="{current_date}" />
"""
        content = content[:head_end_idx] + meta_injection + content[head_end_idx:]
    
    # 3. Build the E-E-A-T Enhanced Schema Graph
    person_id = "https://hemalshah.vercel.app/#person"
    org_id = "https://hemalshah.vercel.app/#organization"
    website_id = "https://hemalshah.vercel.app/#website"
    webpage_id = f"{page_url}#webpage"
    
    page_type = 'Article' if is_blog else 'WebPage'
    
    schema = f"""
  <!-- HIGH E-E-A-T & ENTITY METADATA JSON-LD GRAPH -->
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
        "jobTitle": "Lead AI Automation Engineer",
        "description": "Hemal Shah is a highly experienced AI Architect and Python Developer specializing in Workflow Automation, Semantic SEO, and Large Language Models.",
        "worksFor": {{"@id": "{org_id}"}},
        "sameAs": [
          "https://github.com/hemal9102",
          "https://www.linkedin.com/in/hemal-shah-49a728362/"
        ],
        "knowsAbout": [
          "Artificial Intelligence",
          "Python Programming",
          "Search Engine Optimization",
          "Workflow Automation",
          "System Architecture"
        ],
        "award": "Proven Track Record in AI Engineering"
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
        "name": "{title_clean}",
        "headline": "{title_clean}",
        "description": "{desc_clean}",
        "datePublished": "{publish_date}",
        "dateModified": "{current_date}",
        "isPartOf": {{"@id": "{website_id}"}},
        "author": {{"@id": "{person_id}"}},
        "creator": {{"@id": "{person_id}"}},
        "publisher": {{"@id": "{org_id}"}},
        "reviewedBy": {{"@id": "{person_id}"}},
        "about": [
          {{
            "@type": "Thing",
            "name": "Artificial Intelligence",
            "sameAs": "https://en.wikipedia.org/wiki/Artificial_intelligence"
          }},
          {{
            "@type": "Thing",
            "name": "Automation",
            "sameAs": "https://en.wikipedia.org/wiki/Automation"
          }}
        ],
        "significantLink": [
          "https://hemalshah.vercel.app/services.html",
          "https://hemalshah.vercel.app/work.html",
          "https://hemalshah.vercel.app/contact.html"
        ],
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
            "name": "{title_clean}",
            "item": "{page_url}"
          }}
        ]
      }}
    ]
  }}
  </script>
"""
    # Re-find head_end_idx because length changed after first injection
    head_end_idx = content.find("</head>")
    if head_end_idx != -1:
        content = content[:head_end_idx] + schema + content[head_end_idx:]
    
    return content

def process_all(directory):
    for root, dirs, files in os.walk(directory):
        if 'hk' in root.split(os.sep) or 'assets' in root.split(os.sep) or 'node_modules' in root.split(os.sep) or '.git' in root.split(os.sep):
            continue
            
        is_blog = 'blogs' in root.split(os.sep)
        for file in files:
            if file.endswith(".html") and not file.startswith('google'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = inject_metadata(content, file, is_blog)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Injected E-E-A-T and Canonical metadata into {file_path}")

process_all(root_dir)
print("All E-E-A-T and Semantic Metadata successfully injected!")
