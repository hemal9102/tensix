"""
TenSix Competitor Outflank
--------------------------
Free, robust competitor keyword/intent reconnaissance for the 8 real Ahmedabad
studio rivals surfaced by the keyword battle plan. No paid SEO API.

Pieces (techniques from docs/05 - Competitor Reverse-Engineering ...):
  1. Sitemap crawl (curl.exe): robots.txt + sitemap_index/sitemap/wp-sitemap,
     follow redirects + browser UA. Yields every page URL + slug + <lastmod>.
     (doc §1A)
  2. Page title/H1 extraction: fetch a sample of each rival's money pages and
     pull <title>/<h1> — what they actually target.
  3. Google Suggest harvest: suggestqueries.google.com (free, no key) seeded
     from TenSix services + rival slugs — real search stems. (doc §2A)
  4. Header fingerprint (curl.exe -ILs): TTFB / cache / server on a sample page
     — where a rival is slow, TenSix's static edge wins. (doc §1C)
  5. Jev intent clustering: every harvested keyword/slug clustered by intent
     (cto_leadership / money_service / local / informational / comparison),
     then rival coverage vs TenSix gap.

Output: competitor_outflank_plan.md — TenSix action plan (priority targets,
cluster gaps, per-doc outflank moves).

Keys (never hardcoded):
    $env:OPENROUTER_API_KEY   (Jev clustering; or TYPESAFE_API_KEY)

Usage:
    python competitor_outflank.py --limit-pages 40 --suggest-seeds 20
    python competitor_outflank.py --competitors "kanhasoft.com;duplextech.com"
    python competitor_outflank.py --no-fingerprint
"""

import os
import re
import sys
import json
import time
import argparse
import subprocess
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime

from keyword_battle_plan import (OR_DECISIONS_API, OR_DECISIONS_MODEL, TS_API, TS_MODEL,
                                 _retry_http)

ROOT = os.path.dirname(os.path.abspath(__file__))
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

DEFAULT_COMPETITORS = [
    "kanhasoft.com", "dngwebdeveloper.com", "duplextech.com", "suntecindia.com",
    "areinfotech.com", "esparkinfo.com", "orangemantra.com", "greencubes.co.in",
]

# TenSix's own offering vocabulary — seeds for Google Suggest + gap mapping.
TENSIX_SEEDS = [
    "fractional cto", "custom saas development", "custom crm development",
    "ai agent development", "business process automation", "workflow automation",
    "web scraping service", "email deliverability", "amazon ses setup",
    "website development ahmedabad", "software company ahmedabad",
    "devops setup", "geo aeo seo", "b2b manufacturing website",
]

INTENT_CLUSTER = {
    "type": "choice",
    "instructions": "Classify the search intent of `keyword` for a B2B software/AI studio buyer.",
    "criteria": {
        "cto_leadership": "Hiring tech leadership / strategy (fractional CTO, technical co-founder, tech retainer).",
        "money_service": "Ready to buy a build service (custom software, SaaS, CRM, AI agent, automation, scraping, devops, email, website).",
        "local": "Looking for a provider in a specific city/area (Ahmedabad, Navrangpura, Gujarat).",
        "comparison": "Comparing providers/tools or seeking alternatives (vs, best, top, alternatives, review).",
        "informational": "Learning/how-to/definition, not ready to buy.",
        "irrelevant": "Not a real buyer query for this studio.",
    },
}
VALUE_CLUSTER = {
    "type": "score",
    "instructions": "How valuable is ranking for `keyword` to a studio chasing CTO/CEO and high-ticket 'boring-rich' B2B work?",
    "criteria": [
        "Low: informational/tyre-kicker, little revenue intent.",
        "Medium: service interest but broad or low-ticket.",
        "High: decision-maker / high-ticket / clear buying intent.",
    ],
}
QUESTIONS = {"intent": INTENT_CLUSTER, "value": VALUE_CLUSTER}


