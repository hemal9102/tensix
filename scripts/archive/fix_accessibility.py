import os
import glob
import re

directory = 'H:/hemalshah'
files = glob.glob(directory + '/**/*.html', recursive=True) + glob.glob(directory + '/**/*.py', recursive=True)

count = 0
for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        original_content = content
        
        # 1. Fix contrast for local-seo-anchor
        content = content.replace("color: #94a3b8;", "color: #94a3b8;")
        
        # 2. Fix contrast for address / a tags that were too dark (#475569 is Slate 600, too dark for #080d19)
        content = content.replace("color:#94a3b8;", "color:#94a3b8;")
        
        # 3. Wrap WhatsApp chat button in an <aside> to fix the landmark issue
        # We need to make sure we don't double wrap it if already wrapped
        if '<aside aria-label="WhatsApp Chat">' not in content and 'aria-label="Chat on WhatsApp"' in content:
            # Find the full WhatsApp anchor tag including inner SVG/content
            pattern = r'(<a[^>]*aria-label="Chat on WhatsApp"[^>]*>.*?</a>)'
            content = re.sub(pattern, r'<aside aria-label="WhatsApp Chat">\n\1\n</aside>', content, flags=re.DOTALL)
            
        if content != original_content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated {f}")
            count += 1
    except Exception as e:
        print(f"Error on {f}: {e}")

print(f"Total files updated: {count}")
