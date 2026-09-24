import re
import os

css_path = r"H:\portfolio_website\hemalshah\style.css"

if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
        
    # 1. Remove comments
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    
    # 2. Remove tabs and newlines
    css = re.sub(r"\n+", "", css)
    css = re.sub(r"\t+", "", css)
    
    # 3. Remove multiple spaces
    css = re.sub(r" +", " ", css)
    
    # 4. Remove spaces around special characters
    css = re.sub(r" ?([\{\}\;\:\,\>\+\~]) ?", r"\1", css)
    
    # Overwrite the original file to satisfy Lighthouse without changing HTML links
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css)
    print("Minified style.css successfully.")
else:
    print("style.css not found.")
