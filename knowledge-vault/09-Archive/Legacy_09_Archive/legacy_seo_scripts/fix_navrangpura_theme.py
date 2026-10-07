import re

# 1. Read about.html
with open('C:/hk/DUMP/glibberish/about.html', 'r', encoding='utf-8') as f:
    about_html = f.read()

# Extract the big style blocks
# There are two <style> blocks in head
styles = re.findall(r'<style>.*?</style>', about_html, re.DOTALL)
core_styles = '\n'.join(styles)

# Extract body prefix (from <body> up to <main>)
body_prefix_match = re.search(r'<body>(.*?<main>)', about_html, re.DOTALL)
body_prefix = body_prefix_match.group(1)

# Extract footer and script (from </main> to </body>)
body_suffix_match = re.search(r'(</main>.*?</body>)', about_html, re.DOTALL)
body_suffix = body_suffix_match.group(1)

# 2. Read navrangpura.html
with open('C:/hk/DUMP/glibberish/navrangpura.html', 'r', encoding='utf-8') as f:
    nav_html = f.read()

# Custom styles we want to preserve for navrangpura
custom_styles = '''
.page-wrap{max-width:900px;margin:0 auto;padding:5rem 2rem 6rem;}
h1{font-size:clamp(1.9rem,5vw,3rem);font-weight:700;color:#fff;line-height:1.2;margin-bottom:1.25rem;}
.pgeo-intro{font-size:1.05rem;color:#cbd5e1;line-height:1.8;margin-bottom:3rem;max-width:700px;}
h2{font-size:1.4rem;font-weight:600;color:#fff;margin:3rem 0 1.5rem;}
.faq-list{display:flex;flex-direction:column;gap:1.25rem;}
.faq-card{background:var(--color-bg-card);border:1px solid rgba(255,255,255,0.08);border-radius:var(--border-radius);padding:1.6rem 1.8rem;}
.faq-card:hover{border-color:rgba(59,130,246,0.35);}
.faq-card h3{font-size:1rem;font-weight:600;color:#93c5fd;margin-bottom:0.65rem;}
.pgeo-answer{font-size:0.95rem;color:var(--color-text-muted);line-height:1.75;}
.services-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin:2rem 0 3rem;}
.service-pill{background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.2);border-radius:0.6rem;padding:0.85rem 1.1rem;font-size:0.9rem;color:#93c5fd;font-weight:500;}
.cta-block{background:linear-gradient(135deg,rgba(59,130,246,0.15),rgba(139,92,246,0.12));border:1px solid rgba(59,130,246,0.25);border-radius:var(--border-radius);padding:2rem;text-align:center;margin-top:3rem;}
.cta-block h2{margin:0 0 0.75rem;font-size:1.3rem;}
.cta-block p{color:var(--color-text-muted);margin-bottom:1.5rem;}
.cta-btn{display:inline-flex;align-items:center;gap:0.4rem;padding:0.75rem 1.8rem;background:linear-gradient(135deg,var(--color-blue),var(--color-purple));color:#fff;font-weight:600;border-radius:9999px;font-size:0.95rem;transition:opacity 0.2s,transform 0.2s;}
.cta-btn:hover{opacity:0.9;transform:translateY(-2px);color:#fff;}
.back-link{display:inline-flex;align-items:center;gap:0.4rem;color:var(--color-text-muted);font-size:0.9rem;margin-bottom:2.5rem;transition:color 0.2s;}
.back-link:hover{color:#fff;}
.location-badge{display:inline-flex;align-items:center;gap:0.5rem;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:9999px;padding:0.35rem 0.9rem;font-size:0.82rem;color:var(--color-text-muted);margin-bottom:1.25rem;}
@media(max-width:640px){.page-wrap{padding:4rem 1.25rem 5rem;}}
'''

# Replace styles in nav_html
combined_styles = f'{core_styles}\n<style>\n{custom_styles}\n</style>'
nav_html = re.sub(r'<style>.*?</style>', combined_styles, nav_html, flags=re.DOTALL)

# extract what's inside <main class="page-wrap">
main_content_match = re.search(r'<main class="page-wrap">(.*?)</main>', nav_html, re.DOTALL)
main_content = main_content_match.group(1)

# Put it in a section like core pages
new_main_content = f'''
<section class="section">
<div class="section-inner" style="max-width: 900px; margin: 0 auto; padding-top: 2rem;">
{main_content}
</div>
</section>
'''

new_body = f'''<body>
{body_prefix}
{new_main_content}
{body_suffix}'''

nav_html = re.sub(r'<body>.*?</body>', new_body, nav_html, flags=re.DOTALL)

with open('C:/hk/DUMP/glibberish/navrangpura.html', 'w', encoding='utf-8') as f:
    f.write(nav_html)

print("Done writing navrangpura.html")
