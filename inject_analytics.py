import os
import re
from pathlib import Path

ROOT_DIR = Path(r"H:\portfolio_website\hemalshah")

GA_TAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RJMCZXJ18Y"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-RJMCZXJ18Y');
</script>
"""

def inject_analytics():
    updated = 0
    skipped = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in {
            'assets', 'node_modules', '.git', 'aeo_geo_pages', 'hk', '__pycache__', 'test-results', 'playwright-report'
        }]

        for file in files:
            if not file.endswith(".html"):
                continue
            
            if file.startswith("google") or file.startswith("rajputbhavin"):
                continue

            fp = Path(root) / file
            try:
                content = fp.read_text(encoding="utf-8", errors="ignore")
            except Exception as e:
                print(f"Error reading {fp}: {e}")
                continue

            # 1. Strip all existing GA tags completely so we don't have duplicates
            content = re.sub(
                r'<!-- Google tag \(gtag\.js\) -->\s*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-RJMCZXJ18Y"></script>\s*<script>\s*window\.dataLayer = window\.dataLayer \|\| \[\];\s*function gtag\(\)\{dataLayer\.push\(arguments\);\}\s*gtag\(\'js\', new Date\(\)\);\s*gtag\(\'config\', \'G-RJMCZXJ18Y\'\);\s*</script>\s*',
                '', content, flags=re.IGNORECASE|re.DOTALL
            )

            # 2. Inject immediately AFTER the opening <head> tag
            # Find <head> or <head ...>
            head_match = re.search(r'<head[^>]*>', content, re.IGNORECASE)
            
            if head_match:
                head_end_pos = head_match.end()
                content = content[:head_end_pos] + "\n" + GA_TAG + content[head_end_pos:]
                fp.write_text(content, encoding="utf-8")
                print(f"✅ Injected GA immediately after <head> in {fp.relative_to(ROOT_DIR)}")
                updated += 1
            else:
                print(f"⚠️ Warning: No <head> tag found in {fp.relative_to(ROOT_DIR)}")

    print(f"\n🚀 Done! Re-positioned Google Analytics into {updated} pages.")

if __name__ == "__main__":
    inject_analytics()
