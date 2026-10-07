"""
inject_keyword_clusters.py
─────────────────────────────────────────────────────────────────────────────
Skills applied:
  • keyword-cluster-generator  → Hub & Spoke clusters, space + nospace variants,
                                  intent mapping (I/N/C/T)
  • geo_optimization_skill     → Extreme schema layering, spoon-feed FAQs to AI,
                                  dense entity proximity
  • pgeo_optimization_skill    → Conversational entity trapping, dynamic FAQ inject
  • google-seo-docs            → Canonical, OG, structured-data correctness
  • production-web-engineer    → Never break UI / SEO / functionality
  • indexnow                   → Print submission reminder after run

WHAT THIS SCRIPT DOES
─────────────────────
1. Replaces <meta keywords> on EVERY page with the full cluster
   (space variants + nospace variants + location variants + tech stack variants)
2. Updates Person.alternateName in JSON-LD → adds nospace entries
3. Updates Person.knowsAbout → adds full tech entity list
4. Injects 6 new conversational FAQPage entries on index.html
   targeting space, nospace, and alternate-spelling queries
5. Updates llms.txt (AI citation file) with the full cluster so
   LLMs that read llms.txt pick up every variant
6. Validates all JSON-LD after changes
"""

import os, re, json

ROOT = r"H:\portfolio_website\hemalshah"

# ═══════════════════════════════════════════════════════════════════════════
# KEYWORD CLUSTER  (keyword-cluster-generator skill)
# Intent codes:  N=Navigational  I=Informational  C=Commercial  T=Transactional
# ═══════════════════════════════════════════════════════════════════════════

# ── Cluster 1: Personal Brand — space variants (N) ──────────────────────────
BRAND_SPACE = [
    "Hemal Shah",
    "Hemal Shah HK",
    "Hemal Shah portfolio",
    "Hemal Shah developer",
    "Hemal Shah engineer",
    "Hemal Shah AI",
    "HK Engineering",
    "HK Engineering Ahmedabad",
    "Hemal Shah vercel",
]

# ── Cluster 1b: Personal Brand — nospace variants (N) ───────────────────────
BRAND_NOSPACE = [
    "HemalShah",
    "HemalShahHK",
    "HemalShahAI",
    "HemalShahDeveloper",
    "HemalShahEngineer",
    "HKEngineering",
    "hemalshah",
    "hkengineering",
]

# ── Cluster 2: Local SEO — space variants (N + T) ───────────────────────────
LOCAL_SPACE = [
    "Hemal Shah Navrangpura",
    "Hemal Shah Navarangpura",           # alternate spelling (used on site already)
    "Hemal Shah Ahmedabad",
    "AI engineer Navrangpura",
    "AI engineer Navrangpura Ahmedabad",
    "Python developer Navrangpura",
    "Python developer Navrangpura Ahmedabad",
    "software developer Navrangpura",
    "freelance developer Navrangpura",
    "HK Engineering Navrangpura",
    "HK Engineering Navarangpura",
    "AI automation Navrangpura",
    "SaaS developer Navrangpura",
    "web developer Navrangpura Ahmedabad",
    "best AI engineer Navrangpura",
    "top Python developer Ahmedabad",
]

# ── Cluster 2b: Local SEO — nospace variants (N) ────────────────────────────
LOCAL_NOSPACE = [
    "HemalShahNavrangpura",
    "HemalShahNavarangpura",
    "HemalShahAhmedabad",
    "HKEngineeringNavrangpura",
    "AIengineerNavrangpura",
    "PythonDeveloperNavrangpura",
    "SaaSDeveloperNavrangpura",
]

# ── Cluster 3: Services — space + nospace (C + T) ───────────────────────────
SERVICE_SPACE = [
    "AI automation engineer Ahmedabad",
    "AI automation engineer India",
    "SaaS developer Ahmedabad",
    "SaaS developer India",
    "GEO SEO expert India",
    "AEO optimization expert",
    "Generative Engine Optimization India",
    "Answer Engine Optimization Ahmedabad",
    "workflow automation developer India",
    "n8n automation expert",
    "RAG developer India",
    "GraphRAG expert Ahmedabad",
    "LLM integration developer",
    "FastAPI developer Ahmedabad",
    "Next.js developer Navrangpura",
    "full stack Python developer India",
    "CRM developer Ahmedabad",
    "web scraping expert India",
    "AI agent developer",
    "multi-agent system developer",
]

