import os
import re
import urllib.request

root_dir = r"H:\portfolio_website\hemalshah"
fonts_dir = os.path.join(root_dir, "assets", "fonts")
os.makedirs(fonts_dir, exist_ok=True)

font_url = "https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2"
local_font_filename = "inter-variable.woff2"
local_font_path = os.path.join(fonts_dir, local_font_filename)

# Download the font
if not os.path.exists(local_font_path):
    print(f"Downloading {font_url}...")
    req = urllib.request.Request(font_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        with open(local_font_path, 'wb') as f:
            f.write(response.read())
    print("Downloaded font.")

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
            
            # 1. Remove Google Fonts preconnects
            content = re.sub(r'<link\s+rel="preconnect"\s+href="https://fonts\.googleapis\.com"\s*/?>\s*', '', content)
            content = re.sub(r'<link\s+rel="preconnect"\s+href="https://fonts\.gstatic\.com"\s+crossorigin\s*/?>\s*', '', content)
            
            # 2. Remove the Google Fonts stylesheet link that was injected earlier
            content = re.sub(r'<link\s+rel="stylesheet"\s+href="https://fonts\.googleapis\.com/css2\?family=Inter[^"]*"\s*/?>\s*', '', content)
            
            # Calculate relative path to assets/fonts
            depth = os.path.relpath(dirpath, root_dir).count(os.sep) if dirpath != root_dir else 0
            prefix = '../' * depth if depth > 0 else ''
            rel_font_path = f"{prefix}assets/fonts/{local_font_filename}"
            
            # 3. Inject the font preload link right before the first <style> tag or inside <head>
            preload_link = f'<link rel="preload" href="{rel_font_path}" as="font" type="font/woff2" crossorigin="anonymous">\n  '
            
            # We will insert preload_link right before <style> tag if it exists and hasn't been added yet
            if 'as="font" type="font/woff2"' not in content:
                content = content.replace('<style>', preload_link + '<style>', 1)
                
            # 4. Inject the @font-face rule inside the <style> tag
            font_face_rule = f"@font-face {{ font-family: 'Inter'; font-style: normal; font-weight: 100 900; font-display: swap; src: url('{rel_font_path}') format('woff2'); }}"
            
            if "@font-face { font-family: 'Inter';" not in content:
                content = content.replace('<style>', f'<style>\n{font_face_rule}\n', 1)
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Self-hosted fonts in {os.path.relpath(filepath, root_dir)}")
