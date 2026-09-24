import os
import re

root_dir = r"H:\portfolio_website\hemalshah"
css_path = os.path.join(root_dir, "style.css")

with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

# Extract and remove @import
import_match = re.search(r"@import\s+url\(['\"](https://fonts\.googleapis\.com[^'\"]+)['\"]\);", css_content)
google_fonts_url = ""
if import_match:
    google_fonts_url = import_match.group(1)
    css_content = css_content.replace(import_match.group(0), "")

# We will inject this block
injected_block = ""
if google_fonts_url:
    injected_block += f'<link rel="stylesheet" href="{google_fonts_url}" />\n  '
injected_block += f'<style>{css_content}</style>'

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
            
            # Find the style.css link tag (e.g. href="style.css?v=1.3" or href="../style.css")
            # And replace it with the Google Fonts link + Inline CSS
            content = re.sub(
                r'<link\s+rel="stylesheet"\s+href="[^"]*style\.css[^"]*"\s*/?>',
                injected_block.replace('\\', '\\\\'), # escape backslashes if any
                content
            )
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Inlined CSS in {os.path.relpath(filepath, root_dir)}")