# ---------------------------------------------------------------------------
# curl helpers
# ---------------------------------------------------------------------------
def curl_text(url, timeout=20):
    try:
        p = subprocess.run(["curl.exe", "-sL", "--max-time", str(timeout), "-A", UA, url],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        return p.stdout or ""
    except Exception:
        return ""


def curl_headers(url, timeout=20):
    """curl -ILs: header-only, follow redirects. Returns raw header text + TTFB."""
    try:
        p = subprocess.run(
            ["curl.exe", "-sIL", "--max-time", str(timeout), "-A", UA,
             "-w", "\\nTTFB:%{time_starttransfer}\\nCODE:%{http_code}\\n", url],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        return p.stdout or ""
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# 1. Sitemap crawl
# ---------------------------------------------------------------------------
def discover_sitemaps(domain):
    base = f"https://{domain}"
    found = []
    robots = curl_text(f"{base}/robots.txt", 15)
    for m in re.findall(r"(?i)sitemap:\s*(\S+)", robots):
        found.append(m.strip())
    for path in ("sitemap_index.xml", "sitemap.xml", "wp-sitemap.xml", "sitemap-index.xml"):
        url = f"{base}/{path}"
        if url not in found:
            txt = curl_text(url, 15)
            if "<loc>" in txt or "<sitemap" in txt or "<urlset" in txt:
                found.append(url)
    # de-dupe preserving order
    seen, out = set(), []
    for u in found:
        if u not in seen:
            seen.add(u); out.append(u)
    return out


def expand_sitemaps(sitemap_urls, max_depth=2):
    """Follow sitemap index -> child sitemaps; collect <loc> page URLs + lastmod."""
    pages = {}
    queue = [(u, 0) for u in sitemap_urls]
    visited = set()
    while queue:
        sm, depth = queue.pop(0)
        if sm in visited or depth > max_depth:
            continue
        visited.add(sm)
        xml = curl_text(sm, 20)
        # child sitemaps
        is_index = "<sitemapindex" in xml
        for loc, lastmod in re.findall(r"<loc>(.*?)</loc>(?:\s*<lastmod>(.*?)</lastmod>)?", xml, re.S):
            loc = loc.strip()
            if not loc:
                continue
            if is_index or loc.endswith(".xml"):
                queue.append((loc, depth + 1))
            else:
                pages[loc] = (lastmod or "").strip()
    return pages


def slug_terms(url):
    """Turn a URL path into readable terms, e.g. /services/saas-app-development -> 'saas app development'."""
    path = urllib.parse.urlparse(url).path.strip("/")
    path = re.sub(r"\.(html?|php|aspx)$", "", path)
    parts = re.split(r"[/\-_]+", path)
    stop = {"services", "service", "en", "in", "page", "index", "blog", "category", ""}
    kept = [p for p in parts if p and p.lower() not in stop and not p.isdigit()]
    return " ".join(kept).lower()


# ---------------------------------------------------------------------------
# 2. Title / H1 extraction
# ---------------------------------------------------------------------------
def page_title_h1(url):
    html = curl_text(url, 20)
    t = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    h = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)
    clean = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip() if s else ""
    return clean(t.group(1) if t else ""), clean(h.group(1) if h else "")


# ---------------------------------------------------------------------------
# 3. Google Suggest
# ---------------------------------------------------------------------------
def google_suggest(seed, gl="in"):
    url = ("https://suggestqueries.google.com/complete/search?client=chrome&hl=en"
           f"&gl={gl}&q={urllib.parse.quote(seed)}")
    txt = curl_text(url, 12)
    try:
        data = json.loads(txt)
        return data[1] if len(data) > 1 else []
    except Exception:
        return []


# ---------------------------------------------------------------------------
# 4. Header fingerprint
# ---------------------------------------------------------------------------
def fingerprint(url):
    raw = curl_headers(url, 20)
    def grab(name):
        m = re.search(rf"(?im)^{name}:\s*(.+)$", raw)
        return m.group(1).strip() if m else ""
    ttfb = grab("TTFB")
    return {
        "ttfb": float(ttfb) if re.match(r"^[\d.]+$", ttfb) else None,
        "server": grab("Server"),
        "cache": grab("X-Cache") or grab("CF-Cache-Status"),
        "code": grab("CODE"),
    }


# ---------------------------------------------------------------------------
# 5. Jev clustering (own judge using THIS module's QUESTIONS)
# ---------------------------------------------------------------------------
def _ask_decisions(state, key):
    body = json.dumps({"model": OR_DECISIONS_MODEL, "state": state, "questions": QUESTIONS}).encode()

    def call():
        req = urllib.request.Request(OR_DECISIONS_API, body,
                                     {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)["answers"]
    return _retry_http(call)


def _ask_native(state, key):
    body = json.dumps({"model": TS_MODEL, "state": state, "questions": QUESTIONS}).encode()

    def call():
        req = urllib.request.Request(TS_API, body,
                                     {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)["answers"]
    return _retry_http(call)


def select_judge():
    if os.environ.get("TYPESAFE_API_KEY"):
        return _ask_native, os.environ["TYPESAFE_API_KEY"], "TypeSafe System One jev-latest (calibrated)"
    if os.environ.get("OPENROUTER_API_KEY"):
        return _ask_decisions, os.environ["OPENROUTER_API_KEY"], "OpenRouter typesafe/jev-1.13 decisions (calibrated)"
    sys.exit("Set OPENROUTER_API_KEY or TYPESAFE_API_KEY for the Jev judge.")


def classify(keyword, judge, key):
    return judge({"keyword": keyword}, key)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--competitors", help="Semicolon-separated; default = 8 studios")
    ap.add_argument("--limit-pages", type=int, default=40, help="Max money-pages per rival to title-scan")
    ap.add_argument("--suggest-seeds", type=int, default=0, help="Extra rival-slug seeds to Google-Suggest (0=TenSix seeds only)")
    ap.add_argument("--no-fingerprint", action="store_true")
    ap.add_argument("--max-cluster", type=int, default=250, help="Cap keywords sent to Jev (cost guard)")
    ap.add_argument("--out", default=os.path.join(ROOT, "competitor_outflank_plan.md"))
    args = ap.parse_args()

    competitors = ([c.strip() for c in args.competitors.split(";") if c.strip()]
                   if args.competitors else list(DEFAULT_COMPETITORS))

    judge, key, judge_name = select_judge()
    print(f"Judge: {judge_name}\n")

    rivals = {}
    for d in competitors:
        print(f"[{d}] discovering sitemaps...")
        sms = discover_sitemaps(d)
        pages = expand_sitemaps(sms) if sms else {}
        # keep likely money/service pages (skip blog/tag/author noise)
        money = {u: lm for u, lm in pages.items()
                 if not re.search(r"/(blog|tag|author|category|wp-content|feed|20\d\d)/", u, re.I)}
        print(f"    sitemaps={len(sms)} pages={len(pages)} service-ish={len(money)}")
        # title/h1 scan a sample
        sample = list(money)[:args.limit_pages]
        titles = []
        for u in sample:
            t, h = page_title_h1(u)
            if t or h:
                titles.append({"url": u, "title": t, "h1": h, "slug": slug_terms(u)})
            time.sleep(0.1)
        fp = None
        if not args.no_fingerprint and sample:
            fp = fingerprint(sample[0])
        rivals[d] = {"sitemaps": sms, "n_pages": len(pages), "n_money": len(money),
                     "titles": titles, "fingerprint": fp,
                     "slugs": sorted({t["slug"] for t in titles if t["slug"]})}

    # Build keyword universe: TenSix seeds + rival slugs -> Google Suggest expand
    seeds = list(TENSIX_SEEDS)
    if args.suggest_seeds:
        rival_slugs = sorted({s for r in rivals.values() for s in r["slugs"]})
        seeds += rival_slugs[:args.suggest_seeds]
    print(f"\nGoogle Suggest on {len(seeds)} seeds...")
    universe = set()
    for s in seeds:
        universe.add(s.lower())
        for sug in google_suggest(s):
            universe.add(sug.lower())
        time.sleep(0.15)
    # add rival slugs themselves as candidate keywords
    for r in rivals.values():
        universe.update(r["slugs"])
    universe = sorted(k for k in universe if 2 <= len(k.split()) <= 8)

    # Light relevance pre-filter: keep only keywords touching TenSix's domain,
    # so Jev isn't spent on Google-Suggest junk (movies, salaries, meanings).
    RELEVANT = ("softwar", "saas", "crm", "erp", "develop", "ai ", " ai", "agent", "automat",
                "workflow", "scrap", "data", "cto", "devops", "cloud", "server", "vps", "api",
                "email", "deliver", "ses", "smtp", "website", "web app", "web develop", "app develop",
                "seo", "aeo", "geo", "b2b", "manufactur", "ecommerce", "e-commerce", "portal",
                "integrat", "dashboard", "platform", "consult", "architect", "mvp", "startup",
                "ahmedabad", "navrangpura", "gujarat", "india", "python", "django", "node",
                "react", "next", "fastapi", "retainer", "co-founder", "cofounder")
    DROP = ("movie", "salary", "jobs", "job ", "course", "tutorial", "internship", "meaning",
            "gujarati", "hindi", "app download", "yono", "allu", "allen", "salon", "ikea",
            "roadmap", "interview", "certificat", "free with", "apk", "games", "about blank",
            "artstation", "figma template", "portfolio pdf", "portfolio template")

    def relevant(k):
        if any(d in k for d in DROP):
            return False
        return any(r in k for r in RELEVANT)

    filtered = [k for k in universe if relevant(k)]
    print(f"Keyword universe: {len(universe)} -> {len(filtered)} relevant "
          f"(capping Jev at {args.max_cluster})")
    universe = filtered

    # Jev cluster
    clustered = defaultdict(list)
    valued = {}
    for kw in universe[:args.max_cluster]:
        try:
            a = classify(kw, judge, key)
            intent = a["intent"]["choice"]
            val = a["value"]["score"]
            clustered[intent].append(kw)
            valued[kw] = val
        except Exception as e:
            print(f"  cluster failed: {kw} ({e})")
        time.sleep(0.2)

    render_plan(args.out, competitors, rivals, clustered, valued, judge_name)
    print(f"\nPlan saved: {args.out}")


def render_plan(path, competitors, rivals, clustered, valued, judge_name):
    CLUSTER_ORDER = ["cto_leadership", "money_service", "local", "comparison",
                     "informational", "irrelevant"]
    LABEL = {"cto_leadership": "CTO / Tech Leadership", "money_service": "Money Service (build)",
             "local": "Local (Ahmedabad)", "comparison": "Comparison / Alternatives",
             "informational": "Informational", "irrelevant": "Irrelevant"}

    def high_value(kws):
        return sorted([k for k in kws if valued.get(k, 0) >= 1.5],
                      key=lambda k: -valued.get(k, 0))

    out = ["# TenSix Competitor Outflank — Action Plan", "",
           f"Date: {datetime.now():%Y-%m-%d %H:%M} | Judge: {judge_name}",
           f"Competitors analyzed: {', '.join(competitors)}", "",
           "> Free recon: curl sitemap crawl + Google Suggest + Jev intent/value clustering. "
           "No paid SEO API. Techniques per `docs/05 - Competitor Reverse-Engineering ...`.", ""]

    # Competitor coverage snapshot
    out += ["## 1. Competitor snapshot", "",
            "| Rival | Pages (sitemap) | Service pages scanned | TTFB | Server/cache |",
            "|---|---|---|---|---|"]
    for d in competitors:
        r = rivals.get(d, {})
        fp = r.get("fingerprint") or {}
        ttfb = f"{fp.get('ttfb'):.2f}s" if fp.get("ttfb") else "—"
        sc = " / ".join(x for x in [fp.get("server", ""), fp.get("cache", "")] if x) or "—"
        out.append(f"| {d} | {r.get('n_pages', 0)} | {len(r.get('titles', []))} | {ttfb} | {sc} |")
    out.append("")
    slow = [d for d in competitors if (rivals.get(d, {}).get("fingerprint") or {}).get("ttfb") and
            rivals[d]["fingerprint"]["ttfb"] > 0.6]
    if slow:
        out.append(f"**Speed edge:** {', '.join(slow)} have TTFB > 0.6s — TenSix's static edge "
                   "(<50ms) is a direct Core Web Vitals ranking lever against them (doc §1C/§6).")
        out.append("")

    # Keyword clusters
    out += ["## 2. Keyword clusters (what buyers search; what rivals target)", ""]
    for c in CLUSTER_ORDER:
        kws = clustered.get(c, [])
        if not kws:
            continue
        hv = high_value(kws)
        out += [f"### {LABEL[c]}  ({len(kws)} keywords, {len(hv)} high-value)", ""]
        if hv:
            out.append("**High-value targets:**")
            out += [f"- {k}" for k in hv[:25]]
            out.append("")
        rest = [k for k in kws if k not in hv][:30]
        if rest:
            out.append(f"<details><summary>Other {LABEL[c].lower()} keywords ({len(rest)})</summary>\n")
            out += [f"- {k}" for k in rest]
            out.append("\n</details>\n")

    # TenSix priority actions
    out += ["## 3. TenSix priority actions", ""]
    cto = high_value(clustered.get("cto_leadership", []))
    money = high_value(clustered.get("money_service", []))
    local = high_value(clustered.get("local", []))
    comp = clustered.get("comparison", [])
    if cto:
        out.append(f"1. **Own the CTO/leadership cluster** — TenSix already has a fractional-CTO service; "
                   f"build dedicated, honest pages for: {', '.join(cto[:6])}. This is the highest-ticket, "
                   "lowest-competition cluster for a solo studio.")
    if local:
        out.append(f"2. **Win local intent** — rivals' pages often lack strong Ahmedabad/Navrangpura signal. "
                   f"Target: {', '.join(local[:6])} with genuine local context (doc §: Layer 5 corridors).")
    if money:
        out.append(f"3. **Out-specify money-service keywords** — {', '.join(money[:6])}. Each needs a "
                   "45–55 word Position-0 answer card + FAQPage schema + fixed-price plan (doc §4, CLAUDE.md §4.2/§5).")
    if comp:
        out.append(f"4. **Capture comparison intent** — {len(comp)} comparison/alternative queries exist "
                   f"(e.g. {', '.join(comp[:4])}). TenSix's existing 'vs agencies' page can be extended honestly.")
    out.append("5. **After publishing**, push via Google Indexing API + IndexNow for instant crawl (doc §5).")
    out.append("")
    out += ["## 4. Per-rival target slugs (what they rank on; mirror honestly where TenSix is absent)", ""]
    for d in competitors:
        r = rivals.get(d, {})
        slugs = r.get("slugs", [])[:15]
        if slugs:
            out += [f"**{d}:** " + ", ".join(slugs), ""]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
