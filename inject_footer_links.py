import os
import re

directory = 'C:/hk/DUMP/glibberish'

inject_block = '''<nav aria-label="Ahmedabad Hubs navigation" class="footer-nav">
<h3>Ahmedabad Hubs</h3>
<ul>
<li><a href="hk-engineering-ahmedabad.html">HK Engineering Ahmedabad</a></li>
<li><a href="ahmedabad-software-engineering.html">Software Engineering Ahmedabad</a></li>
<li><a href="navrangpura.html">Navrangpura Hub</a></li>
</ul>
</nav>
'''

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # check if already injected
    if 'Ahmedabad Hubs navigation' in content:
        return

    # find <div class="footer-social">
    if '<div class="footer-social">' in content:
        new_content = content.replace('<div class="footer-social">', inject_block + '<div class="footer-social">')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith('.html') and not file.startswith('google'):
            process_file(os.path.join(root, file))

print("Done injecting footer links.")
