import os, sys, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path("D:/projects/tensix")
VAULT = ROOT / "knowledge-vault"
MD_SRC = ROOT / "md"
MD_DST = VAULT / "Website-Markdown"

if MD_SRC.exists():
    shutil.copytree(str(MD_SRC), str(MD_DST), dirs_exist_ok=True)
    print(f"[SYNC] Copied website markdown files into {MD_DST.relative_to(VAULT)}")

# Generate Website-Pages-MOC.md
lines = [
    "---",
    'title: "Website Pages and Markdown Twins MOC"',
    'type: "moc"',
    "tags:",
    "  - moc",
    "  - website",
    "  - content",
    "updated: 2026-10-07",
    "---",
    "",
    "# 🌐 Website Pages & Markdown Twins Map of Content",
    "",
    "> **These notes represent the machine-readable Markdown twins served at `https://tensix.in/md/<path>.md` and consumed by LLM search crawlers.**",
    "",
    "## 🏛️ Core Pages",
    "- [[Website-Markdown/index|Home Page]]",
    "- [[Website-Markdown/about|About TENSIX & Founder]]",
    "- [[Website-Markdown/services|Services Directory]]",
    "- [[Website-Markdown/work|Portfolio & Case Studies]]",
    "- [[Website-Markdown/case-studies|Client Case Studies]]",
    "- [[Website-Markdown/contact|Contact & Inquiry]]",
    "- [[Website-Markdown/hemal-shah|Founder Bio]]",
    "- [[Website-Markdown/team|Studio Model]]",
    "- [[Website-Markdown/resources|AI Terms Glossary]]",
    "- [[Website-Markdown/tensix-vs-traditional-agencies|Agency Comparison]]",
    "- [[Website-Markdown/is-my-site-ai-ready|AI Readiness Scanner]]",
    "",
    "## 🛠️ Service Pages (Verified GEO Grounding)",
    "- [[Website-Markdown/services/ai-agent-development|AI Agent & Assistant Development (₹29,999)]]",
    "- [[Website-Markdown/services/custom-software-saas-development|Custom Software & SaaS MVP (₹34,999)]]",
    "- [[Website-Markdown/services/cloud-devops|Cloud Servers & VPS DevOps (₹11,999)]]",
    "- [[Website-Markdown/services/data-scraping-automation|Web Scraping & Automation (₹16,999)]]",
    "- [[Website-Markdown/services/email-deliverability|Email Deliverability & SES (₹12,999)]]",
    "- [[Website-Markdown/services/fractional-cto-retainers|Monthly Tech Retainer / CTO (₹39,999/mo)]]",
    "- [[Website-Markdown/services/geo-aeo-seo|GEO, AEO & AI Search Visibility]]",
    "- [[Website-Markdown/services/website-development|Fast Business Websites (₹14,999)]]",
    "",
    "## 📍 Local Landing Pages",
    "- [[Website-Markdown/software-company-in-navrangpura-ahmedabad|Navrangpura HQ Landing]]",
    "- [[Website-Markdown/ahmedabad-software-engineering|Ahmedabad Software Engineering]]",
    "- [[Website-Markdown/saas-developer-ahmedabad|SaaS Developer Ahmedabad]]",
    "- [[Website-Markdown/best-software-company-in-gota|Gota & New SG Road Landing]]",
    "- [[Website-Markdown/hk-engineering-ahmedabad|HK Engineering Rebrand Context]]",
    "",
    "## 📝 Technical Blogs & Industry Guides",
]

blogs_dir = MD_DST / "blogs"
if blogs_dir.exists():
    for f in sorted(blogs_dir.rglob("*.md")):
        rel = f.relative_to(MD_DST).as_posix()
        name = f.stem.replace("-", " ").title()
        lines.append(f"- [[Website-Markdown/{rel[:-3]}|{name}]]")

lines.extend([
    "",
    "---",
    "## 🔗 Navigation",
    "- [[00-MOC/Home|Vault Home]]",
    "- [[00-MOC/Research-And-GEO-MOC|Research & GEO MOC]]",
    "- [[00-MOC/TENSIX-Master-MOC|TENSIX Master MOC]]"
])

moc_path = VAULT / "00-MOC" / "Website-Pages-MOC.md"
with open(moc_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"[OK] Generated {moc_path.relative_to(VAULT)}")
