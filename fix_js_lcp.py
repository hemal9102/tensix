import os
import re

root_dir = r"H:\portfolio_website\hemalshah"
p5_tag = '<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js"></script>'
p5_tag_defer = '<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js" defer></script>'

# 1. Update p5.js and remove duplicates
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
            
            # Remove all instances of p5
            content = content.replace(p5_tag, "")
            content = content.replace(p5_tag_defer, "")
            
            # Insert exactly one instance with defer in the head if it previously had p5
            if p5_tag in original_content or p5_tag_defer in original_content:
                # Add it before </head>
                content = content.replace("</head>", f"  {p5_tag_defer}\n</head>")
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

# 2. Fix LCP Render Delay in index.html (remove reveal from hero content)
index_path = os.path.join(root_dir, "index.html")
if os.path.exists(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove reveal classes from the hero elements
    content = content.replace('<h1 class="reveal">', '<h1>')
    content = content.replace('class="hero-subtitle-row reveal reveal-delay-1"', 'class="hero-subtitle-row"')
    content = content.replace('class="hero-description reveal reveal-delay-2"', 'class="hero-description"')
    content = content.replace('class="hero-tags reveal reveal-delay-3"', 'class="hero-tags"')
    content = content.replace('class="hero-cta reveal reveal-delay-4"', 'class="hero-cta"')

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed LCP element delays in index.html and deferred p5.js globally.")
