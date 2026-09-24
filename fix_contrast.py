import os

root_dir = r"H:\portfolio_website\hemalshah"

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
            
            # Fix footer bottom contrast (copyright text)
            content = content.replace("color:rgba(148,163,184,0.6);", "color:#cbd5e1;")
            
            # Fix main footer contrast
            content = content.replace(".site-footer{background:#080d19;border-top:1px solid rgba(255,255,255,0.06);padding:3rem 2rem 3rem;color:var(--color-text-muted);}", 
                                      ".site-footer{background:#080d19;border-top:1px solid rgba(255,255,255,0.06);padding:3rem 2rem 3rem;color:#cbd5e1;}")
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed contrast in {os.path.relpath(filepath, root_dir)}")
