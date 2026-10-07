import os
import re
import urllib.request

root_dir = r"H:\portfolio_website\hemalshah"
icons_dir = os.path.join(root_dir, "assets", "icons")
os.makedirs(icons_dir, exist_ok=True)

all_external_urls = set()

for dirpath, dirnames, filenames in os.walk(root_dir):
    if 'node_modules' in dirnames:
        dirnames.remove('node_modules')
    if '.git' in dirnames:
        dirnames.remove('.git')
        
    for file in filenames:
        if file.endswith('.html'):
            filepath = os.path.join(dirpath, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            urls = re.findall(r'src="(https://(?:www\.vectorlogo\.zone|n8n\.io)[^"]+)"', content)
            for u in urls:
                all_external_urls.add(u)

url_to_local_filename = {}
for url in all_external_urls:
    if "n8n.io" in url:
        filename = "n8n-icon.png"
    else:
        filename = url.split('/')[-1]
        
    local_path = os.path.join(icons_dir, filename)
    url_to_local_filename[url] = filename
    
    if not os.path.exists(local_path):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                with open(local_path, 'wb') as f:
                    f.write(response.read())
            print(f"Downloaded {filename}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

for dirpath, dirnames, filenames in os.walk(root_dir):
    if 'node_modules' in dirnames:
        dirnames.remove('node_modules')
    if '.git' in dirnames:
        dirnames.remove('.git')
        
    for file in filenames:
        if file.endswith('.html'):
            filepath = os.path.join(dirpath, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            original_content = content
            
            # Remove n8n and vectorlogo preconnects
            content = re.sub(r'\s*<!-- Preconnect to external image CDNs for LCP optimization -->\s*', '', content)
            content = re.sub(r'\s*<link\s+rel="preconnect"\s+href="https://(?:www\.vectorlogo\.zone|n8n\.io)"\s*/?>', '', content)
            
            # Make sure we don't accidentally have multiple fonts.googleapis.com preconnects
            # Actually, I'll let it be and just strip exactly what the regex matches.
            
            # Replace URLs with local equivalents
            for url, filename in url_to_local_filename.items():
                depth = os.path.relpath(dirpath, root_dir).count(os.sep) if dirpath != root_dir else 0
                prefix = '../' * depth if depth > 0 else ''
                local_url = f"{prefix}assets/icons/{filename}?v=1.3"
                content = content.replace(url, local_url)
                
            # Add defer to script.js if not already there
            # find <script src="script.js...">
            # replace with <script defer src="script.js...">
            content = re.sub(
                r'<script(?!\s+defer)\s+src="([^"]*script\.js[^"]*)"',
                r'<script defer src="\1"',
                content
            )
            
            # Bump cache version for script.js and style.css to ?v=1.3
            content = re.sub(r'script\.js(?:\?v=[0-9\.]+)?', 'script.js?v=1.3', content)
            content = re.sub(r'style\.css(?:\?v=[0-9\.]+)?', 'style.css?v=1.3', content)
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Applied enterprise fixes to {os.path.relpath(filepath, root_dir)}")
