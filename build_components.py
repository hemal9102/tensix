#!/usr/bin/env python3
"""
TENSIX Static Component Builder
Injects reusable modular components (_head_common.html, _header.html, _footer.html)
into static HTML files using marker tags (<!-- @include name --> ... <!-- @endinclude -->).

Preserves:
- Page-specific titles, meta descriptions, canonicals, og/twitter tags, and JSON-LD schema graphs.
- Active navigation states on the header per section.
"""

import os
import re
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
COMPONENTS_DIR = os.path.join(ROOT_DIR, "components")

HEAD_COMMON_FILE = os.path.join(COMPONENTS_DIR, "_head_common.html")
HEADER_FILE = os.path.join(COMPONENTS_DIR, "_header.html")
FOOTER_FILE = os.path.join(COMPONENTS_DIR, "_footer.html")

def load_components():
    with open(HEAD_COMMON_FILE, "r", encoding="utf-8") as f:
        head_common = f.read().strip()
    with open(HEADER_FILE, "r", encoding="utf-8") as f:
        header_template = f.read().strip()
    with open(FOOTER_FILE, "r", encoding="utf-8") as f:
        footer = f.read().strip()
    return head_common, header_template, footer

def get_html_pages():
    pages = []
    for dirpath, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in ("hk", "skills", "resources", "assets", "node_modules", ".git", "09_Archive", "components")]
        for fname in files:
            if fname.endswith(".html") and not fname.startswith("google") and not fname.startswith("rajputbhavin"):
                pages.append(os.path.join(dirpath, fname))
    return sorted(pages)

def get_active_nav(rel_path):
    # Determines active class for header navigation
    rel = rel_path.replace("\\", "/")
    nav_keys = {
        "NAV_HOME_ACTIVE": "",
        "NAV_ABOUT_ACTIVE": "",
        "NAV_WORK_ACTIVE": "",
        "NAV_SERVICES_ACTIVE": "",
        "NAV_BLOGS_ACTIVE": ""
    }
    if rel == "index.html":
        nav_keys["NAV_HOME_ACTIVE"] = "active"
    elif rel == "about.html":
        nav_keys["NAV_ABOUT_ACTIVE"] = "active"
    elif rel in ("work.html", "case-studies.html", "gallery.html"):
        nav_keys["NAV_WORK_ACTIVE"] = "active"
    elif rel.startswith("services/") or rel == "services.html":
        nav_keys["NAV_SERVICES_ACTIVE"] = "active"
    elif rel.startswith("blogs/") or rel == "blogs.html":
        nav_keys["NAV_BLOGS_ACTIVE"] = "active"
    return nav_keys

def render_header(header_template, rel_path):
    active_map = get_active_nav(rel_path)
    res = header_template
    for key, val in active_map.items():
        res = res.replace("{{" + key + "}}", val)
    # clean extra space if class=""
    res = res.replace('class="" ', '').replace('class=""', '')
    return res

def process_file(file_path, head_common, header_template, footer):
    rel_path = os.path.relpath(file_path, ROOT_DIR)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # 1. HEAD COMMON
    # If marker exists, replace between markers; otherwise wrap existing common tags
    head_include_pat = r"<!-- @include head_common -->.*?<!-- @endinclude -->"
    if re.search(head_include_pat, content, re.DOTALL):
        new_block = f"<!-- @include head_common -->\n{head_common}\n<!-- @endinclude -->"
        content = re.sub(head_include_pat, new_block, content, flags=re.DOTALL)
        modified = True
    else:
        # Find Google tag through tensix.css and wrap
        raw_head_match = re.search(r"(<!-- Google tag \(gtag\.js\) -->.*?<link rel=\"stylesheet\" href=\"[^\"]*tensix\.css\?v=[^\"]*\"/>)", content, re.DOTALL)
        if raw_head_match:
            wrapped = f"<!-- @include head_common -->\n{head_common}\n<!-- @endinclude -->"
            content = content[:raw_head_match.start()] + wrapped + content[raw_head_match.end():]
            modified = True

    # 2. HEADER
    rendered_header = render_header(header_template, rel_path)
    header_include_pat = r"<!-- @include header -->.*?<!-- @endinclude -->"
    if re.search(header_include_pat, content, re.DOTALL):
        new_block = f"<!-- @include header -->\n{rendered_header}\n<!-- @endinclude -->"
        content = re.sub(header_include_pat, new_block, content, flags=re.DOTALL)
        modified = True
    else:
        raw_header_match = re.search(r"<header\b[^>]*>.*?</header>", content, re.DOTALL)
        if raw_header_match:
            wrapped = f"<!-- @include header -->\n{rendered_header}\n<!-- @endinclude -->"
            content = content[:raw_header_match.start()] + wrapped + content[raw_header_match.end():]
            modified = True

    # 3. FOOTER
    footer_include_pat = r"<!-- @include footer -->.*?<!-- @endinclude -->"
    if re.search(footer_include_pat, content, re.DOTALL):
        new_block = f"<!-- @include footer -->\n{footer}\n<!-- @endinclude -->"
        content = re.sub(footer_include_pat, new_block, content, flags=re.DOTALL)
        modified = True
    else:
        raw_footer_match = re.search(r"<footer\b[^>]*>.*?</footer>", content, re.DOTALL)
        if raw_footer_match:
            wrapped = f"<!-- @include footer -->\n{footer}\n<!-- @endinclude -->"
            content = content[:raw_footer_match.start()] + wrapped + content[raw_footer_match.end():]
            modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def main():
    print("=" * 60)
    print("  TENSIX Component Builder & Synchronizer")
    print("=" * 60)
    
    head_common, header_template, footer = load_components()
    pages = get_html_pages()
    print(f"[INFO] Loaded components. Processing {len(pages)} HTML pages...")

    updated_count = 0
    for page in pages:
        rel = os.path.relpath(page, ROOT_DIR).replace("\\", "/")
        if process_file(page, head_common, header_template, footer):
            updated_count += 1
            print(f"  [OK] Synchronized: {rel}")
        else:
            print(f"  [SKIP] Unchanged or unmapped: {rel}")

    print("=" * 60)
    print(f"[COMPLETED] Successfully synchronized {updated_count}/{len(pages)} pages.")
    print("=" * 60)

if __name__ == "__main__":
    main()
