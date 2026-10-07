import urllib.request
import re
import os

url = "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})

try:
    with urllib.request.urlopen(req) as response:
        css_content = response.read().decode('utf-8')
    print("Downloaded CSS successfully")
    # find all latin blocks
    # A block might look like:
    # /* latin */
    # @font-face { ... }
    
    latin_blocks = []
    blocks = css_content.split('/* latin */')
    if len(blocks) > 1:
        for b in blocks[1:]:
            # The block starts with @font-face { ... }
            match = re.search(r'@font-face\s*\{[^}]+\}', b)
            if match:
                latin_blocks.append(match.group(0))
    
    print(f"Found {len(latin_blocks)} latin font-face blocks.")
    for lb in latin_blocks:
        print(lb)
        
except Exception as e:
    print(f"Error: {e}")
