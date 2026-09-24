import os
import re

blog_dir = r"H:\portfolio_website\hemalshah\blogs"

new_header_and_dock = """  <header class="site-header">
    <a href="../index.html" class="logo"><img src="../assets/favicon.png" alt="HK Engineering" class="logo-img" width="36" height="36" /></a>
    <nav class="nav" id="main-nav" aria-label="Main navigation">
      <ul>
        <li><a href="../index.html">Home</a></li>
        <li><a href="../about.html">About</a></li>
        <li><a href="../work.html">Work</a></li>
        <li><a href="../services.html">Skills</a></li>
        <li><a href="../blogs.html" class="active">Blog</a></li>
        <li><a href="../contact.html" class="nav-cta">Contact</a></li>
      </ul>
    </nav>
    <button class="nav-toggle" aria-controls="main-nav" aria-expanded="false" aria-label="Toggle navigation">
      <span></span><span></span><span></span>
    </button>
  </header>

  <!-- ── Floating Dock ──────────────────────── -->
  <nav class="floating-dock" aria-label="Quick navigation">
    <div class="dock-inner">
      <a class="dock-btn" href="../index.html" title="Home">
        <span class="dock-tooltip">Home</span>
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      </a>
      <a class="dock-btn" href="../blogs.html" title="Blog" style="color:#fff;background:rgba(59,130,246,0.15);">
        <span class="dock-tooltip">Blog</span>
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20"/><path d="M4 3v16.5"/><path d="M8 3h12v18H8z"/></svg>
      </a>
      <div class="dock-divider"></div>
      <a class="dock-btn" href="https://github.com/hemal9102" target="_blank" rel="noopener" title="GitHub">
        <span class="dock-tooltip">GitHub</span>
        <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.44 9.8 8.21 11.39.6.11.79-.26.79-.58v-2.23c-3.34.73-4.03-1.42-4.03-1.42-.55-1.39-1.33-1.76-1.33-1.76-1.09-.74.08-.73.08-.73 1.2.08 1.84 1.24 1.84 1.24 1.07 1.83 2.81 1.3 3.49 1 .11-.78.42-1.3.76-1.6-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.52.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.29-1.55 3.3-1.23 3.3-1.23.66 1.66.24 2.88.12 3.18.77.84 1.24 1.91 1.24 3.22 0 4.61-2.81 5.63-5.48 5.92.43.37.82 1.1.82 2.22v3.29c0 .32.19.69.8.58A12 12 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
      </a>
      <a class="dock-btn" href="https://www.linkedin.com/in/hemal-shah-49a728362/" target="_blank" rel="noopener" title="LinkedIn">
        <span class="dock-tooltip">LinkedIn</span>
        <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zm1.78 13.02H3.56V9h3.56v11.45zM22.23 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.46c.98 0 1.77-.77 1.77-1.73V1.73C24 .77 23.21 0 22.23 0z"/></svg>
      </a>
      <a class="dock-btn" href="mailto:hemal.shah2004@gmail.com" title="Email">
        <span class="dock-tooltip">Email</span>
        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
      </a>
    </div>
  </nav>"""

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
        <a href="../index.html#contact" class="cta-button primary">Hire Me Instantly</a>
        <a href="../contact.html" class="cta-button secondary">Custom Form</a>
      </div>
    </div>
  </section>

  <!-- ── Footer ─────────────────────────────── -->
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <a href="../index.html" class="logo"><img src="../assets/favicon.png" alt="HK Engineering" class="logo-img" width="36" height="36" /></a>
        <p>Founder, HK Engineering | Co-Founder, CreativeIQ | AI Agent & Full-Stack Python Engineer</p>
      </div>
      <nav class="footer-nav">
        <h3>Navigate</h3>
        <ul>
          <li><a href="../index.html">Home</a></li>
          <li><a href="../about.html">About</a></li>
          <li><a href="../work.html">Work</a></li>
          <li><a href="../services.html">Skills</a></li>
          <li><a href="../blogs.html">Blog</a></li>
          <li><a href="../contact.html">Contact</a></li>
        </ul>
      </nav>
      <nav class="footer-nav" aria-label="Resources navigation">
        <h3>Resources</h3>
        <ul>
          <li><a href="../resources.html">AI Resources</a></li>
          <li><a href="../compare.html">Comparisons</a></li>
          <li><a href="../frameworks.html">Proprietary Frameworks</a></li>
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

  <script src="../script.js"></script>
</body>
</html>"""


# Process all HTML files in blogs/ and subdirectories
for root, _, files in os.walk(blog_dir):
    for f in files:
        if f.endswith(".html"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                
            original_content = content
            
            # Subdir depth logic
            rel_path = os.path.relpath(path, blog_dir)
            depth = len(rel_path.split(os.sep)) - 1
            if depth > 0:
                # If we are in blogs/ai-engineering/..., we need ../../ instead of ../
                prefix = "../../"
            else:
                prefix = "../"
                
            header_dock_str = new_header_and_dock.replace("../", prefix)
            cta_footer_str = new_cta_and_footer.replace("../", prefix)

            # REPLACE HEADER + DOCK
            # Find everything from <header class="site-header"> to the end of <nav class="floating-dock">...</nav>
            # OR just </header> if no dock exists
            
            header_pattern = r'<header class="site-header">.*?</header>'
            dock_pattern = r'<!-- ── Floating Dock ──────────────────────── -->.*?<nav class="floating-dock".*?</nav>'
            
            # Remove old dock if exists
            content = re.sub(dock_pattern, "", content, flags=re.DOTALL)
            
            # Replace header with new header + dock
            content = re.sub(header_pattern, header_dock_str, content, flags=re.DOTALL)
            
            # REPLACE CTA + FOOTER
            # Find the footer and anything after it up to </body>
            footer_pattern = r'(?:<!-- ── CTA / Contact Banner ───────────────── -->)?\s*<section class="section" style="background:linear-gradient.*?</section>\s*<!-- ── Footer ─────────────────────────────── -->\s*<footer class="site-footer">.*?</footer>\s*<script src=.*?</script>\s*</body>\s*</html>'
            
            # Or just find <footer class="site-footer"> to the end of the document
            content = re.sub(r'<footer class="site-footer">.*', cta_footer_str, content, flags=re.DOTALL)
            
            # Make sure to remove any existing CTA banner that was just above the footer so we don't duplicate
            content = re.sub(r'<!-- ── CTA / Contact Banner ───────────────── -->\s*<section class="section" style="background:linear-gradient.*?</section>', '', content, flags=re.DOTALL)

            if content != original_content:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(content)
                print(f"Updated: {f}")
