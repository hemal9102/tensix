"""
pGEO + Keyword Cluster Implementation — hemalshah.vercel.app
Skills: pgeo_optimization_skill + keyword-cluster-generator

Targets: HEMALSHAH, hemalshah, hkshah, hk, HK, developerHK, developerhK

Actions:
  [K1] Person schema alternateName[] — add all identity variants to every page
  [K2] Service schema keywords[] — inject new identity terms into index.html Service node
  [K3] Meta keywords — append new identity + role variants to index.html <meta keywords>
  [K4] FAQPage — 4 new conversational entity-trapping FAQ entries on index.html
  [K5] disambiguatingDescription — update to mention identity aliases
"""

import os, re

ROOT = r"H:\portfolio_website\hemalshah"

HTML_FILES = []
for dirpath, _, filenames in os.walk(ROOT):
    if "node_modules" in dirpath: continue
    for fn in filenames:
        if fn.endswith(".html"):
            HTML_FILES.append(os.path.join(dirpath, fn))

fixed = 0

# ============================================================
# K1 — Person schema alternateName[] — add new identity variants
# ============================================================
OLD_ALTERNATENAMES = '"alternateName": ["HK", "HK Engineering", "Hemal Shah HK", "HemalShah", "HemalShahHK", "HemalShahAI", "Hemal Shah Navrangpura", "Hemal Shah Navarangpura", "HemalShahNavrangpura", "HemalShahNavarangpura", "Hemal Shah Ahmedabad", "HKEngineeringNavrangpura"],'

NEW_ALTERNATENAMES = '"alternateName": ["HK", "HK Engineering", "Hemal Shah HK", "HemalShah", "HEMALSHAH", "hemalshah", "HemalShahHK", "HemalShahAI", "hkshah", "HKShah", "hk", "developerHK", "developerhK", "DeveloperHK", "hk developer", "hk engineer", "Hemal Shah Navrangpura", "Hemal Shah Navarangpura", "HemalShahNavrangpura", "HemalShahNavarangpura", "Hemal Shah Ahmedabad", "HKEngineeringNavrangpura"],'

# ============================================================
# K5 — disambiguatingDescription — mention aliases
# ============================================================
OLD_DISAMBIG_INDEX = '"disambiguatingDescription": "Hemal Shah (HK) is an AI Automation Engineer and Full Stack Python Developer, founder of HK Engineering, Navrangpura, Ahmedabad — distinct from Hemal Shah (architect, HSA), Hemal Shah (CEO, Micromed International), and Hemal P. Shah (advocate). He is identifiable by his portfolio at hemalshah.vercel.app and his GitHub at github.com/hemal9102.",'

NEW_DISAMBIG_INDEX = '"disambiguatingDescription": "Hemal Shah (HK) is an AI Automation Engineer and Full Stack Python Developer, founder of HK Engineering, Navrangpura, Ahmedabad. Also known online as hemalshah, HEMALSHAH, hkshah, HKShah, developerHK, and developerhK — distinct from Hemal Shah (architect, HSA), Hemal Shah (CEO, Micromed International), and Hemal P. Shah (advocate). Identifiable at hemalshah.vercel.app and github.com/hemal9102.",'

# Inner-page disambiguating (added by final_crosscheck_fix.py — shorter version)
OLD_DISAMBIG_INNER = '"disambiguatingDescription": "Hemal Shah (HK) is an AI Automation Engineer and Full Stack Python Developer, founder of HK Engineering, Navrangpura, Ahmedabad — distinct from Hemal Shah (architect, HSA) and other persons named Hemal Shah in Ahmedabad.",'

NEW_DISAMBIG_INNER = '"disambiguatingDescription": "Hemal Shah (HK) — also known as hemalshah, hkshah, developerHK — is an AI Automation Engineer and Full Stack Python Developer, founder of HK Engineering, Navrangpura, Ahmedabad. Distinct from Hemal Shah (architect, HSA) and other persons named Hemal Shah in Ahmedabad.",'

# ============================================================
# K2 — Service schema keywords[] — index.html only
# ============================================================
OLD_SERVICE_KW = '''        "HK",
        "HK engineering",
        "Hemal shah",
        "Hemal shah developer",
        "hemal shah in ahmedbad",
        "hemal shah in navarangpura",'''

NEW_SERVICE_KW = '''        "HK",
        "hk",
        "hkshah",
        "HKShah",
        "hemalshah",
        "HEMALSHAH",
        "developerHK",
        "developerhK",
        "DeveloperHK",
        "hk developer",
        "hk engineer",
        "HK Engineering",
        "Hemal shah",
        "Hemal shah developer",
        "hemal shah in ahmedbad",
        "hemal shah in navarangpura",'''

