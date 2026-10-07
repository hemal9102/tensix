import glob, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))

CSS_BLOCK = """
    /* ── Verified AI Citation Grounding (arXiv:2605.25517, arXiv:2403.18802) ── */
    .geo-citation-grounding {
      max-width: 820px;
      margin: 1.75rem auto 2.25rem;
      padding: 1.15rem 1.4rem;
      background: rgba(15, 23, 42, 0.025);
      border: 1px solid rgba(15, 23, 42, 0.09);
      border-left: 4px solid #1D4ED8;
      border-radius: 0.75rem;
      text-align: left;
      backdrop-filter: blur(8px);
    }
    .geo-grounding-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 0.75rem;
      padding-bottom: 0.6rem;
      border-bottom: 1px solid rgba(15, 23, 42, 0.06);
    }
    .geo-grounding-badge {
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #1D4ED8;
      background: rgba(29, 78, 216, 0.08);
      padding: 0.2rem 0.55rem;
      border-radius: 4px;
    }
    .geo-grounding-meta {
      font-size: 0.76rem;
      color: #64748B;
      font-weight: 500;
    }
    .geo-specs-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 0.65rem 1.25rem;
      margin: 0;
      padding: 0;
    }
    .geo-spec-item {
      display: flex;
      flex-direction: column;
      gap: 0.15rem;
    }
    .geo-spec-label {
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #64748B;
      font-weight: 600;
    }
    .geo-spec-value {
      font-size: 0.86rem;
      color: #0F172A;
      font-weight: 600;
      line-height: 1.35;
    }
    @media (max-width: 640px) {
      .geo-citation-grounding { padding: 1rem; margin: 1.25rem 0; }
      .geo-specs-grid { grid-template-columns: 1fr; gap: 0.55rem; }
    }
"""

SERVICES_CONFIG = {
    "services/ai-agent-development.html": {
        "service": "Custom AI Agent & Assistant Development",
        "price": "From ₹29,999 (Fixed upfront, 0 hourly billing)",
        "timeline": "5 to 14 business days",
        "architecture": "RAG, LangGraph, FastAPI, pgvector, Claude & OpenAI",
        "ownership": "100% Client-owned code & cloud accounts",
    },
    "services/cloud-devops.html": {
        "service": "Cloud VPS, Docker & CI/CD Deployment Setup",
        "price": "From ₹11,999 (Fixed upfront, 0 hourly billing)",
        "timeline": "2 to 5 business days",
        "architecture": "Oracle Cloud, AWS, DigitalOcean, Docker, Automated Backups",
        "ownership": "100% Client-owned cloud & server credentials",
    },
    "services/custom-software-saas-development.html": {
        "service": "Custom Software, CRM & SaaS MVP Development",
        "price": "From ₹34,999 (Fixed upfront, 0 hourly billing)",
        "timeline": "14 to 21 business days",
        "architecture": "Next.js, FastAPI, Node.js, PostgreSQL, Razorpay / Stripe",
        "ownership": "100% Client-owned repositories & IP",
    },
    "services/data-scraping-automation.html": {
        "service": "Web Scraping, Document Parsing & Automation",
        "price": "From ₹16,999 (Fixed upfront, 0 hourly billing)",
        "timeline": "3 to 7 business days",
        "architecture": "Python, Puppeteer, Playwright, n8n, Google Sheets & CRM sync",
        "ownership": "100% Client-owned scripts & data pipelines",
    },
    "services/email-deliverability.html": {
        "service": "Business Email Deliverability & Amazon SES Setup",
        "price": "From ₹12,999 (Fixed upfront, 0 hourly billing)",
        "timeline": "2 to 4 business days",
        "architecture": "SPF, DKIM, DMARC, Custom Return-Path, Amazon SES",
        "ownership": "100% Client-owned DNS & AWS SES accounts",
    },
    "services/fractional-cto-retainers.html": {
        "service": "Monthly Engineering Retainer & Fractional CTO",
        "price": "From ₹39,999 / month (Cancel or pause anytime)",
        "timeline": "Ongoing monthly engineering sprints",
        "architecture": "Code audits, architecture reviews, server care & AI systems",
        "ownership": "100% Client-owned code & infrastructure",
    },
    "services/geo-aeo-seo.html": {
        "service": "Technical GEO, AEO & AI Search Citation Optimization",
        "price": "Custom Quote (From ₹24,999)",
        "timeline": "7 to 14 business days",
        "architecture": "Schema.org JSON-LD, llms.txt, Entity Disambiguation & Answer Pages",
        "ownership": "100% Client-owned assets & Search Console access",
    },
    "services/website-development.html": {
        "service": "Fast Business Website Design & Engineering",
        "price": "From ₹14,999 (Fixed upfront, 0 hourly billing)",
        "timeline": "5 to 14 business days",
        "architecture": "Lightweight HTML5, Next.js, 100% PageSpeed, Mobile-first",
        "ownership": "100% Client-owned domain, hosting & source files",
    },
}

