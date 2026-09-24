import os
import re

root_dir = r"H:\portfolio_website\hemalshah"
count = 0

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
            
            # Remove any preload links for style.css
            content = re.sub(r'<link\s+rel="preload"\s+href="[^"]*style\.css[^"]*"\s+as="style"\s*/?>\s*', '', content)
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
                print(f"Removed style.css preload from {os.path.relpath(filepath, root_dir)}")

print(f"Removed dead preload links from {count} files.")
