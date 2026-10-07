"""Convert every production page from the dark Swiss theme to the light theme.

Property-aware: colours inside <style> blocks, style="" attributes and SVG
fill/stroke attributes are remapped according to the CSS property they sit in
(text, background, border, shadow) and the rule they belong to (white text on a
saturated/dark button stays white). Idempotent: a page that already carries
<meta name="theme-color"> is left alone. Stdlib only.

    python apply_light_theme.py
"""
import colorsys
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP_DIR = re.compile(r'^(09_Archive|knowledge-vault|knowledge_base|0\d_.*|node_modules|resources|skills|tests|tools)$')
MARKER = '<meta name="theme-color" content="#ffffff">'
PRISM_LIGHT = 'https://cdnjs.cloudflare.com/ajax/libs/prism-themes/1.9.0/prism-coldark-cold.min.css'
PRISM_LIGHT_SRI = 'sha384-jgh29qbN0Sqy02lb0Sl2Ha77kxfgaHt2VeZ4fnOH7DbDNehViGzeX/Ow56I3Cj1j'  # WCAG-AA light theme

# ── exact token / component swaps (both token sets) ──────────────────────────
TOKENS = [
    (r'--color-bg:\s*#(?:090A0F|0F172A);', '--color-bg:#FFFFFF;'),
    (r'--color-bg-light:\s*#(?:0F121C|1e293b);', '--color-bg-light:#F8FAFC;'),
    (r'--color-bg-card:\s*rgba\(255,\s*255,\s*255,\s*0?\.0\d+\);', '--color-bg-card:rgba(15,23,42,0.03);'),
    (r'--color-text:\s*#(?:F8FAFC|e2e8f0);', '--color-text:#0F172A;'),
    (r'--color-text-muted:\s*#(?:94A3B8|aab6c8);', '--color-text-muted:#475569;'),
    (r'--color-primary:\s*#ff6b6b;', '--color-primary:#DC2626;'),
    (r'--color-accent:\s*#ffd166;', '--color-accent:#B45309;'),
    (r'(--glow-(?:blue|purple):\s*rgba\(\d+,\s*\d+,\s*\d+,\s*)0?\.\d+\)', r'\g<1>0.18)'),
    (r'--shadow-d1:[^;]*;', '--shadow-d1:0 4px 16px rgba(15,23,42,0.06);'),
    (r'--shadow-d2:[^;]*;', '--shadow-d2:0 12px 40px rgba(15,23,42,0.08);'),
    (r'--shadow-d3:[^;]*;', '--shadow-d3:0 24px 64px rgba(15,23,42,0.12);'),
    (r'(\.gradient-text\s*\{[^}]*?background(?:-image)?\s*:\s*)linear-gradient\((?:[^()]|\([^()]*\))*\)',
     r'\g<1>linear-gradient(90deg,#0F172A 0%,#1D4ED8 35%,#7C3AED 65%,#0F172A 100%)'),
    (r'color-scheme:\s*dark', 'color-scheme:light'),
]
# values the var() resolver needs when deciding what a background will look like
VARS = {'--color-blue': '#3b82f6', '--color-purple': '#8b5cf6', '--color-primary': '#DC2626',
        '--color-accent': '#B45309', '--color-bg': '#FFFFFF', '--color-bg-light': '#F8FAFC',
        '--color-text': '#0F172A', '--color-text-muted': '#475569'}

