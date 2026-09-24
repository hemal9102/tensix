import os
import re

blog_dir = r"H:\portfolio_website\hemalshah\blogs"
root_dir = r"H:\portfolio_website\hemalshah"

# Map old filenames to new SEO-friendly filenames
renames = {
    "blog1.html": "what-is-our-life.html",
    "blog2.html": "why-i-chose-automation-over-a-9-to-5.html",
    "blog3.html": "building-my-first-ai-project-lessons-learned.html",
    "blog4.html": "n8n-vs-python-scripts-when-to-use-which.html",
    "blog5.html": "the-ultimate-local-business-seo-master-strategy.html"
}

# 1. RENAME FILES ON DISK
for old, new in renames.items():
    old_path = os.path.join(blog_dir, old)
    new_path = os.path.join(blog_dir, new)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed {old} -> {new}")

# 2. UPDATE blogs.html
blogs_html_path = os.path.join(root_dir, "blogs.html")
with open(blogs_html_path, "r", encoding="utf-8") as f:
    blogs_content = f.read()

for old, new in renames.items():
    # href="blogs/blog1.html" -> href="blogs/what-is-our-life.html"
    blogs_content = blogs_content.replace(f'href="blogs/{old}"', f'href="blogs/{new}"')

with open(blogs_html_path, "w", encoding="utf-8") as f:
    f.write(blogs_content)

# 3. UPDATE sitemap-new.xml
sitemap_path = os.path.join(root_dir, "sitemap-new.xml")
with open(sitemap_path, "r", encoding="utf-8") as f:
    sitemap_content = f.read()

for old, new in renames.items():
    sitemap_content = sitemap_content.replace(f'/blogs/{old}', f'/blogs/{new}')

with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(sitemap_content)

# 4. UPDATE INTERNAL LINKS IN THE BLOG FILES THEMSELVES (e.g. Next -> blog2.html)
# Also update the canonical meta tags and JSON-LD URLs
for old, new in renames.items():
    # The file is now at `new`
    new_path = os.path.join(blog_dir, new)
    if not os.path.exists(new_path):
        continue
    
    with open(new_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace any mention of old filenames inside the content (like href="blog2.html")
    for old_link, new_link in renames.items():
        content = content.replace(f'href="{old_link}"', f'href="{new_link}"')
        
    # Replace canonical link and json-ld urls (we already set file_name in JSON-LD in the previous script)
    # The JSON-LD was injected as "https://hemalshah.vercel.app/blog1.html" (oops, the previous script injected root paths! Wait, previous script fixed root pages, not blog pages JSON-LD URLs, but let's just do a generic replace just in case)
    content = content.replace(f'/{old}', f'/{new}')
    
    with open(new_path, "w", encoding="utf-8") as f:
        f.write(content)
        
print("All blogs renamed and references updated!")