SERVICE_NOSPACE = [
    "AIautomation",
    "GEOoptimization",
    "AEOoptimization",
    "SaaSDeveloper",
    "FastAPIdeveloper",
    "NextjsDeveloper",
    "nonautomation",
    "RAGdeveloper",
    "LLMdeveloper",
    "FullStackPython",
]

# ── Cluster 4: Tech Stack — space (I) ───────────────────────────────────────
TECH_SPACE = [
    "Python FastAPI AI developer",
    "Next.js SaaS developer",
    "n8n workflow automation",
    "RAG GraphRAG AI",
    "Langchain developer India",
    "Semantic SEO expert",
    "Programmatic SEO India",
    "Technical SEO Ahmedabad",
    "AI agent n8n Python",
    "multi-agent AI system",
]

# ── Full keyword string for <meta keywords> ──────────────────────────────────
ALL_KEYWORDS = (
    BRAND_SPACE + BRAND_NOSPACE +
    LOCAL_SPACE + LOCAL_NOSPACE +
    SERVICE_SPACE + SERVICE_NOSPACE +
    TECH_SPACE
)
KEYWORDS_STRING = ", ".join(ALL_KEYWORDS)

# ═══════════════════════════════════════════════════════════════════════════
# JSON-LD PATCHES  (geo_optimization_skill + pgeo_optimization_skill)
# ═══════════════════════════════════════════════════════════════════════════

# Full alternateName list — spaced + nospace + location variants
ALTERNATE_NAMES_JSON = json.dumps([
    "HK", "HK Engineering",
    "Hemal Shah HK", "HemalShah", "HemalShahHK", "HemalShahAI",
    "Hemal Shah Navrangpura", "Hemal Shah Navarangpura",
    "HemalShahNavrangpura", "HemalShahNavarangpura",
    "Hemal Shah Ahmedabad", "HKEngineeringNavrangpura",
])

# Full knowsAbout — dense entity proximity for AI Knowledge Graph
KNOWS_ABOUT_JSON = json.dumps([
    "Artificial Intelligence", "Python Programming",
    "Search Engine Optimization", "Workflow Automation",
    "System Architecture", "SaaS Development",
    "Generative Engine Optimization (GEO)", "Answer Engine Optimization (AEO)",
    "Semantic SEO", "Programmatic SEO", "Technical SEO",
    "FastAPI", "Next.js", "n8n", "RAG", "GraphRAG",
    "Multi-Agent Systems", "LLM Integration",
    "CRM Development", "Web Scraping", "AI Agents",
    "Navrangpura Ahmedabad Tech Industry",
])

