import glob
from bs4 import BeautifulSoup
import re
import os

directory = 'H:/hemalshah/blogs'
files = glob.glob(directory + '/**/*.html', recursive=True)

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    soup = BeautifulSoup(content, 'html.parser')
    
    main_tag = soup.find('main')
    if not main_tag:
        continue
        
    # Check if already has the valid structure
    article = main_tag.find('article')
    blog_post = main_tag.find('div', class_='blog-post')
    
    if article and blog_post:
        print(f"Skipping {f}, already valid.")
        continue
        
    print(f"Fixing {f}...")
    
    # Extract pieces
    h1 = main_tag.find('h1')
    author_badge = main_tag.find('div', class_='author-badge')
    
    # Find the path prefix for back link depending on folder depth
    depth = f.replace('\\', '/').replace('H:/hemalshah/blogs/', '').count('/')
    prefix = '../' if depth == 0 else '../../'
    
    # The content is everything after h1
    content_nodes = []
    if h1:
        current = h1.next_sibling
        while current:
            content_nodes.append(str(current))
            current = current.next_sibling
            
    article_html = "".join(content_nodes).strip()
    
    # Create the new main content
    # Look for publish date in author badge
    date_str = "Published on "
    if author_badge:
        span = author_badge.find('span')
        if span and '• Published ' in span.text:
            date_str += span.text.split('• Published ')[1]
        else:
            date_str += "2026"
            
    # Clean up author badge to standard style
    author_badge_html = f"""
    <div class="author-badge" style="display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem; padding: 1rem; background: rgba(255,255,255,0.03); border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
    <img src="{prefix}assets/favicon.webp?v=1.1" style="border-radius: 50%;" width="50"/>
    <div>
    <strong style="color: #fff; display: block; font-size: 1.1rem;">Hemal Shah (HK)</strong>
    <span style="font-size: 0.9rem; color: #94a3b8;">AI Automation Engineer & Technical SEO</span>
    </div>
    </div>
    """
    
    new_main_html = f"""<main>
<!-- ── Blog Content ────────────────────────── -->
<section class="section" style="padding-top:calc(var(--header-height) + 3rem);">
<div class="section-inner">
<a class="blog-back reveal" href="{prefix}blogs.html">
        ← Back to Blog
      </a>
<div class="blog-post reveal">
{author_badge_html}
<h1>{h1.text if h1 else ''}</h1>
<p class="blog-meta">{date_str}</p>
<article>
{article_html}
</article>
</div>
</div>
</section>
</main>"""

    # Replace the old <main>...</main> with the new one
    # Because BeautifulSoup can mess up formatting when writing out the whole document,
    # we'll use regex to replace just the main block.
    
    # regex to find main block
    pattern = r'<main.*?>.*?</main>'
    new_content = re.sub(pattern, new_main_html, content, flags=re.DOTALL)
    
    with open(f, 'w', encoding='utf-8') as out_f:
        out_f.write(new_content)
        
    print(f"Fixed {f}")
