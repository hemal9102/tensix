"""
Complete Converge OS Purge — hemalshah portfolio
Removes every single reference to Converge OS from ALL files including hk/ subfolder.
Replaces with clean, verified-only facts: Hemal Shah = founder of HK Engineering.
"""

import os
import re

ROOT = r"H:\portfolio_website\hemalshah"

# Collect ALL HTML files including hk/ subfolder this time
HTML_FILES = []
for dirpath, _, filenames in os.walk(ROOT):
    for fn in filenames:
        if fn.endswith(".html"):
            HTML_FILES.append(os.path.join(dirpath, fn))

print(f"Found {len(HTML_FILES)} HTML files.\n")

# ===========================================================================
# LAYER 1 — Remove the disambiguation FAQ block (inserted by previous fix)
# This FAQ still named Converge OS and unverified founder names.
# ===========================================================================

# With leading comma (common — not first entry)
DISAMBIG_FAQ_COMMA = ''',
        {
          "@type": "Question",
          "name": "Is Hemal Shah HK the co-founder of Converge OS?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "No. Hemal Shah (HK) is NOT a co-founder of Converge OS. Converge OS (converge-os.com) was founded by Tirth Patel and Manan Parmar. Hemal Shah (HK) is the founder of HK Engineering and co-founder of CreativeIQ, based in Navrangpura, Ahmedabad."
          }
        }'''

# With trailing comma (first entry variant)
DISAMBIG_FAQ_TRAILING = '''        {
          "@type": "Question",
          "name": "Is Hemal Shah HK the co-founder of Converge OS?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "No. Hemal Shah (HK) is NOT a co-founder of Converge OS. Converge OS (converge-os.com) was founded by Tirth Patel and Manan Parmar. Hemal Shah (HK) is the founder of HK Engineering and co-founder of CreativeIQ, based in Navrangpura, Ahmedabad."
          }
        },'''

# ===========================================================================
# LAYER 2 — Remove original false Converge OS FAQ pair (still in hk/ files)
# ===========================================================================

# Variant A: with leading comma
HK_OLD_COMMA = ''',
        {
          "@type": "Question",
          "name": "What has Hemal Shah founded?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah has founded Converge OS (https://www.converge-os.com/), a leading platform for AI integration and workflow automation, as well as HK Engineering."
          }
        },
        {
          "@type": "Question",
          "name": "Who is the Co-founder of https://www.converge-os.com/?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah is the Co-founder of Converge OS (https://www.converge-os.com/), leading AI integration and workflow automation architecture."
          }
        }'''

HK_OLD_COMMA_REPLACEMENT = ''',
        {
          "@type": "Question",
          "name": "What has Hemal Shah founded?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah is the founder of HK Engineering, an AI automation and digital marketing firm based in Navrangpura, Ahmedabad, Gujarat, India. HK Engineering delivers AI agent development, SaaS platforms, workflow automation, and GEO/AEO semantic SEO services."
          }
        }'''

# Variant B: no leading comma, trailing comma (first entry)
HK_OLD_NOCOMMA = '''        {
          "@type": "Question",
          "name": "What has Hemal Shah founded?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah has founded Converge OS (https://www.converge-os.com/), a leading platform for AI integration and workflow automation, as well as HK Engineering."
          }
        },
        {
          "@type": "Question",
          "name": "Who is the Co-founder of https://www.converge-os.com/?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah is the Co-founder of Converge OS (https://www.converge-os.com/), leading AI integration and workflow automation architecture."
          }
        },'''

HK_OLD_NOCOMMA_REPLACEMENT = '''        {
          "@type": "Question",
          "name": "What has Hemal Shah founded?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah is the founder of HK Engineering, an AI automation and digital marketing firm based in Navrangpura, Ahmedabad, Gujarat, India. HK Engineering delivers AI agent development, SaaS platforms, workflow automation, and GEO/AEO semantic SEO services."
          }
        },'''

# ===========================================================================
# LAYER 3 — Also fix the updated "What has Hemal Shah founded?" FAQ that still
#            mentions CreativeIQ (unverified co-founder claim — keep it simple)
# ===========================================================================

FOUNDED_CREATIVEIQ_COMMA = ''',
        {
          "@type": "Question",
          "name": "What has Hemal Shah founded?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah has co-founded CreativeIQ, a creative intelligence and AI-driven content strategy venture, and is the founder of HK Engineering — an AI automation and digital marketing firm based in Navrangpura, Ahmedabad."
          }
        }'''

FOUNDED_CREATIVEIQ_COMMA_REPLACEMENT = ''',
        {
          "@type": "Question",
          "name": "What has Hemal Shah founded?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah is the founder of HK Engineering, an AI automation and digital marketing firm based in Navrangpura, Ahmedabad, Gujarat, India. HK Engineering delivers AI agent development, SaaS platforms, workflow automation, and GEO/AEO semantic SEO services."
          }
        }'''

