import glob

files = glob.glob('H:/hemalshah/**/*.html', recursive=True)
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if 'reveal' in content and 'script.js' not in content:
        new_content = content.replace('</body>', '<script src="/script.js" defer></script>\n</body>')
        if new_content != content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f'Fixed {f}')
