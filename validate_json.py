import re, json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

JSONLD_RE = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.DOTALL | re.IGNORECASE)
blocks = JSONLD_RE.findall(html)
print(f'Found {len(blocks)} JSON-LD blocks\n')

for i, raw in enumerate(blocks):
    try:
        json.loads(raw.strip())
        print(f'Block {i+1}: OK')
    except json.JSONDecodeError as e:
        print(f'Block {i+1}: ERROR — {e}')
        lines = raw.strip().splitlines()
        err_line = e.lineno
        start = max(0, err_line - 4)
        end = min(len(lines), err_line + 3)
        for ln, text in enumerate(lines[start:end], start + start + 1):
            marker = '  <<<' if ln == err_line else ''
            print(f'  {ln:4d}: {text}{marker}')
        print()
