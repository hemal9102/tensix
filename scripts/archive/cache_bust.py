import os
import re

root_dir = r"H:\portfolio_website\hemalshah"
cache_version = "v=1.1"

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
            
            # Cache bust style.css
            content = re.sub(r'href="((?:\.\./)*)style\.css"', rf'href="\1style.css?{cache_version}"', content)
            # Cache bust script.js
            content = re.sub(r'src="((?:\.\./)*)script\.js"', rf'src="\1script.js?{cache_version}"', content)
            # Cache bust favicon.webp
            content = re.sub(r'src="((?:\.\./)*)assets/favicon\.webp"', rf'src="\1assets/favicon.webp?{cache_version}"', content)
            # Cache bust icons
            content = re.sub(r'src="((?:\.\./)*)assets/icons/([^"]+\.svg)"', rf'src="\1assets/icons/\2?{cache_version}"', content)
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Added cache busting to {os.path.relpath(filepath, root_dir)}")
