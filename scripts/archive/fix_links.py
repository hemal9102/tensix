import os
import re

directory = 'C:/hk/DUMP/glibberish'

links_to_fix = [
    'about', 'work', 'services', 'blogs', 'contact',
    'resources', 'compare', 'frameworks', 'gallery', 'team',
    'navrangpura', 'hk-engineering-ahmedabad', 'ahmedabad-software-engineering'
]

# We want to replace href="<link>" or href="<link>#something" or href="/<link>"
# with href="<link>.html"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    for link in links_to_fix:
        # replace href="about" -> href="about.html"
        new_content = re.sub(fr'href="{link}"', f'href="{link}.html"', new_content)
        # replace href="/about" -> href="/about.html"
        new_content = re.sub(fr'href="/{link}"', f'href="/{link}.html"', new_content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            process_file(os.path.join(root, file))

print("Done updating links.")
