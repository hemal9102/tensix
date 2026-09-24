import os
import re

root_dir = r"H:\portfolio_website\hemalshah"

html_files = [f for f in os.listdir(root_dir) if f.endswith('.html') and not f.startswith('google')]

for file_name in html_files:
    file_path = os.path.join(root_dir, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    has_title = "<title>" in content
    has_desc = 'name="description"' in content
    has_json = "application/ld+json" in content
    has_footer = '<footer class="site-footer">' in content
    has_dock = 'class="floating-dock"' in content
    has_resources_link = 'resources.html' in content
    
    print(f"{file_name}: Title: {has_title}, Desc: {has_desc}, JSON-LD: {has_json}, Footer: {has_footer}, Dock: {has_dock}, ResLinks: {has_resources_link}")
