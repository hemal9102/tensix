import os
import re

root_dir = r"H:\portfolio_website\hemalshah"
html_files = [f for f in os.listdir(root_dir) if f.endswith('.html') and not f.startswith('google')]

new_cta_and_footer = """  <!-- ── CTA / Contact Banner ───────────────── -->
  <section class="section" style="background:linear-gradient(135deg,rgba(59,130,246,0.08),rgba(139,92,246,0.08)); border-top: 1px solid rgba(255,255,255,0.05);">
    <div class="section-inner text-center">
      <h2 class="section-title reveal" style="font-size:2rem;font-weight:700;color:#fff;margin-bottom:1rem;">
        Ready to build your next <span class="gradient-text">AI Agent</span> or <span class="gradient-text">Automation</span>?
      </h2>
      <p class="reveal reveal-delay-1" style="color:var(--color-text-muted);margin-bottom:2rem;max-width:600px;margin-left:auto;margin-right:auto;">
        Let's work together to build custom workflows, RAG tools, and full-stack solutions. Drop me a line right away!
      </p>
      <div class="hero-buttons reveal reveal-delay-2">
        <a href="index.html#contact" class="cta-button primary">Hire Me Instantly</a>
        <a href="contact.html" class="cta-button secondary">Custom Form</a>
      </div>
    </div>
  </section>

  <!-- ── Footer ─────────────────────────────── -->
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <a href="index.html" class="logo"><img src="assets/favicon.png" alt="HK Engineering" class="logo-img" width="36" height="36" /></a>
        <p>Founder, HK Engineering | Co-Founder, CreativeIQ | AI Agent & Full-Stack Python Engineer</p>
      </div>
      <nav class="footer-nav">
        <h3>Navigate</h3>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="work.html">Work</a></li>
          <li><a href="services.html">Skills</a></li>
          <li><a href="blogs.html">Blog</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </nav>
      <nav class="footer-nav" aria-label="Resources navigation">
        <h3>Resources</h3>
        <ul>
          <li><a href="resources.html">AI Resources</a></li>
          <li><a href="compare.html">Comparisons</a></li>
          <li><a href="frameworks.html">Proprietary Frameworks</a></li>
        </ul>
      </nav>
      <div class="footer-social">
        <h3>Connect</h3>
        <div class="social-row">
          <a class="social-btn" href="https://github.com/hemal9102" target="_blank" rel="noopener" aria-label="GitHub">
            <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.21 11.39.6.11.79-.26.79-.58v-2.23c-3.34.73-4.03-1.42-4.03-1.42-.55-1.39-1.33-1.76-1.33-1.76-1.09-.74.08-.73.08-.73 1.2.08 1.84 1.24 1.84 1.24 1.07 1.83 2.81 1.3 3.49 1 .11-.78.42-1.3.76-1.6-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.52.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.29-1.55 3.3-1.23 3.3-1.23.66 1.66.24 2.88.12 3.18.77.84 1.24 1.91 1.24 3.22 0 4.61-2.81 5.63-5.48 5.92.43.37.82 1.1.82 2.22v3.29c0 .32.19.69.8.58A12 12 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
          </a>
          <a class="social-btn" href="https://www.linkedin.com/in/hemal-shah-49a728362/" target="_blank" rel="noopener" aria-label="LinkedIn">
            <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zm1.78 13.02H3.56V9h3.56v11.45zM22.23 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.46c.98 0 1.77-.77 1.77-1.73V1.73C24 .77 23.21 0 22.23 0z"/></svg>
          </a>
          <a class="social-btn" href="https://www.instagram.com/hemall_9/" target="_blank" rel="noopener" aria-label="Instagram">
            <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M7.75 2h8.5A5.75 5.75 0 0 1 22 7.75v8.5A5.75 5.75 0 0 1 16.25 22h-8.5A5.75 5.75 0 0 1 2 16.25v-8.5A5.75 5.75 0 0 1 7.75 2zm0 1.5A4.25 4.25 0 0 0 3.5 7.75v8.5A4.25 4.25 0 0 0 7.75 20.5h8.5a4.25 4.25 0 0 0 4.25-4.25v-8.5A4.25 4.25 0 0 0 16.25 3.5h-8.5zm4.25 3.25a5.25 5.25 0 1 1 0 10.5 5.25 5.25 0 0 1 0-10.5zm0 1.5a3.75 3.75 0 1 0 0 7.5 3.75 3.75 0 0 0 0-7.5zm5.75-.5a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>
          </a>
          <a class="social-btn" href="mailto:hemal.shah2004@gmail.com" aria-label="Email">
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
          </a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 Hemal Shah · AI Engineer<br>HK Engineering · Navrangpura Local Hub HK Engineering Navrangpura (Local Hub) Hemal Shah (AI Engineer Profile)</p>
    </div>
  </footer>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js"></script>
  <script src="script.js"></script>
</body>
</html>"""

schema_template = """  <!-- JSON-LD Structured Data for SEO & LLMs -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "{title}",
    "description": "{description}",
    "url": "https://hemalshah.vercel.app/{file_name}",
    "publisher": {
      "@type": "Organization",
      "name": "HK Engineering",
      "logo": {
        "@type": "ImageObject",
        "url": "https://hemalshah.vercel.app/assets/favicon.png"
      }
    }
  }
  </script>
"""

keywords_meta = '  <meta name="keywords" content="Hemal Shah, HK, Hemal Shah HK, HK Engineering, AI Engineer, Python Developer, SEO Automation, AI Automation" />'

for file_name in html_files:
    file_path = os.path.join(root_dir, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    original_content = content
    
    # 1. FIX FOOTER
    # Replace footer + scripts + end tags
    # Also strip out any existing CTA banner
    content = re.sub(r'<!-- ── CTA / Contact Banner ───────────────── -->\s*<section class="section" style="background:linear-gradient.*?</section>', '', content, flags=re.DOTALL)
    # Note: for contact.html maybe we don't want the CTA? Actually the CTA is fine on all pages. Let's just add it.
    if file_name == 'contact.html':
        # Remove CTA just for contact page
        custom_footer = new_cta_and_footer.split('<!-- ── Footer ─────────────────────────────── -->')[1]
        custom_footer = '<!-- ── Footer ─────────────────────────────── -->\n' + custom_footer
        content = re.sub(r'<footer class="site-footer">.*', custom_footer, content, flags=re.DOTALL)
    else:
        content = re.sub(r'<footer class="site-footer">.*', new_cta_and_footer, content, flags=re.DOTALL)
        
    # 2. FIX JSON-LD & META TAGS
    # Extract Title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1).split("–")[0].split("|")[0].strip() if title_match else "Page"
    
    # Extract Description
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
    desc = desc_match.group(1) if desc_match else ""
    
    if "application/ld+json" not in content:
        head_end_idx = content.find("</head>")
        if head_end_idx != -1:
            schema_filled = schema_template.replace("{title}", title).replace("{description}", desc).replace("{file_name}", file_name)
            injection = f"{keywords_meta}\n{schema_filled}"
            content = content[:head_end_idx] + injection + content[head_end_idx:]

    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {file_name}")