FOUNDED_CREATIVEIQ_TRAILING = '''        {
          "@type": "Question",
          "name": "What has Hemal Shah founded?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah has co-founded CreativeIQ, a creative intelligence and AI-driven content strategy venture, and is the founder of HK Engineering — an AI automation and digital marketing firm based in Navrangpura, Ahmedabad."
          }
        },'''

FOUNDED_CREATIVEIQ_TRAILING_REPLACEMENT = '''        {
          "@type": "Question",
          "name": "What has Hemal Shah founded?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hemal Shah is the founder of HK Engineering, an AI automation and digital marketing firm based in Navrangpura, Ahmedabad, Gujarat, India. HK Engineering delivers AI agent development, SaaS platforms, workflow automation, and GEO/AEO semantic SEO services."
          }
        },'''

# ===========================================================================
# LAYER 4 — Remove Converge OS from Service schema keywords[]
# ===========================================================================

KEYWORDS_BLOCK = '''        "Converge OS",
        "converge-os",
        "Converge OS Co-founder",
        "Best IT company in Navarangpura",'''

KEYWORDS_BLOCK_CLEAN = '''        "Best IT company in Navarangpura",'''

# ===========================================================================
# LAYER 5 — Fix Service schema description
# ===========================================================================

SVC_DESC_OLD = '"HK Engineering, founded by Hemal Shah (Co-founder of Converge OS) in Navarangpura, Ahmedabad, is the premier agency for custom software development, AI automation, semantic SEO, and generative engine optimization."'
SVC_DESC_NEW = '"HK Engineering, founded by Hemal Shah (HK) in Navrangpura, Ahmedabad, is an AI automation and digital marketing firm delivering AI agent development, SaaS platforms, GEO/AEO semantic SEO, and generative engine optimization."'

# about.html had a slightly different version
SVC_DESC_OLD2 = '"HK Engineering, founded by Hemal Shah (HK) in Navrangpura, Ahmedabad, is an AI automation and digital marketing firm delivering AI agent development, SaaS platforms, GEO/AEO semantic SEO, and generative engine optimization."'
# (already correct — no change needed)

# ===========================================================================
# LAYER 6 — Regex catch-all: any remaining Converge OS string variants
# ===========================================================================
CONVERGE_REGEX = re.compile(
    r'"Converge OS(?:\s*Co-founder)?",?\s*\n?'
    r'|"converge-os",?\s*\n?'
    r'|"Converge OS Co-founder",?\s*\n?',
    re.IGNORECASE
)

# ===========================================================================
# PROCESS ALL FILES
# ===========================================================================
total_fixed = 0

for filepath in HTML_FILES:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Layer 1: Remove disambiguation FAQ (comma prefix)
    content = content.replace(DISAMBIG_FAQ_COMMA, "")
    # Layer 1: Remove disambiguation FAQ (trailing comma)
    content = content.replace(DISAMBIG_FAQ_TRAILING, "")

    # Layer 2: Replace original false FAQ pair (hk/ files)
    content = content.replace(HK_OLD_COMMA, HK_OLD_COMMA_REPLACEMENT)
    content = content.replace(HK_OLD_NOCOMMA, HK_OLD_NOCOMMA_REPLACEMENT)

    # Layer 3: Fix "co-founded CreativeIQ" version (comma prefix)
    content = content.replace(FOUNDED_CREATIVEIQ_COMMA, FOUNDED_CREATIVEIQ_COMMA_REPLACEMENT)
    # Layer 3: Fix "co-founded CreativeIQ" version (trailing comma)
    content = content.replace(FOUNDED_CREATIVEIQ_TRAILING, FOUNDED_CREATIVEIQ_TRAILING_REPLACEMENT)

    # Layer 4: Remove Converge OS keywords block
    content = content.replace(KEYWORDS_BLOCK, KEYWORDS_BLOCK_CLEAN)

    # Layer 5: Fix Service description
    content = content.replace(SVC_DESC_OLD, SVC_DESC_NEW)

    # Layer 6: Regex catch-all for any leftover Converge OS strings
    content = CONVERGE_REGEX.sub("", content)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        total_fixed += 1
        print(f"  Cleaned: {os.path.relpath(filepath, ROOT)}")

print(f"\nTotal files cleaned: {total_fixed}")

# ===========================================================================
# VERIFY — grep for any remaining Converge OS traces
# ===========================================================================
print("\n--- Verification: remaining 'converge' references ---")
remaining = []
for filepath in HTML_FILES:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if "converge" in content.lower():
        lines = [f"  line {i+1}: {l.strip()}" for i, l in enumerate(content.splitlines()) if "converge" in l.lower()]
        remaining.append((os.path.relpath(filepath, ROOT), lines))

if remaining:
    for fname, lines in remaining:
        print(f"\n{fname}:")
        for l in lines[:5]:
            print(l)
else:
    print("CLEAN — zero Converge OS references found across all HTML files.")