# hand-picked Tailwind 700/800 shades for light/pastel text colours (>=4.5:1 even on tinted badges)
FG_MAP = {
    '93c5fd': '1D4ED8', '60a5fa': '1D4ED8', '3b82f6': '1D4ED8', '2563eb': '1D4ED8', '38bdf8': '0369A1',
    'c4b5fd': '6D28D9', 'a78bfa': '6D28D9', '8b5cf6': '6D28D9', '7c3aed': '6D28D9', 'c084fc': '7E22CE',
    '86efac': '166534', '4ade80': '166534', '22c55e': '166534', '25d366': '166534',
    '34d399': '065F46', '10b981': '065F46', '059669': '065F46',
    'fdba74': '9A3412', 'fb923c': '9A3412', 'f97316': '9A3412', 'ff4500': 'C2410C',
    'fca5a5': 'B91C1C', 'f87171': 'B91C1C', 'ef4444': 'B91C1C', 'ff6b6b': 'B91C1C', 'dc2626': 'B91C1C',
    'e879f9': 'A21CAF', 'ffd166': '92400E', 'fde68a': '92400E', 'fbbf24': '92400E', 'facc15': '854D0E',
}

COLOR = re.compile(r'url\([^)]*\)|#[0-9a-fA-F]{8}\b|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3,4}\b'
                   r'|rgba?\(\s*[\d.]+\s*,\s*[\d.]+\s*,\s*[\d.]+\s*(?:,\s*[\d.]+\s*)?\)'
                   r'|(?<![-\w])(?:white|black)(?![-\w])')
DECL = re.compile(r'([-\w]+)(\s*:\s*)((?:url\([^)]*\)|[^;{}])*)')
RULE = re.compile(r'([^{}]*)\{([^{}]*)\}')

FG = {'color', '-webkit-text-fill-color', 'caret-color', 'text-decoration-color', 'text-decoration'}
SVG = {'fill', 'stroke', 'stop-color'}
BG = {'background', 'background-color', 'background-image'}
SHADOW = {'box-shadow', 'text-shadow', 'filter', '-webkit-filter'}
EDITS = [0]  # per-file colour edit counter
CONSOLE_SEL =re.compile(r'(?<![-\w])(pre|code|console|terminal)(?![-\w])', re.I)


def parse(tok):
    t = tok.lower()
    if t == 'white':
        return 255, 255, 255, 1.0
    if t == 'black':
        return 0, 0, 0, 1.0
    if t.startswith('#'):
        h = t[1:]
        if len(h) in (3, 4):
            h = ''.join(c * 2 for c in h)
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a
    if t.startswith('rgb'):
        p = [float(x) for x in re.findall(r'[\d.]+', t)]
        return int(p[0]), int(p[1]), int(p[2]), (p[3] if len(p) > 3 else 1.0)
    return None


def lum(r, g, b, *_):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def sat(r, g, b, *_):
    return max(r, g, b) - min(r, g, b)


def hexs(r, g, b):
    return '#%02X%02X%02X' % (r, g, b)


def slate(a):  # rgba(15,23,42,a)
    return 'rgba(15,23,42,%s)' % (('%.3f' % a).rstrip('0').rstrip('.') or '0')