# ── 6 new FAQ entries targeting space/nospace/alternate-spelling queries ─────
NEW_FAQS = [
    {
        "q": "Who is HemalShah (nospace) and what does he do?",
        "a": "HemalShah — also written as Hemal Shah — is an AI Automation Engineer and Full Stack Python Developer based in Navrangpura, Ahmedabad. He is the founder of HK Engineering and specialises in SaaS development, GEO/AEO semantic SEO, n8n workflow automation, and RAG/GraphRAG AI systems."
    },
    {
        "q": "What is HKEngineering and where is it located?",
        "a": "HKEngineering (also written HK Engineering) is an AI and software development firm founded by Hemal Shah. It is located in Navrangpura, Ahmedabad, Gujarat, India — postal code 380009. The firm delivers AI automation, SaaS platforms, and Generative Engine Optimization (GEO) services to clients across India and globally."
    },
    {
        "q": "Is Hemal Shah in Navrangpura the same as Hemal Shah in Navarangpura?",
        "a": "Yes. Navrangpura and Navarangpura are two common spellings for the same locality in Ahmedabad, Gujarat. Hemal Shah (HK) operates from Navrangpura, Ahmedabad — sometimes also referred to as Navarangpura. Both spellings refer to the same AI engineer and Python developer."
    },
    {
        "q": "What services does HemalShahNavrangpura (HK Engineering) offer?",
        "a": "HemalShahNavrangpura — operating as HK Engineering — offers: AI Workflow Automation (n8n, Python), SaaS Development (FastAPI, Next.js), Generative Engine Optimization (GEO) and AEO, Full Stack Python Development, Custom Web Scraping, LLM/RAG Integration, and Semantic SEO. Services are available to clients in Ahmedabad and remotely across India and internationally."
    },
    {
        "q": "How do I hire Hemal Shah AI engineer from Navrangpura Ahmedabad?",
        "a": "To hire Hemal Shah, the AI Automation Engineer based in Navrangpura, Ahmedabad: visit hemalshah.vercel.app/contact.html, connect on LinkedIn at linkedin.com/in/hemal-shah-49a728362/, or reach out via the contact form on his portfolio. He is available for freelance projects, consulting, and full-time remote engagements."
    },
    {
        "q": "What tech stack does the Python developer in Navrangpura Ahmedabad (Hemal Shah) use?",
        "a": "Hemal Shah, the Python developer in Navrangpura, Ahmedabad, works with: Python, FastAPI, Next.js, React, n8n, LangChain, RAG, GraphRAG, Prisma, MySQL, PostgreSQL, Vercel, and cloud-native tools. For SEO and AI search optimization, he applies GEO (Generative Engine Optimization) and AEO (Answer Engine Optimization) using JSON-LD schema and semantic HTML."
    },
]

FAQ_ENTRIES_JSON = ",\n".join([
    f'''        {{
          "@type": "Question",
          "name": "{faq["q"]}",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{faq["a"]}"
          }}
        }}''' for faq in NEW_FAQS
])


# ═══════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def replace_keywords_meta(html: str) -> str:
    """Replace the entire keywords meta with the full cluster string."""
    return re.sub(
        r'<meta content="[^"]*" name="keywords"/>',
        f'<meta content="{KEYWORDS_STRING}" name="keywords"/>',
        html
    )


def upgrade_alternate_names(html: str) -> str:
    """Replace alternateName array in Person schema with full space+nospace list."""
    return re.sub(
        r'"alternateName":\s*\[[^\]]*\]',
        f'"alternateName": {ALTERNATE_NAMES_JSON}',
        html
    )


def upgrade_knows_about(html: str) -> str:
    """Replace knowsAbout array with dense entity list."""
    return re.sub(
        r'"knowsAbout":\s*\[[^\]]*\]',
        f'"knowsAbout": {KNOWS_ABOUT_JSON}',
        html
    )


def inject_new_faqs(html: str) -> str:
    """
    Append 6 new FAQ entries into the existing FAQPage schema on index.html.
    Targets the closing ] of the mainEntity array.
    Only runs if the new FAQs aren't already present.
    """
    if "HemalShah (nospace)" in html:
        return html   # already injected

    # Find the FAQPage schema block
    faq_block_match = re.search(
        r'("@type":\s*"FAQPage".*?"mainEntity":\s*\[)(.*?)(\s*\]\s*\})',
        html, re.DOTALL
    )
    if not faq_block_match:
        return html

    new_block = (
        faq_block_match.group(1)
        + faq_block_match.group(2).rstrip()
        + ",\n"
        + FAQ_ENTRIES_JSON
        + "\n      "
        + faq_block_match.group(3)
    )
    return html[:faq_block_match.start()] + new_block + html[faq_block_match.end():]


