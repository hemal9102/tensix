import os
import re
import glob

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Update :root variables
    content = content.replace(
        "--color-bg:#0F172A;",
        "--color-bg:#090A0F;"
    )
    content = content.replace(
        "--color-bg-light:#1e293b;",
        "--color-bg-light:#0F121C;"
    )
    content = content.replace(
        "--color-bg-card:rgba(255,255,255,0.05);",
        "--color-bg-card:rgba(255,255,255,0.035);"
    )
    content = content.replace(
        "--color-text:#e2e8f0;",
        "--color-text:#F8FAFC;"
    )
    content = content.replace(
        "--color-text-muted:#aab6c8;",
        "--color-text-muted:#94A3B8;"
    )

    # 2. Update gradient-text to Swiss Platinum & Electric Cobalt Shimmer
    content = content.replace(
        "linear-gradient(90deg,#3b82f6 0%,#8b5cf6 35%,#ffd166 60%,#ff6b6b 80%,#3b82f6 100%)",
        "linear-gradient(90deg,#FFFFFF 0%,#CBD5E1 30%,#93C5FD 55%,#3B82F6 75%,#FFFFFF 100%)"
    )

    # 3. Update site header scrolled background
    content = content.replace(
        "site-header.scrolled{background:rgba(15,23,42,0.98);",
        "site-header.scrolled{background:rgba(9,10,15,0.96);border-bottom:1px solid rgba(255,255,255,0.08);"
    )

    # 4. Update site footer background
    content = content.replace(
        ".site-footer{background:#080d19;",
        ".site-footer{background:#06070A;border-top:1px solid rgba(255,255,255,0.08);"
    )

    # 5. Update hero background gradients
    content = content.replace(
        "background:linear-gradient(135deg,#0F172A 0%,rgba(76,0,255,0.25) 50%,#0F172A 100%);",
        "background:linear-gradient(180deg,#090A0F 0%,#0F121C 50%,#090A0F 100%);"
    )
    content = content.replace(
        "background:linear-gradient(135deg,#0F172A 0%,rgba(76,0,255,0.2) 100%);",
        "background:linear-gradient(180deg,#090A0F 0%,#0E111A 100%);"
    )

    # 6. Update floating dock
    content = content.replace(
        "background:rgba(15,23,42,0.88);",
        "background:rgba(12,14,21,0.92);border:1px solid rgba(255,255,255,0.12);"
    )

    # 7. Update nav-cta button to Swiss high-contrast architectural styling
    old_nav_cta = ".nav-cta{background:linear-gradient(135deg,#3b82f6,#8b5cf6) !important;color:#fff !important;font-weight:600 !important;box-shadow:0 0 12px rgba(59,130,246,0.35);border:1px solid rgba(255,255,255,0.1);padding:0.4rem 1.1rem !important;border-radius:0.5rem;transition:all 0.3s ease !important;}"
    new_nav_cta = ".nav-cta{background:#FFFFFF !important;color:#090A0F !important;font-weight:700 !important;box-shadow:0 0 16px rgba(255,255,255,0.25);border:1px solid rgba(255,255,255,0.2);padding:0.4rem 1.15rem !important;border-radius:0.5rem;transition:all 0.3s ease !important;}"
    content = content.replace(old_nav_cta, new_nav_cta)

    # 8. Update logo image tags to bust cache with v=2.0 and add rounded corners
    content = re.sub(
        r'<img alt="TENSIX Logo" class="logo-img"([^>]*?)src="assets/favicon\.webp[^"]*"',
        r'<img alt="TENSIX Swiss Logo" class="logo-img"\1src="assets/favicon.webp?v=2.0" style="border-radius:8px;"',
        content
    )
    content = re.sub(
        r'<img alt="TENSIX Logo" class="logo-img"([^>]*?)src="\.\./assets/favicon\.webp[^"]*"',
        r'<img alt="TENSIX Swiss Logo" class="logo-img"\1src="../assets/favicon.webp?v=2.0" style="border-radius:8px;"',
        content
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Applied Swiss theme to: {filepath}")
    else:
        print(f"No changes needed for: {filepath}")

# Process all root HTML files
root_files = glob.glob('*.html')
for f in root_files:
    update_file(f)

# Process all blog HTML files
blog_files = glob.glob('blogs/*.html')
for f in blog_files:
    update_file(f)

print("Swiss theme application complete!")
