import os
import glob
from bs4 import BeautifulSoup

html_files = glob.glob('**/*.html', recursive=True)

for file in html_files:
    if 'node_modules' in file:
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    changed = False
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        
        # We only care about internal links
        if href.startswith('http') or href.startswith('//') or href.startswith('mailto:') or href.startswith('tel:'):
            continue
        
        if href.endswith('.html'):
            new_href = href[:-5]
            if new_href == 'index':
                new_href = '/'
            elif new_href == '':
                pass
            a['href'] = new_href
            changed = True
        elif 'index.html' in href:
            new_href = href.replace('index.html', '')
            a['href'] = new_href
            changed = True
            
    if changed:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Fixed internal links in {file}")
