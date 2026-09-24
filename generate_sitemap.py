import os
from datetime import datetime

root_dir = r"H:\portfolio_website\hemalshah"
base_url = "https://hemalshah.vercel.app"

# Find all HTML files, ignoring google verification, the hk/ folder, and node_modules
html_files = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Skip ignored directories
    if 'node_modules' in dirnames:
        dirnames.remove('node_modules')
    if 'hk' in dirnames:
        dirnames.remove('hk')
    if '.git' in dirnames:
        dirnames.remove('.git')
        
    for file in filenames:
        if file.endswith('.html') and not file.startswith('google'):
            # Get relative path
            rel_path = os.path.relpath(os.path.join(dirpath, file), root_dir)
            # Convert Windows backslashes to forward slashes for URLs
            rel_path_unix = rel_path.replace('\\', '/')
            html_files.append(rel_path_unix)

# Generate sitemap XML content
today = datetime.now().strftime("%Y-%m-%d")

xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

for file_path in sorted(html_files):
    # Determine priority based on importance
    if file_path == 'index.html':
        loc = base_url + "/"
        priority = "1.0"
    elif file_path in ['about.html', 'work.html', 'services.html']:
        loc = f"{base_url}/{file_path}"
        priority = "0.9"
    elif file_path.startswith('blogs/'):
        loc = f"{base_url}/{file_path}"
        priority = "0.7"
    else:
        loc = f"{base_url}/{file_path}"
        priority = "0.8"
        
    # Some URLs might be backup or temp files, let's filter wr1.html if present
    if "wr1.html" in file_path:
        continue

    xml_lines.append('  <url>')
    xml_lines.append(f'    <loc>{loc}</loc>')
    xml_lines.append(f'    <lastmod>{today}</lastmod>')
    xml_lines.append('    <changefreq>monthly</changefreq>')
    xml_lines.append(f'    <priority>{priority}</priority>')
    xml_lines.append('  </url>')

xml_lines.append('</urlset>')

sitemap_path = os.path.join(root_dir, 'sitemap-new.xml')
with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_lines))

print(f"Sitemap successfully regenerated at {sitemap_path} with {len(html_files)} entries.")