def darken(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    while l > 0 and 1.05 / (lum(r, g, b) + 0.05) < 4.5:
        l -= 0.02
        r, g, b = (round(x * 255) for x in colorsys.hls_to_rgb(h, l, s))
    return hexs(r, g, b)


def fg(c, alpha_keep=False):
    """Text / icon colour that will sit on a light surface."""
    r, g, b, a = c
    L = lum(*c)
    if sat(*c) < 45:
        if L > 0.6:
            if alpha_keep and a < 1:
                return slate(a)
            if a < 1:
                return '#0F172A' if a >= 0.7 else '#475569'
            return '#0F172A' if L > 0.8 else '#334155'
        if L > 0.2:
            return '#475569'
        return None
    key = '%02x%02x%02x' % (r, g, b)
    if key in FG_MAP and a >= 0.5:
        return '#' + FG_MAP[key]
    if a == 1 and 1.05 / (L + 0.05) < 4.5:
        return darken(r, g, b)
    return None


def bg(c, console=False, footer=False):
    r, g, b, a = c
    L = lum(*c)
    if sat(*c) >= 45:
        return None
    if L < 0.05:  # dark surface -> light surface
        if a < 1:
            return 'rgba(255,255,255,%s)' % ('%.3f' % a).rstrip('0').rstrip('.')
        if footer:
            return '#F8FAFC'
        if console:
            return '#F1F5F9'
        return '#FFFFFF' if L < 0.0045 else '#F8FAFC' if L < 0.012 else '#F1F5F9'
    if L > 0.6:
        if a >= 0.9:  # white button / swatch -> dark button
            return '#0F172A' if L > 0.85 else '#1E293B'
        return slate(a)
    return None


def border(c):
    r, g, b, a = c
    L = lum(*c)
    if sat(*c) >= 45:
        return None
    if L > 0.6:
        return slate(a) if a < 1 else ('#0F172A' if L > 0.85 else '#334155')
    if L < 0.05 and a == 1:
        return '#E2E8F0'
    return None


def shadow(c):
    r, g, b, a = c
    L = lum(*c)
    if sat(*c) >= 45:
        return None
    if L < 0.05 or L > 0.6:
        return slate(max(0.04, round(a * (0.3 if L < 0.05 else 0.5), 3)))
    return None


def resolve_vars(v):
    return re.sub(r'var\(\s*(--[-\w]+)\s*(?:,\s*([^()]*))?\)', lambda m: VARS.get(m.group(1), m.group(2) or ''), v)


def first_solid(v):
    for t in COLOR.findall(v):
        c = parse(t) if not t.startswith('url') else None
        if c and c[3] >= 0.5:
            return c
    return None


def sub_colors(value, fn):
    def rep(m):
        t = m.group(0)
        if t.startswith('url'):
            return t
        c = parse(t)
        out = fn(c) if c else None
        if out and out != t:
            EDITS[0] += 1
        return out or t
    return COLOR.sub(rep, value)


def convert_block(selector, body):
    decls = [(m.group(1).lower(), m.group(3)) for m in DECL.finditer(body)]
    clip_text = any(p.endswith('background-clip') and 'text' in v for p, v in decls)
    console = bool(CONSOLE_SEL.search(selector))
    footer = 'footer' in selector.lower()
    # what will the background of this rule look like after conversion?
    surface = None
    for p, v in decls:
        if p in BG and not clip_text:
            c = first_solid(v)
            if c:
                new = bg(c, console, footer)
                surface = parse(new) if new else c
            elif 'var(' in v:  # theme tokens already hold their light-theme values
                surface = first_solid(resolve_vars(v)) or surface
    dark_surface = surface is not None and (lum(*surface) < 0.3 or sat(*surface) >= 80)

    def text_fn(c):
        if dark_surface:  # white text on a saturated/dark button stays white
            return '#FFFFFF' if (sat(*c) < 45 and lum(*c) < 0.05 and lum(*surface) < 0.3) else None
        return fg(c)

    def decl(m):
        prop = m.group(1).lower()
        val = m.group(3)
        if prop.startswith('--'):
            name = prop
            if name.startswith('--color-') or 'glow' in name or 'shadow' in name:
                return m.group(0)
            fn = ((lambda c: bg(c)) if 'bg' in name else fg if ('text' in name or 'accent' in name)
                  else border if 'border' in name else None)
        elif prop in FG:
            fn = text_fn
            if not dark_surface:  # brand tokens are too light for body-size text on white
                val = val.replace('var(--color-blue)', '#1D4ED8').replace('var(--color-purple)', '#6D28D9')
        elif prop in SVG:
            fn = (lambda c: None) if dark_surface else (lambda c: fg(c, alpha_keep=True))
        elif prop in BG:
            fn = fg if clip_text else (lambda c: bg(c, console, footer))
        elif prop.startswith('border') or prop.startswith('outline') or prop == 'column-rule':
            fn = border
        elif prop in SHADOW:
            fn = shadow
        else:
            fn = None
        return m.group(1) + m.group(2) + sub_colors(val, fn) if fn else m.group(0)

    return DECL.sub(decl, body)


def convert_css(css):
    for pat, rep in TOKENS:
        css = re.sub(pat, rep, css, flags=re.I)
    css = RULE.sub(lambda m: m.group(1) + '{' + convert_block(m.group(1), m.group(2)) + '}', css)
    # header / footer finishing touches
    css = re.sub(r'(\.site-header\.scrolled\s*\{\s*background:\s*)rgba\(255,255,255,0?\.\d+\)', r'\1rgba(255,255,255,0.92)', css)
    return css


def svg_attr(m):
    c = parse(m.group(3)) if COLOR.fullmatch(m.group(3)) else None
    if not c or (c[:3] == (255, 255, 255) and c[3] == 1):  # solid white icons sit on coloured buttons
        return m.group(0)
    out = fg(c, alpha_keep=True)
    EDITS[0] += bool(out)
    return m.group(1) + '="' + out + '"' if out else m.group(0)


def convert_html(s):
    s = re.sub(r'(<style[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + convert_css(m.group(2)) + m.group(3), s, flags=re.S)
    s = re.sub(r'(\sstyle=")([^"]*)(")', lambda m: m.group(1) + convert_block('', m.group(2)) + m.group(3), s)
    s = re.sub(r"(\sstyle=')([^']*)(')", lambda m: m.group(1) + convert_block('', m.group(2)) + m.group(3), s)
    s = re.sub(r'\b(fill|stroke|stop-color)(=")([^"]*)"', svg_attr, s)
    # light Prism theme for code blocks
    s = re.sub(r'(<link[^>]*?)https://[^"]*prism-tomorrow\.min\.css"([^>]*>)',
               lambda m: re.sub(r'integrity="[^"]*"', 'integrity="%s"' % PRISM_LIGHT_SRI, m.group(1) + PRISM_LIGHT + '"' + m.group(2)), s)
    s = re.sub(r"(mermaid\.initialize\(\{[^}]*theme:\s*)'dark'", r"\1'neutral'", s)
    vp = re.search(r'<meta[^>]*name="viewport"[^>]*>', s)
    at = vp.end() if vp else s.index('<head>') + len('<head>')
    return s[:at] + '\n' + MARKER + s[at:]


def pages():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.') and not (root == ROOT and SKIP_DIR.match(d))]
        for f in files:
            if f.endswith('.html') and not f.startswith('google'):
                yield os.path.join(root, f)


def main():
    total = 0
    for path in sorted(pages()):
        with open(path, encoding='utf-8', newline='') as f:
            src = f.read()
        out = src
        EDITS[0] = 0
        if MARKER not in out:
            out = convert_html(out)
        out = re.sub(r'script\.js\?v=1\.3\b', 'script.js?v=1.4', out)
        rel = os.path.relpath(path, ROOT)
        if out != src:
            with open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(out)
            total += 1
            print('%-70s %5d colour edits' % (rel, EDITS[0]))
        else:
            print('%-70s unchanged' % rel)

    js = os.path.join(ROOT, 'script.js')
    with open(js, encoding='utf-8', newline='') as f:
        src = f.read()
    out = (src.replace('ctx.fillStyle = `rgba(255,255,255,${pt.opacity})`;', 'ctx.fillStyle = `rgba(15,23,42,${pt.opacity})`;')
              .replace("ctx.strokeStyle = 'rgba(255,255,255,0.18)';", "ctx.strokeStyle = 'rgba(15,23,42,0.12)';")
              .replace("btn.style.color = '#fff';", "btn.style.color = '#1D4ED8';")
              .replace("'background:rgba(255,255,255,0.22)',", "'background:rgba(15,23,42,0.15)',"))
    if out != src:
        with open(js, 'w', encoding='utf-8', newline='') as f:
            f.write(out)
        total += 1
        print('script.js                                                              canvas colours')
    print('Light theme: %d file(s) changed.' % total)


if __name__ == '__main__':
    main()