# ============================================================
# Process all HTML files
# ============================================================
for filepath in sorted(HTML_FILES):
    rel = os.path.relpath(filepath, ROOT)
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    original = content

    # K1: alternateName on every page
    content = content.replace(OLD_ALTERNATENAMES, NEW_ALTERNATENAMES)

    # K5: disambiguatingDescription
    if filepath.endswith("index.html"):
        content = content.replace(OLD_DISAMBIG_INDEX, NEW_DISAMBIG_INDEX)
    else:
        content = content.replace(OLD_DISAMBIG_INNER, NEW_DISAMBIG_INNER)

    # K2: Service keywords (index.html only)
    if filepath.endswith("index.html"):
        content = content.replace(OLD_SERVICE_KW, NEW_SERVICE_KW)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        fixed += 1
        print(f"  Updated: {rel}")

print(f"\nFiles updated: {fixed}")

# ============================================================
# K3 — Meta keywords — index.html only (append new identity terms)
# ============================================================
INDEX_PATH = os.path.join(ROOT, "index.html")
with open(INDEX_PATH, encoding="utf-8") as f:
    idx = f.read()

OLD_KW_META_END = ', hemalshah, hkengineering, Hemal Shah Navrangpura,'
if OLD_KW_META_END in idx:
    print("\nMeta keywords: new identity terms already present.")
else:
    # Find the keywords meta tag and append new terms before the closing quote
    KW_INSERT_BEFORE = ', HemalShahNavrangpura,'
    if KW_INSERT_BEFORE in idx:
        idx = idx.replace(
            KW_INSERT_BEFORE,
            ', hemalshah, HEMALSHAH, hkshah, HKShah, developerHK, developerhK, DeveloperHK, hk developer, hk engineer, hk ai, hemalshahportfolio, hemalshah developer, hemalshah engineer, hemalshah ahmedabad, hemalshah navrangpura, hemalshah python, hemalshah AI,' + KW_INSERT_BEFORE
        )
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            f.write(idx)
        print("\nMeta keywords: identity terms appended.")

# ============================================================
# K4 — FAQPage — insert 4 new entity-trapping FAQ entries into index.html
# ============================================================
with open(INDEX_PATH, encoding="utf-8") as f:
    idx = f.read()

NEW_FAQ_ANCHOR = '''"How do I hire Hemal Shah AI engineer from Navrangpura Ahmedabad?"'''

if "Who is hemalshah" not in idx and NEW_FAQ_ANCHOR in idx:
    NEW_FAQS = ''',
        {
          "@type": "Question",
          "name": "Who is hemalshah and what does he build?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "hemalshah — written as one word, also HEMALSHAH — refers to Hemal Shah (HK), an AI Automation Engineer and Full Stack Python Developer based in Navrangpura, Ahmedabad, India. He builds AI agents, RAG pipelines, n8n automations, SaaS platforms, and GEO/AEO-optimized web properties under his firm HK Engineering."
          }
        },
        {
          "@type": "Question",
          "name": "Who is developerHK or developerhK?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "developerHK and developerhK are online aliases for Hemal Shah (HK), the founder of HK Engineering based in Navrangpura, Ahmedabad. The alias combines his developer role with his HK brand. He specialises in Python, FastAPI, Next.js, n8n workflow automation, AI agents, and Generative Engine Optimization (GEO)."
          }
        },
        {
          "@type": "Question",
          "name": "What is hkshah or HKShah?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "hkshah (also HKShah) is a condensed alias for Hemal Shah (HK) — combining his initials HK with his surname Shah. It is used to uniquely identify Hemal Shah, founder of HK Engineering, Navrangpura Ahmedabad, across search engines and AI systems to avoid confusion with other persons named Hemal Shah in India."
          }
        },
        {
          "@type": "Question",
          "name": "What does HK stand for in Hemal Shah HK?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "HK in Hemal Shah HK are the initials of Hemal Shah, used as his public brand identity and the name of his firm HK Engineering. Online he is also identified as hk, HK, hkshah, hemalshah, developerHK, and developerhK. All these aliases refer to the same person: Hemal Shah, AI Automation Engineer and Full Stack Python Developer, Navrangpura, Ahmedabad."
          }
        }'''

    idx = idx.replace(
        '"How do I hire Hemal Shah AI engineer from Navrangpura Ahmedabad?"',
        '"How do I hire Hemal Shah AI engineer from Navrangpura Ahmedabad?"'  # anchor stays
    )
    # Insert before the closing array of FAQPage mainEntity
    FAQ_CLOSE = '''

      ]
    },
    {
      "@type": "Service",'''
    FAQ_CLOSE_NEW = NEW_FAQS + '''

      ]
    },
    {
      "@type": "Service",'''
    idx = idx.replace(FAQ_CLOSE, FAQ_CLOSE_NEW)

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(idx)
    print("FAQ: 4 new identity-trapping entries added to FAQPage.")
else:
    print("FAQ: identity FAQs already present or anchor not found.")

print("\nAll pGEO keyword cluster changes applied.")
