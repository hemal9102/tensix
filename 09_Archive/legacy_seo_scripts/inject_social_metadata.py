import os
import re
from datetime import datetime

root_dir = r"H:\portfolio_website\hemalshah"
current_date = datetime.now().strftime("%Y-%m-%d")

def inject_social(content, file_name, is_blog=False):
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "Hemal Shah"
    title_clean = title.replace('"', '&quot;')
    
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content, re.IGNORECASE)
    desc = desc_match.group(1).strip() if desc_match else "Hemal Shah (HK) is an AI Automation Engineer."
    desc_clean = desc.replace('"', '&quot;')
    
    url_path = f"blogs/{file_name}" if is_blog else file_name
    if file_name == "index.html" and not is_blog:
        url_path = ""
    page_url = f"https://hemalshah.vercel.app/{url_path}"
    
    og_type = 'article' if is_blog else 'website'
    image_url = "https://hemalshah.vercel.app/assets/favicon.png"
    
    # Clean old OG and Twitter tags to prevent duplicates
    content = re.sub(r'<meta property="og:.*?".*?>\n?', '', content)
    content = re.sub(r'<meta name="twitter:.*?".*?>\n?', '', content)
    content = re.sub(r'<link rel="alternate" hreflang=".*? href=".*?".*?>\n?', '', content)
    
    head_end_idx = content.find("</head>")
    if head_end_idx != -1:
        social_injection = f"""
  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="{og_type}" />
  <meta property="og:title" content="{title_clean}" />
  <meta property="og:description" content="{desc_clean}" />
  <meta property="og:url" content="{page_url}" />
  <meta property="og:image" content="{image_url}" />

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title_clean}" />
  <meta name="twitter:description" content="{desc_clean}" />
  <meta name="twitter:image" content="{image_url}" />

  <!-- Hreflang -->
  <link rel="alternate" hreflang="en" href="{page_url}" />
  <link rel="alternate" hreflang="x-default" href="{page_url}" />
"""
        content = content[:head_end_idx] + social_injection + content[head_end_idx:]
    
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
                
                new_content = inject_social(content, file, is_blog)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Injected Social Metadata into {file_path}")

process_all(root_dir)

# Update sitemap.xml
sitemap_path = os.path.join(root_dir, 'sitemap-new.xml')
if os.path.exists(sitemap_path):
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        sitemap_content = f.read()
    
    # Update lastmod to today
    sitemap_content = re.sub(r'<lastmod>.*?</lastmod>', f'<lastmod>{current_date}</lastmod>', sitemap_content)
    
    with open(os.path.join(root_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print("Generated and updated sitemap.xml")
