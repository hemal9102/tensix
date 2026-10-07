import os

root_dir = r"H:\portfolio_website\hemalshah"
target_line = '<link rel="preconnect" href="https://fonts.googleapis.com" />'
new_preconnects = """  <!-- Preconnect to external image CDNs for LCP optimization -->
  <link rel="preconnect" href="https://www.vectorlogo.zone" />
  <link rel="preconnect" href="https://n8n.io" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />"""

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
                
            if target_line in content:
                content = content.replace(target_line, new_preconnects)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Added preconnect hints to {os.path.relpath(filepath, root_dir)}")
