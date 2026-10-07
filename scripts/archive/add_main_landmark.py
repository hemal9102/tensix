import os
import re

root_dir = r"H:\portfolio_website\hemalshah"

def process_html(content):
    if '<main>' in content or '<main ' in content:
        # Already has main, skip
        return content
    
    header_end = content.find('</header>')
    footer_start = content.find('<footer class="site-footer">')
    
    if header_end != -1 and footer_start != -1:
        # Find where to inject <main>
        main_start_idx = header_end + len('</header>')
        
        # Check if there is <nav class="floating-dock" right after header
        # Let's search in the substring right after header
        sub = content[main_start_idx:main_start_idx+100]
        if '<nav class="floating-dock"' in sub:
            nav_start = content.find('<nav class="floating-dock"', main_start_idx)
            nav_end = content.find('</nav>', nav_start)
            if nav_end != -1:
                main_start_idx = nav_end + len('</nav>')
                
        # Also check for <!-- ── Floating Bottom Dock ────────────────── -->
        # Actually just insert <main> right at main_start_idx
        
        new_content = content[:main_start_idx] + '\n  <main>\n' + content[main_start_idx:footer_start] + '\n  </main>\n  ' + content[footer_start:]
        return new_content
    return content

count = 0
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
            content = process_html(content)
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
                print(f"Added <main> to {os.path.relpath(filepath, root_dir)}")

print(f"Modified {count} files.")
