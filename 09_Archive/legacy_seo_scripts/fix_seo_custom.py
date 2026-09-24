import os
import json
import glob
from bs4 import BeautifulSoup

# 1. Update vercel.json
with open('vercel.json', 'r') as f:
    config = json.load(f)

config['redirects'] = [
    { "source": "/hk/blogs/blog1(?:\\.html)?", "destination": "/blogs", "permanent": True },
    { "source": "/hk/blogs(?:\\.html)?", "destination": "/blogs", "permanent": True },
    { "source": "/hk/backup(?:\\.html)?", "destination": "/", "permanent": True },
    { "source": "/hk/index(?:\\.html)?", "destination": "/", "permanent": True },
    { "source": "/hk/(.*)", "destination": "/$1", "permanent": True },
    { "source": "/blogs/blog2(?:\\.html)?", "destination": "/blogs", "permanent": True },
    { "source": "/blogs/blog3(?:\\.html)?", "destination": "/blogs", "permanent": True },
    { "source": "/blogs/blog4(?:\\.html)?", "destination": "/blogs", "permanent": True },
    { "source": "/blogs/blog5(?:\\.html)?", "destination": "/blogs", "permanent": True },
    { "source": "/blogs/blog6(?:\\.html)?", "destination": "/blogs", "permanent": True }
]

with open('vercel.json', 'w') as f:
    json.dump(config, f, indent=2)

# 2. Fix Canonicals in HTML
html_files = glob.glob('**/*.html', recursive=True)
base_url = 'https://hemalshah.vercel.app'

for file in html_files:
    if 'node_modules' in file:
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    head = soup.head
    if not head:
        continue
    
    # Calculate canonical URL
    # Replace backslashes with forward slashes
    clean_path = file.replace('\\', '/')
    
    if clean_path == 'index.html':
        canonical_url = base_url + '/'
    else:
        # Remove .html extension
        if clean_path.endswith('.html'):
            clean_path = clean_path[:-5]
        canonical_url = base_url + '/' + clean_path
    
    canonical_tag = soup.find('link', {'rel': 'canonical'})
    if canonical_tag:
        canonical_tag['href'] = canonical_url
    else:
        new_tag = soup.new_tag('link', rel='canonical', href=canonical_url)
        head.append(new_tag)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"Fixed {file}")
