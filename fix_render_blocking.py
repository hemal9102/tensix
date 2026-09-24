import os
import re

root_dir = r"H:\portfolio_website\hemalshah"
old_font = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />'
new_font = """  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" as="style" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" media="print" onload="this.media='all'" />
  <noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" /></noscript>"""

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
            
            # 1. Fix Google Fonts
            content = content.replace(old_font, new_font)
            
            # 2. Add preload for style.css if not exists
            style_match = re.search(r'<link rel="stylesheet" href="(\.\./)*style\.css" />', content)
            if style_match:
                style_path = style_match.group(1) if style_match.group(1) else ""
                style_tag = f'<link rel="stylesheet" href="{style_path}style.css" />'
                preload_tag = f'<link rel="preload" href="{style_path}style.css" as="style" />\n  {style_tag}'
                
                # Check if we already added it
                if f'<link rel="preload" href="{style_path}style.css" as="style" />' not in content:
                    content = content.replace(style_tag, preload_tag)
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated render-blocking resources in {os.path.relpath(filepath, root_dir)}")