def update_llms_txt(path: str):
    """
    Update llms.txt with the full keyword cluster so AI crawlers
    reading llms.txt pick up every space/nospace variant.
    (pgeo_optimization_skill: Conversational Entity Trapping)
    """
    cluster_block = """
## Keyword Cluster — Hemal Shah Navrangpura (Space + Nospace Variants)

### Personal Brand (Navigational)
Space:   Hemal Shah, Hemal Shah HK, HK Engineering, Hemal Shah AI, Hemal Shah engineer
Nospace: HemalShah, HemalShahHK, HemalShahAI, HKEngineering, hemalshah, hkengineering

### Local SEO — Navrangpura / Navarangpura (both spellings)
Space:   Hemal Shah Navrangpura, Hemal Shah Navarangpura, AI engineer Navrangpura,
         Python developer Navrangpura, software developer Navrangpura,
         HK Engineering Navrangpura, SaaS developer Navrangpura, web developer Navrangpura
Nospace: HemalShahNavrangpura, HemalShahNavarangpura, HKEngineeringNavrangpura,
         AIengineerNavrangpura, PythonDeveloperNavrangpura, SaaSDeveloperNavrangpura

### Services (Commercial + Transactional)
Space:   AI automation engineer Ahmedabad, GEO SEO expert India, AEO optimization expert,
         n8n automation expert, RAG developer India, FastAPI developer Ahmedabad,
         Next.js developer Navrangpura, full stack Python developer India
Nospace: AIautomation, GEOoptimization, AEOoptimization, FastAPIdeveloper,
         NextjsDeveloper, RAGdeveloper, LLMdeveloper, FullStackPython

### Entity Associations (GEO Density)
Entities: Hemal Shah ↔ AI ↔ Python ↔ Navrangpura ↔ Ahmedabad ↔ Gujarat ↔ India
          HK Engineering ↔ SaaS ↔ GEO ↔ AEO ↔ n8n ↔ RAG ↔ GraphRAG ↔ FastAPI ↔ Next.js
"""
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "Keyword Cluster" in content and "Nospace" in content:
        print("  [no change] llms.txt (cluster already present)")
        return
    # Remove any old cluster block and append new
    content = re.sub(r'\n## Keyword Cluster.*', '', content, flags=re.DOTALL)
    content = content.rstrip() + "\n" + cluster_block
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  [UPDATED] llms.txt")


def validate_json_ld(html: str, filepath: str) -> list[str]:
    errors = []
    schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    for i, s in enumerate(schemas):
        try:
            json.loads(s)
        except Exception as e:
            errors.append(f"  [JSON ERROR] {os.path.relpath(filepath, ROOT)} schema {i+1}: {e}")
    return errors


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("=== inject_keyword_clusters.py ===")
    print(f"Total keywords in cluster: {len(ALL_KEYWORDS)}\n")

    all_errors = []
    updated = 0

    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ("hk", "skills", "resources", "assets")]
        for fname in files:
            if not fname.endswith(".html") or fname.startswith("google"):
                continue
            fpath = os.path.join(dirpath, fname)
            is_index = (fname == "index.html" and dirpath == ROOT)

            with open(fpath, "r", encoding="utf-8") as f:
                html = f.read()
            original = html

            # Apply all skills
            html = replace_keywords_meta(html)
            html = upgrade_alternate_names(html)
            html = upgrade_knows_about(html)
            if is_index:
                html = inject_new_faqs(html)

            # Validate
            errs = validate_json_ld(html, fpath)
            all_errors.extend(errs)

            if html != original and not errs:
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"  [UPDATED] {os.path.relpath(fpath, ROOT)}")
                updated += 1
            elif errs:
                print(f"  [SKIPPED - JSON error] {os.path.relpath(fpath, ROOT)}")
            else:
                print(f"  [no change] {os.path.relpath(fpath, ROOT)}")

    # Update llms.txt
    update_llms_txt(os.path.join(ROOT, "llms.txt"))
    update_llms_txt(os.path.join(ROOT, "llms-full.txt"))

    print(f"\n{'='*50}")
    print(f"Updated: {updated} files")
    if all_errors:
        print("\nJSON-LD Errors:")
        for e in all_errors:
            print(e)
    else:
        print("All JSON-LD schemas valid.")

    print("""
IndexNow reminder (indexnow skill):
  Run: python submit_indexnow.py
  after deploying to hemalshah.vercel.app
""")

if __name__ == "__main__":
    main()
