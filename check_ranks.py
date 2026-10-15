"""
TenSix Rank Checker (SerpAPI)
-----------------------------
Checks where www.tensix.in ranks on Google (India) for high-intent,
decision-maker (CTO/CEO) and high-value ("boring but rich") business
keywords, using SerpAPI's real Google SERP data.

The SerpAPI key is read from the SERPAPI_KEY environment variable
(never hardcoded). Set it before running, e.g. in PowerShell:
    $env:SERPAPI_KEY = "your_key_here"

Usage:
    python check_ranks.py
    python check_ranks.py --depth 100 --location "Ahmedabad,Gujarat,India"
"""

import os
import json
import time
import argparse
import urllib.parse
import urllib.request
from datetime import datetime

TARGET_DEFAULT = "tensix.in"

# Keywords derived from TenSix's own page titles/H1s + the 8 services.
# These are the real, high-intent, decision-maker + "boring-rich" queries
# the site is actually built to win. Spam/concatenated variants from
# seo_keywords.txt are deliberately excluded.
KEYWORDS = [
    # --- Brand (baseline) ---
    "tensix",
    "tensix ahmedabad",
    "hemal shah tensix",

    # --- Fractional CTO / tech leadership (CTO/CEO intent) ---
    "fractional cto ahmedabad",
    "fractional cto services india",
    "monthly tech retainer for startup",
    "part time cto for startup india",
    "technical co-founder for hire india",

    # --- Custom software / SaaS / CRM (service pages) ---
    "custom saas development ahmedabad",
    "saas developer ahmedabad",
    "saas development company ahmedabad",
    "custom crm development ahmedabad",
    "custom software development company ahmedabad",
    "multi tenant saas architecture india",
    "saas mvp development india",

    # --- AI agents / automation (core offering) ---
    "ai agent development company india",
    "ai assistant development for business",
    "business process automation ahmedabad",
    "workflow automation company india",
    "n8n automation developer india",

    # --- Data scraping (boring-rich niche) ---
    "web scraping company india",
    "data scraping service for business",

    # --- Cloud / DevOps ---
    "cloud server setup service india",
    "devops setup for startup india",
    "vps server management india",

    # --- Email deliverability (boring-rich niche) ---
    "email deliverability consultant india",
    "amazon ses setup service",
    "fix emails going to spam business",

    # --- Website development (local money) ---
    "website development company ahmedabad",
    "business website developer ahmedabad",
    "fast business website ahmedabad",

    # --- GEO / AEO / AI-search SEO (differentiator) ---
    "geo aeo seo services india",
    "get cited by chatgpt perplexity seo",
    "ai search optimization company india",

    # --- Industrial / B2B manufacturing (high-value Ahmedabad clusters) ---
    "b2b manufacturing website ahmedabad",
    "industrial web development ahmedabad",
    "export business website ahmedabad",

    # --- Local / general discovery ---
    "best software company in ahmedabad",
    "software company in navrangpura ahmedabad",
    "software development company ahmedabad",
    "ai development company ahmedabad",

    # --- Industry survival-guide intent (long-tail, low competition) ---
    "ahmedabad pharma export website",
    "ahmedabad textile exporter website",
    "ahmedabad jewelry ecommerce website",
]

def serpapi_search(keyword, location, depth, api_key):
    params = {
        "engine": "google",
        "q": keyword,
        "location": location,
        "google_domain": "google.co.in",
        "gl": "in",
        "hl": "en",
        "num": depth,
        "api_key": api_key,
    }
    url = "https://serpapi.com/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "tensix-rank-checker"})
    with urllib.request.urlopen(req, timeout=40) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def rank_of(target, organic, depth):
    for item in organic:
        pos = item.get("position")
        link = item.get("link", "")
        try:
            host = urllib.parse.urlparse(link).netloc.lower()
        except Exception:
            host = ""
        if pos and pos <= depth and target in host:
            return pos, link
    return None, None


def check(keyword, target, location, depth, api_key, retries=2):
    last_err = None
    for attempt in range(retries + 1):
        try:
            data = serpapi_search(keyword, location, depth, api_key)
            if "error" in data:
                raise RuntimeError(data["error"])
            organic = data.get("organic_results", [])
            return rank_of(target, organic, depth)
        except (TimeoutError, OSError) as e:
            last_err = e
            time.sleep(3)
    raise last_err


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=TARGET_DEFAULT)
    ap.add_argument("--depth", type=int, default=100)
    ap.add_argument("--location", default="India")
    ap.add_argument("--delay", type=float, default=1.0)
    args = ap.parse_args()

    api_key = os.environ.get("SERPAPI_KEY")
    if not api_key:
        print("ERROR: SERPAPI_KEY environment variable not set.")
        print('Set it first:  $env:SERPAPI_KEY = "your_key"')
        sys.exit(1)

    print("=" * 70)
    print(f"  TENSIX RANK CHECK (SerpAPI / Google India)")
    print(f"  target={args.target}  location={args.location}  depth=top-{args.depth}")
    print(f"  {datetime.now():%Y-%m-%d %H:%M}")
    print("=" * 70)
    print(f"{'POS':>5}  KEYWORD")
    print("-" * 70)

    found, missing, errors = 0, 0, 0
    report_lines = []
    for kw in KEYWORDS:
        try:
            pos, link = check(kw, args.target, args.location, args.depth, api_key)
            if pos:
                tag = f"#{pos}"
                found += 1
            else:
                tag = "--"
                missing += 1
            print(f"{tag:>5}  {kw}")
            report_lines.append((kw, pos, link))
        except Exception as e:
            errors += 1
            print(f"  ERR  {kw}  ({type(e).__name__}: {e})")
            report_lines.append((kw, None, f"ERROR: {e}"))
        time.sleep(args.delay)

    print("-" * 70)
    print(f"  Ranked: {found}   Not in top-{args.depth}: {missing}   Errors: {errors}")
    print("=" * 70)

    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    out = f"rank_report_{stamp}.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# TenSix Rank Report (SerpAPI / Google {args.location})\n\n")
        f.write(f"Date: {datetime.now():%Y-%m-%d %H:%M} | Target: {args.target} | Depth: top-{args.depth}\n\n")
        f.write("| Pos | Keyword | URL |\n|----|---------|-----|\n")
        for kw, pos, link in report_lines:
            p = f"#{pos}" if pos else "—"
            f.write(f"| {p} | {kw} | {link or ''} |\n")
    print(f"Report saved: {out}")


if __name__ == "__main__":
    main()
