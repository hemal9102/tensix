import os
import re

blog_dir = r"H:\portfolio_website\hemalshah\blogs"

# Remove "1. ", "2. ", etc. from <h1> and <title> tags in blog HTML files
for f in os.listdir(blog_dir):
    if f.endswith('.html'):
        path = os.path.join(blog_dir, f)
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            
        original_content = content
        
        # Replace <title>1. What Is Our Life?
        content = re.sub(r'<title>([1-9]\.\s*)', '<title>', content)
        
        # Replace <h1>1. What Is Our Life?</h1>
        content = re.sub(r'<h1>([1-9]\.\s*)', '<h1>', content)
        
        # Replace "headline": "1. What Is Our Life?" in JSON-LD
        content = re.sub(r'"headline": "([1-9]\.\s*)', '"headline": "', content)
        
        # Replace "name": "1. What Is Our Life?" in JSON-LD
        content = re.sub(r'"name": "([1-9]\.\s*)', '"name": "', content)

        if content != original_content:
            with open(path, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"Updated title numbering in {f}")
