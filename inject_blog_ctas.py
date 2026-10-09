import os
import re

missing_blogs = [
    r'D:\projects\tensix\blogs\building-my-first-ai-project-lessons-learned.html',
    r'D:\projects\tensix\blogs\n8n-vs-python-scripts-when-to-use-which.html',
    r'D:\projects\tensix\blogs\the-future-of-seo-geo-and-search-engines.html',
    r'D:\projects\tensix\blogs\the-ultimate-local-business-seo-master-strategy.html',
    r'D:\projects\tensix\blogs\why-i-chose-automation-over-a-9-to-5.html',
    r'D:\projects\tensix\blogs\case-studies\china-vs-india-ai-race-cheap-llms.html',
    r'D:\projects\tensix\blogs\case-studies\irctc-system-design-scalability.html',
    r'D:\projects\tensix\blogs\case-studies\whatsapp-system-design-outage.html'
]

cta_block = '''
<div class="inquiry-cta" style="margin: 3rem 0; padding: 2.5rem; background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(139,92,246,0.1)); border: 1px solid rgba(139,92,246,0.3); border-radius: 0.8rem; text-align: center; box-shadow: 0 10px 30px rgba(15,23,42,0.06);">
<h2 style="font-size: 1.8rem; font-weight: 700; color: #0F172A; margin-bottom: 0.75rem; border: none; padding: 0;">Need Something Similar Engineered for Your Business?</h2>
<p style="color: #334155; font-size: 1.05rem; margin-bottom: 1.5rem; max-width: 600px; margin-left: auto; margin-right: auto;">TENSIX builds custom business software, AI agents, and high-velocity automations at guaranteed fixed prices. You deal directly with Principal Architect Hemal Shah — 0 middlemen.</p>
<div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
<a class="cta-button primary" href="https://wa.me/918320278775?text=Hi%20Hemal%2C%20I%20read%20your%20article%20and%20would%20like%20to%20discuss%20a%20project." target="_blank" rel="noopener" style="padding: 0.8rem 2rem; font-size: 1rem; display: inline-flex; align-items: center; gap: 0.5rem;">Chat on WhatsApp Direct ↗</a>
<a class="cta-button secondary" href="/contact" style="padding: 0.8rem 2rem; font-size: 1rem;">Get a Fixed-Price Plan →</a>
</div>
</div>
'''

for path in missing_blogs:
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Insert right before </article> or before mesh-service-callout
    if '<div class="mesh-service-callout"' in html:
        html = html.replace('<div class="mesh-service-callout"', cta_block + '\n<div class="mesh-service-callout"', 1)
    elif '</article>' in html:
        html = html.replace('</article>', cta_block + '\n</article>', 1)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Added Commercial Action Box to: {os.path.basename(path)}")
