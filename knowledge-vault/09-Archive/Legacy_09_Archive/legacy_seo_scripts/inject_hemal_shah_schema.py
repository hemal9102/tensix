import os
import re

root_dir = r"H:\portfolio_website\hemalshah"
blog_dir = r"H:\portfolio_website\hemalshah\blogs"

# Define the master person schema that will be used everywhere
person_schema = """    {
      "@type": "Person",
      "@id": "https://hemalshah.vercel.app/#person",
      "name": "Hemal Shah",
      "alternateName": ["HK", "Hemal Shah HK", "HK Engineering"],
      "url": "https://hemalshah.vercel.app/",
      "jobTitle": "AI Automation Engineer & Python Developer",
      "description": "Hemal Shah (HK) is an AI Automation Engineer, Full Stack Developer, and Technical SEO specialist.",
      "sameAs": [
        "https://github.com/hemal9102",
        "https://www.linkedin.com/in/hemal-shah-49a728362/",
        "https://www.instagram.com/hemall_9/"
      ]
    }"""

def extract_meta(content, file_name, is_blog=False):
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "Hemal Shah"
    
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content, re.IGNORECASE)
    desc = desc_match.group(1).strip() if desc_match else ""
    
    # Remove all existing ld+json scripts to avoid duplicates
    content = re.sub(r'<script type="application/ld\+json">.*?</script>', '', content, flags=re.DOTALL)
    
    # Build new schema
    url_path = f"blogs/{file_name}" if is_blog else file_name
    
    page_type = "TechArticle" if is_blog else "WebPage"
    id_type = "article" if is_blog else "webpage"
    
    # For work.html, compare.html etc, maybe use ItemPage or CollectionPage, but WebPage is universally good.
    if file_name in ["work.html", "wr1.html", "gallery.html"]:
        page_type = "CollectionPage"
    elif file_name == "about.html":
        page_type = "AboutPage"
    elif file_name == "contact.html":
        page_type = "ContactPage"
    
    schema = f"""
  <!-- JSON-LD Entity Graph for Hemal Shah Topical Authority -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
{person_schema},
      {{
        "@type": "{page_type}",
        "@id": "https://hemalshah.vercel.app/{url_path}#{id_type}",
        "url": "https://hemalshah.vercel.app/{url_path}",
        "name": "{title}",
        "headline": "{title}",
        "description": "{desc}",
        "author": {{"@id": "https://hemalshah.vercel.app/#person"}},
        "creator": {{"@id": "https://hemalshah.vercel.app/#person"}},
        "publisher": {{"@id": "https://hemalshah.vercel.app/#person"}},
        "mainEntityOfPage": {{"@id": "https://hemalshah.vercel.app/{url_path}#{id_type}"}}
      }}
    ]
  }}
  </script>
"""
    head_end_idx = content.find("</head>")
    if head_end_idx != -1:
        content = content[:head_end_idx] + schema + content[head_end_idx:]
    
    return content

def process_directory(directory, is_blog):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html") and not file.startswith('google'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = extract_meta(content, file, is_blog)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated schema for {file_path}")

# Process root pages
print("Processing root pages...")
process_directory(root_dir, is_blog=False)

# Process blogs
# Actually, the walk will process blogs twice if I run it on root_dir, because blogs is a subdirectory of root_dir.
# Let's fix that. I will just walk root_dir and check if 'blogs' is in the path.

def process_all(directory):
    for root, dirs, files in os.walk(directory):
        # skip hk subfolder as it looks like a backup or separate project
        if 'hk' in root.split(os.sep):
            continue
            
        is_blog = 'blogs' in root.split(os.sep)
        for file in files:
            if file.endswith(".html") and not file.startswith('google'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = extract_meta(content, file, is_blog)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated schema for {file_path}")

process_all(root_dir)
print("All schemas injected!")
