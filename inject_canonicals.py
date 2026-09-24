import os
import re

root_dir = r"H:\portfolio_website\hemalshah"
base_url = "https://hemalshah.vercel.app"

# Find all HTML files
for dirpath, dirnames, filenames in os.walk(root_dir):
    if 'node_modules' in dirnames:
        dirnames.remove('node_modules')
    if 'hk' in dirnames:
        dirnames.remove('hk')
    if '.git' in dirnames:
        dirnames.remove('.git')
        
    for file in filenames:
        if file.endswith('.html') and not file.startswith('google'):
            filepath = os.path.join(dirpath, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            
            # Remove any existing canonicals to avoid duplicates
            content = re.sub(r'<link rel="canonical" href=".*?"\s*/?>\n?', '', content)
            
            # Determine canonical URL (clean URLs, no .html needed if vercel handles it, but let's stick to literal)
            rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
            if rel_path == 'index.html':
                canonical_url = f"{base_url}/"
            else:
                canonical_url = f"{base_url}/{rel_path}"
                
            canonical_tag = f'  <link rel="canonical" href="{canonical_url}" />\n'
            
            # Inject right before </head>
            head_end_idx = content.find("</head>")
            if head_end_idx != -1:
                content = content[:head_end_idx] + canonical_tag + content[head_end_idx:]
                
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Added canonical to {rel_path}")
