import os
import re

root_dir = r"H:\portfolio_website\hemalshah"
old_url = "https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js"
new_url = "https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"

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
                
            if old_url in content:
                content = content.replace(old_url, new_url)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Upgraded p5.js in {os.path.relpath(filepath, root_dir)}")
