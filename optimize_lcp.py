import os
import re
from PIL import Image

root_dir = r"H:\portfolio_website\hemalshah"
favicon_path = os.path.join(root_dir, "assets", "favicon.png")

# 1. Resize favicon
try:
    if os.path.exists(favicon_path):
        with Image.open(favicon_path) as img:
            print(f"Original size: {img.size}")
            # Resize down to 100x100
            img_resized = img.resize((100, 100), Image.Resampling.LANCZOS)
            img_resized.save(favicon_path, optimize=True, format="PNG")
        print("Successfully resized favicon.png to 100x100.")
    else:
        print("favicon.png not found.")
except Exception as e:
    print(f"Error resizing favicon: {e}")

# 2. Replace OpenCV image link globally
old_opencv = "https://opencv.org/wp-content/uploads/2020/07/OpenCV_logo_no_text_.png"
new_opencv = "https://www.vectorlogo.zone/logos/opencv/opencv-icon.svg"

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
                
            if old_opencv in content:
                content = content.replace(old_opencv, new_opencv)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated OpenCV logo in {os.path.relpath(filepath, root_dir)}")
