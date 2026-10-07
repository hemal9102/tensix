import os
import re
from PIL import Image

root_dir = r"H:\portfolio_website\hemalshah"
favicon_png = os.path.join(root_dir, "assets", "favicon.png")
favicon_webp = os.path.join(root_dir, "assets", "favicon.webp")

try:
    if os.path.exists(favicon_png):
        with Image.open(favicon_png) as img:
            # Save 70x70 webp for on-page image tags
            img_70 = img.resize((70, 70), Image.Resampling.LANCZOS)
            img_70.save(favicon_webp, "WEBP", quality=85)
            print("Saved favicon.webp at 70x70.")
            
            # Save 32x32 png for the browser tab icon
            img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
            img_32.save(favicon_png, "PNG", optimize=True)
            print("Resized favicon.png to 32x32.")
            
except Exception as e:
    print(f"Error optimizing images: {e}")

# Replace img src in all HTML files
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
            
            # We ONLY want to replace the image tags, NOT the link rel="icon" tag.
            # Using regex to target <img ... src="...favicon.png" ...>
            content = re.sub(r'(<img[^>]*src=["\'](?:[^"\']*?/)?assets/)favicon\.png(["\'][^>]*>)', r'\1favicon.webp\2', content)
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated img src to webp in {os.path.relpath(filepath, root_dir)}")
