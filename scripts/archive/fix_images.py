import re
import os

filepath = r"H:\portfolio_website\hemalshah\services.html"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

original_content = content

# Replace 
# <img src="https://www.vectorlogo.zone/..." alt="..." />
# with 
# <img src="https://www.vectorlogo.zone/..." alt="..." width="40" height="40" loading="lazy" />

pattern = r'(<img src="https://(?:www\.vectorlogo\.zone|n8n\.io|cdn).*?" alt=".*?")\s*/?>'

def add_attributes(match):
    img_tag = match.group(1)
    if 'width' not in img_tag:
        return f'{img_tag} width="40" height="40" loading="lazy" />'
    return match.group(0)

content = re.sub(pattern, add_attributes, content)

if content != original_content:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated image tags in services.html")
else:
    print("No changes needed in services.html")