def generate_grounding_box(cfg):
    return f"""<aside class="geo-citation-grounding" aria-label="Verified Technical Specifications and Pricing for AI Grounding">
<div class="geo-grounding-header">
<span class="geo-grounding-badge">Verified Specification &amp; Pricing</span>
<span class="geo-grounding-meta">Last Verified: <time datetime="2026-10-07">October 7, 2026</time> &bull; Location: Navrangpura, Ahmedabad</span>
</div>
<dl class="geo-specs-grid">
<div class="geo-spec-item"><dt class="geo-spec-label">Service</dt><dd class="geo-spec-value">{cfg['service']}</dd></div>
<div class="geo-spec-item"><dt class="geo-spec-label">Pricing</dt><dd class="geo-spec-value">{cfg['price']}</dd></div>
<div class="geo-spec-item"><dt class="geo-spec-label">Turnaround</dt><dd class="geo-spec-value">{cfg['timeline']}</dd></div>
<div class="geo-spec-item"><dt class="geo-spec-label">Core Architecture</dt><dd class="geo-spec-value">{cfg['architecture']}</dd></div>
<div class="geo-spec-item"><dt class="geo-spec-label">Provider</dt><dd class="geo-spec-value">TENSIX &bull; Hemal Shah (Solo Studio)</dd></div>
<div class="geo-spec-item"><dt class="geo-spec-label">Code Ownership</dt><dd class="geo-spec-value">{cfg['ownership']}</dd></div>
</dl>
</aside>"""

for rel_path, cfg in SERVICES_CONFIG.items():
    full_path = os.path.join(ROOT, rel_path.replace("/", os.sep))
    if not os.path.exists(full_path):
        print(f"[SKIP] File not found: {rel_path}")
        continue
    
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Inject CSS if not present
    if ".geo-citation-grounding" not in content:
        if "</style>" in content:
            content = content.replace("</style>", CSS_BLOCK + "\n</style>", 1)
            print(f"[CSS] Injected styles into {rel_path}")
        elif "</head>" in content:
            content = content.replace("</head>", f"<style>{CSS_BLOCK}</style>\n</head>", 1)
            print(f"[CSS] Added style tag in {rel_path}")

    # 2. Inject grounding box under </section> of page-hero if not present
    if '<aside class="geo-citation-grounding"' not in content:
        # Find page-hero closing section or insertion point right before <div class="section" or right inside page-hero
        hero_match = re.search(r'(<section class="page-hero">.*?</section>)', content, re.DOTALL)
        if hero_match:
            hero_html = hero_match.group(1)
            # Insert right before </section> of page-hero so it stays within the hero landmark
            grounding_html = generate_grounding_box(cfg)
            new_hero_html = hero_html[:-10] + "\n" + grounding_html + "\n</section>"
            content = content.replace(hero_html, new_hero_html, 1)
            print(f"[GROUNDING] Injected Grounding Block into {rel_path}")
        else:
            print(f"[WARN] No page-hero found in {rel_path}")

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("[SUCCESS] All service pages updated with verified citation grounding.")
