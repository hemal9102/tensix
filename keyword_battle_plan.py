"""
TenSix Keyword Battle Plan
--------------------------
For each target keyword this pipeline:
  1. Fetches the top-10 Google (India) competitors + TenSix's live rank via SerpAPI
     (one call per keyword; cached in serp_cache.json to protect quota).
  2. Grounds priorities in TenSix's OWN real Google data:
       - Search Console (GSC): impressions / clicks / avg position per query.
       - GA4: which pages actually get traffic / conversions.
     (Both optional; skipped gracefully if creds/libs are absent.)
  3. Scores each competitor with the TypeSafe "Jev" model (OpenRouter, or native
     TypeSafe) using TenSix's own 48-variable Position-0 rubric as the basis.
  4. Synthesizes an honest, per-keyword action plan: who the top 10 are, which
     ranking levers they win/lose on, and what TenSix must do to rank.

Honesty: recommendations obey CLAUDE.md §5 (no fake claims/guarantees/invented
stats) and §4.2 (service pages carry Service + FAQPage schema). We recommend the
STRUCTURE (answer envelope, FAQ schema, local corridors, Person/E-E-A-T), never
fabricated numbers.

Keys/config (never hardcoded):
    $env:SERPAPI_KEY   = "..."                       # required for competitors
    $env:OPENROUTER_API_KEY = "sk-or-..."            # Jev judge (primary)
    $env:TYPESAFE_API_KEY   = "..."                  # Jev judge (native, calibrated)
    --creds <path>     service-account json (GSC+GA4)  or GOOGLE_APPLICATION_CREDENTIALS
    --gsc-site sc-domain:tensix.in
    --ga4-property 550016993   or  $env:GA4_PROPERTY_ID

Usage:
    python keyword_battle_plan.py --dry-run
    python keyword_battle_plan.py --serp-only --limit 1
    python keyword_battle_plan.py --only-money --limit 10 --creds <sa.json> --gsc-site sc-domain:tensix.in --ga4-property 550016993
"""

import os
import re
import sys
import json
import time
import argparse
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

# Reuse the proven SerpAPI client + keyword list (its main() is __main__-guarded).
from check_ranks import serpapi_search, rank_of, KEYWORDS, TARGET_DEFAULT

ROOT = os.path.dirname(os.path.abspath(__file__))
SERP_CACHE = os.path.join(ROOT, "serp_cache.json")

# Top ~10 money keywords: the decision-maker + boring-rich set to run first.
MONEY_KEYWORDS = [
    "fractional cto ahmedabad",
    "fractional cto services india",
    "custom saas development ahmedabad",
    "custom crm development ahmedabad",
    "ai agent development company india",
    "business process automation ahmedabad",
    "workflow automation company india",
    "web scraping company india",
    "email deliverability consultant india",
    "website development company ahmedabad",
]

# ---------------------------------------------------------------------------
# TypeSafe Jev judge (pattern from citation_audit.py). Code owns policy; Jev
# only supplies judgments. QUESTIONS blend competitor classification with the
# 48-variable Position-0 rubric (the gaps a competitor leaves become TenSix's
# action items).
# ---------------------------------------------------------------------------
TS_API = "https://api.typesafe.ai/v1/systemone"
TS_MODEL = "jev-latest"
# OpenRouter serves real Jev as a "decisions model" on a dedicated endpoint
# (NOT chat/completions). Same {model, state, questions} wire format as native
# TypeSafe System One; response is answers.<name>.{noul|choice|score}.
OR_DECISIONS_API = "https://openrouter.ai/api/alpha/decisions"
OR_DECISIONS_MODEL = "typesafe/jev-1.13"

QUESTIONS = {
    "result_type": {
        "type": "choice",
        "instructions": "From `domain`, `title`, `snippet`, what kind of result holds this Google "
                        "position for `keyword`?",
        "criteria": {
            "studio_or_agency": "A software/AI/dev studio or agency that directly competes with TenSix.",
            "freelancer": "An individual freelancer or solo consultant.",
            "directory_aggregator": "A listings/aggregator (Clutch, GoodFirms, Sortlist, Justdial, DesignRush).",
            "marketplace": "A gig/talent marketplace (Fiverr, Toptal, Upwork, Freelancer.com).",
            "editorial_or_blog": "An article/listicle/blog, not a provider's own service page.",
            "big_brand": "A large national/global firm unlikely to be displaced locally.",
            "other": "None of the above clearly fits.",
        },
    },
    "intent_match": {
        "type": "choice",
        "instructions": "How well does this result match what a buyer typing `keyword` actually wants?",
        "criteria": {
            "direct": "Squarely answers the buyer intent (provider page for exactly this service/place).",
            "partial": "Related but off-angle (wrong location, adjacent service, or generic page).",
            "mismatch": "Does not match the intent; ranks for other reasons.",
        },
    },
    "beatability": {
        "type": "score",
        "instructions": "How realistically could a focused solo Ahmedabad studio (TenSix) outrank THIS "
                        "result for `keyword` with a strong, honest, locally-relevant page?",
        "criteria": [
            "Entrenched: strong national brand or dominant aggregator; very hard to displace.",
            "Hard: established competitor with an on-topic, well-built page.",
            "Winnable: generic, thin, or non-local page a sharper page could beat.",
            "Soft: off-intent, stale, or barely-relevant result holding the slot almost by default.",
        ],
    },
    "answer_envelope": {
        "type": "noul",
        "instructions": "Does `title`+`snippet` present a tight, direct, Position-0 style answer to "
                        "`keyword` (the kind Google lifts into a featured snippet)?",
        "criteria": {"true": "A direct, self-contained answer is evident.",
                     "false": "Slogan, boilerplate, or navigation; no direct answer."},
    },
    "faq_signal": {
        "type": "noul",
        "instructions": "Is there any signal this result carries structured Q&A / FAQ / People-Also-Ask "
                        "style content (from `title`/`snippet`)?",
        "criteria": {"true": "FAQ / question-answer structure is evident.",
                     "false": "No question/answer structure evident."},
    },
    "info_density": {
        "type": "score",
        "instructions": "How concrete and checkable are the claims in `title`+`snippet`?",
        "criteria": [
            "Only generic marketing language; nothing verifiable.",
            "Some concrete detail (named service/tech) but no numbers, dates, or outcomes.",
            "Concrete checkable facts: specific numbers, named tools, or measured outcomes.",
        ],
    },
    "local_corridor": {
        "type": "score",
        "instructions": "From `title`/`snippet`/`domain`, how strong is this result's signal of serving "
                        "the specific location in `keyword` (Ahmedabad / India)?",
        "criteria": [
            "No location signal at all.",
            "Generic pan-India signal only.",
            "Names the city or region relevantly.",
            "Strong, specific local signal (Ahmedabad area, corridor, or local proof).",
        ],
    },
    "contestable_format": {
        "type": "noul",
        "instructions": "Can TenSix contest this slot with its OWN service/landing page (true), or is it a "
                        "third-party directory/marketplace/listicle TenSix must instead get LISTED in (false)?",
        "criteria": {"true": "A provider page TenSix competes with head-to-head.",
                     "false": "A directory/marketplace/listicle: get listed, don't try to outrank."},
    },
}


def _retry_http(fn):
    for attempt in range(6):
        try:
            return fn()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 502, 503, 529) or attempt == 5:
                raise
            time.sleep(2 ** attempt)


def ask_native(state, key):
    body = json.dumps({"model": TS_MODEL, "state": state, "questions": QUESTIONS}).encode()

    def call():
        req = urllib.request.Request(TS_API, body,
                                     {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)["answers"]
    return _retry_http(call)


def ask_jev_decisions(state, key):
    """Real Jev via OpenRouter's alpha decisions endpoint. Same request/response
    shape as native TypeSafe: body {model, state, questions}, response
    answers.<name>.{noul|choice|score}."""
    body = json.dumps({"model": OR_DECISIONS_MODEL, "state": state, "questions": QUESTIONS}).encode()

    def call():
        req = urllib.request.Request(OR_DECISIONS_API, body,
                                     {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)["answers"]
    return _retry_http(call)


def select_judge():
    if os.environ.get("TYPESAFE_API_KEY"):
        return ask_native, os.environ["TYPESAFE_API_KEY"], "TypeSafe System One jev-latest (calibrated)"
    if os.environ.get("OPENROUTER_API_KEY"):
        return ask_jev_decisions, os.environ["OPENROUTER_API_KEY"], "OpenRouter typesafe/jev-1.13 decisions (calibrated)"
    sys.exit("Set OPENROUTER_API_KEY or TYPESAFE_API_KEY for the Jev judge.")


# ---------------------------------------------------------------------------
# SerpAPI fetch + cache
# ---------------------------------------------------------------------------
def load_cache(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_cache(path, cache):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cache, f)


def cache_key(keyword, location, depth):
    return f"{location}|{depth}|{keyword}".lower()


# --- Apify Google Search Scraper (location-accurate, batch) -----------------
APIFY_ACTOR = "apify~google-search-scraper"


def _apify_to_serp(item, depth):
    """Normalize one Apify result-page item into the SerpAPI shape the rest of
    the pipeline expects: {"organic_results": [{position, link, title, snippet}]}."""
    organic = []
    for o in item.get("organicResults", []):
        url = o.get("url", "")
        host = urllib.parse.urlparse(url).netloc.lower()
        # drop Google's own local-pack / internal links
        if "google." in host or not host:
            continue
        pos = o.get("position")
        if pos and pos <= depth:
            organic.append({"position": len(organic) + 1, "link": url,
                            "title": o.get("title", ""), "snippet": o.get("description", "")})
    return {"organic_results": organic}


def apify_batch(keywords, location, depth, token):
    """Fetch all keywords in one Apify run. Returns {keyword_lower: serp_dict}."""
    payload = {
        "queries": "\n".join(keywords),
        "resultsPerPage": max(depth, 10),
        "maxPagesPerQuery": 1,
        "countryCode": "in",
        "languageCode": "en",
        "locationUquery": location,
    }
    url = f"https://api.apify.com/v2/acts/{APIFY_ACTOR}/run-sync-get-dataset-items?token={token}"
    req = urllib.request.Request(url, json.dumps(payload).encode(),
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        items = json.load(r)
    out = {}
    for it in items:
        term = (it.get("searchQuery", {}) or {}).get("term", "")
        if term:
            out[term.lower()] = _apify_to_serp(it, depth)
    return out


def get_serp(keyword, location, depth, api_key, cache, refresh=False):
    k = cache_key(keyword, location, depth)
    if not refresh and k in cache:
        return cache[k], True
    last = None
    for attempt in range(3):
        try:
            data = serpapi_search(keyword, location, depth, api_key)
            if "error" in data:
                raise RuntimeError(data["error"])
            cache[k] = data
            return data, False
        except (TimeoutError, OSError) as e:
            last = e
            time.sleep(3)
    raise last


def top_competitors(data, target, depth, k=10):
    rows = []
    for item in data.get("organic_results", []):
        pos = item.get("position")
        link = item.get("link", "")
        host = urllib.parse.urlparse(link).netloc.lower()
        if host.startswith("www."):
            host = host[4:]
        if pos and pos <= depth and target not in host:
            rows.append({"position": pos, "domain": host, "title": item.get("title", ""),
                         "snippet": item.get("snippet", ""), "link": link})
        if len(rows) >= k:
            break
    return rows


# ---------------------------------------------------------------------------
# GSC + GA4 ground truth (patterns from aeg-cli; optional + graceful)
# ---------------------------------------------------------------------------
def gsc_data(creds_path, site):
    """Returns {query_lower: {impressions, clicks, position}} for the last 90 days."""
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_file(
        creds_path, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    svc = build("searchconsole", "v1", credentials=creds)
    end = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    body = {"startDate": start, "endDate": end, "dimensions": ["query"], "rowLimit": 1000}
    try:
        resp = svc.searchanalytics().query(siteUrl=site, body=body).execute()
    except Exception:
        alt = site.replace("sc-domain:", "https://www.").rstrip("/") + "/" if site.startswith("sc-domain:") \
            else "sc-domain:" + urllib.parse.urlparse(site).netloc
        resp = svc.searchanalytics().query(siteUrl=alt, body=body).execute()
    out = {}
    for r in resp.get("rows", []):
        out[r["keys"][0].lower()] = {"impressions": r["impressions"], "clicks": r["clicks"],
                                     "position": r["position"]}
    return out


def ga4_data(creds_path, property_id):
    """Returns {page_path: {views, users, sessions, key_events}} for last 90 days."""
    os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", creds_path)
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import RunReportRequest, Dimension, Metric, DateRange
    client = BetaAnalyticsDataClient()
    req = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews"), Metric(name="activeUsers"),
                 Metric(name="sessions"), Metric(name="keyEvents")],
        date_ranges=[DateRange(start_date="90daysAgo", end_date="today")],
        limit=200,
    )
    resp = client.run_report(req)
    out = {}
    for r in resp.rows:
        v = r.metric_values
        out[r.dimension_values[0].value] = {"views": int(v[0].value), "users": int(v[1].value),
                                            "sessions": int(v[2].value), "key_events": int(v[3].value)}
    return out


def striking_distance(gsc_row):
    if not gsc_row:
        return "cold"  # no impressions at all — needs a page built for it
    pos = gsc_row["position"]
    if pos <= 7:
        return "ranking"
    if pos <= 30:
        return "close"  # already shown by Google, within push distance
    return "buried"  # indexed but deep (pos 31-100)


# ---------------------------------------------------------------------------
# Synthesis (code-side policy, not model)
# ---------------------------------------------------------------------------
def _n(c, q):  # noul value
    return c["ans"][q]["noul"] if c.get("ans") else 0.0


def _s(c, q):  # score value
    return c["ans"][q]["score"] if c.get("ans") else 0.0


def difficulty_label(real):
    if not real:
        return "Open (no direct competitor pages in top 10)"
    avg = sum(_s(c, "beatability") for c in real) / len(real)
    if avg >= 2.3:
        return "Winnable"
    if avg >= 1.5:
        return "Hard"
    return "Entrenched"


def synthesize(keyword, gsc_row, comps):
    real = [c for c in comps if c.get("ans") and _n(c, "contestable_format") >= 0.5]
    directories = [c for c in comps if c.get("ans") and _n(c, "contestable_format") < 0.5]
    soft = [c for c in real if _s(c, "beatability") >= 2.0]
    weak_local = [c for c in real if _s(c, "local_corridor") < 1.5]
    boilerplate = [c for c in real if _s(c, "info_density") < 1.0]
    no_envelope = [c for c in real if _n(c, "answer_envelope") < 0.5]
    no_faq = [c for c in real if _n(c, "faq_signal") < 0.5]

    sd = striking_distance(gsc_row)
    actions = []
    if sd == "close":
        actions.append(f"PRIORITY: GSC shows TenSix already at pos {gsc_row['position']:.0f} with "
                       f"{gsc_row['impressions']} impressions — a focused page upgrade can push into top 10.")
    elif sd == "buried":
        actions.append(f"GSC shows TenSix indexed but buried (pos {gsc_row['position']:.0f}) — relevance/"
                       "authority on this query is weak; needs a dedicated, specific page.")
    elif sd == "cold":
        actions.append("GSC shows zero impressions — Google does not yet see a relevant TenSix page; build one.")

    if directories:
        actions.append(f"{len(directories)} of the top slots are directories/marketplaces "
                       f"({', '.join(d['domain'] for d in directories[:3])}). Get TenSix LISTED there; "
                       "do not try to outrank them with a service page.")
    if weak_local:
        actions.append("Ranking pages show weak local signal — a page that genuinely names Ahmedabad / "
                       "Navrangpura + real local context (Layer 5) can win on relevance.")
    if boilerplate:
        actions.append("Ranking pages are generic/boilerplate — out-specify with a concrete, honest offer "
                       "(named service, clear process, fixed-price plan). Real figures only (CLAUDE.md §5).")
    if no_envelope:
        actions.append("Ranking pages lack a tight Position-0 answer — open the page with a 45–55 word direct "
                       "answer to the query (Layer 1).")
    if no_faq:
        actions.append("Ranking pages lack FAQ structure — add a visible FAQ + matching FAQPage JSON-LD "
                       "(Layers 3; CLAUDE.md §4.2) to capture PAA/dropdowns.")
    if soft:
        actions.append(f"{len(soft)} slots look soft/off-intent — realistic near-term targets.")
    if not real and not directories:
        actions.append("Top 10 is mostly off-intent/editorial — a direct, honest service page could rank with "
                       "modest effort.")
    return {"difficulty": difficulty_label(real), "striking": sd,
            "n_dir": len(directories), "n_real": len(real), "actions": actions}


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def fmt_row(c):
    if not c.get("ans"):
        return (f"| {c['position']} | {c['domain']} | (judge failed) | | | | | | |")
    a = c["ans"]
    return (f"| {c['position']} | {c['domain']} | {a['result_type']['choice']} | "
            f"{a['intent_match']['choice']} | {a['beatability']['score']:.1f} | "
            f"{a['answer_envelope']['noul']:.2f} | {a['faq_signal']['noul']:.2f} | "
            f"{a['info_density']['score']:.1f} | {a['local_corridor']['score']:.1f} | "
            f"{a['contestable_format']['noul']:.2f} |")


def render_report(results, meta):
    out = ["# TenSix Keyword Battle Plan", "",
           f"Date: {meta['date']} | Target: {meta['target']} | Location: {meta['location']} | "
           f"Depth: top-{meta['depth']}", f"Judge: {meta['judge']}",
           f"Ground truth: GSC={'on' if meta['gsc'] else 'off'}, GA4={'on' if meta['ga4'] else 'off'}", ""]
    out += ["## Summary", "",
            "| Keyword | TenSix rank | GSC (impr / pos) | Striking | Difficulty | #Dir | #Real | Top action |",
            "|---|---|---|---|---|---|---|---|"]
    for r in results:
        g = r["gsc_row"]
        gsc = f"{g['impressions']} / {g['position']:.0f}" if g else "—"
        rank = f"#{r['rank']}" if r["rank"] else "—"
        top = r["syn"]["actions"][0] if r["syn"]["actions"] else ""
        out.append(f"| {r['keyword']} | {rank} | {gsc} | {r['syn']['striking']} | "
                   f"{r['syn']['difficulty']} | {r['syn']['n_dir']} | {r['syn']['n_real']} | {top} |")
    out.append("")
    for r in results:
        out += [f"## {r['keyword']}", "",
                f"**TenSix rank:** {'#' + str(r['rank']) if r['rank'] else 'not in top-' + str(meta['depth'])}  "
                f"| **Difficulty:** {r['syn']['difficulty']}  | **Striking distance:** {r['syn']['striking']}", ""]
        if r["gsc_row"]:
            g = r["gsc_row"]
            out.append(f"GSC (90d): {g['impressions']} impressions, {g['clicks']} clicks, "
                       f"avg position {g['position']:.1f}.")
            out.append("")
        out += ["### Top competitors", "",
                "| Pos | Domain | Type | Intent | Beatable(0-3) | AnsEnv | FAQ | Density(0-2) | Local(0-3) | Contestable |",
                "|---|---|---|---|---|---|---|---|---|---|"]
        out += [fmt_row(c) for c in r["comps"]]
        out += ["", "### What TenSix must do to rank"]
        out += [f"- {a}" for a in r["syn"]["actions"]]
        out.append("")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keywords", help='Semicolon-separated subset, e.g. "a;b"')
    ap.add_argument("--only-money", action="store_true", help="Use the top-10 money keyword set")
    ap.add_argument("--limit", type=int, help="Only the first N keywords")
    ap.add_argument("--depth", type=int, default=10)
    ap.add_argument("--location", default="India")
    ap.add_argument("--target", default=TARGET_DEFAULT)
    ap.add_argument("--top-k", type=int, default=10)
    ap.add_argument("--refresh-cache", action="store_true")
    ap.add_argument("--no-cache-write", action="store_true")
    ap.add_argument("--delay", type=float, default=0.5)
    ap.add_argument("--creds", default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
    ap.add_argument("--gsc-site", default="sc-domain:tensix.in")
    ap.add_argument("--ga4-property", default=os.environ.get("GA4_PROPERTY_ID"))
    ap.add_argument("--no-gsc", action="store_true")
    ap.add_argument("--no-ga4", action="store_true")
    ap.add_argument("--provider", choices=["serpapi", "apify"], default="serpapi",
                    help="SERP source. apify = location-accurate batch via Apify Google Search Scraper.")
    ap.add_argument("--dry-run", action="store_true", help="Print one Jev request + quota estimate; no calls")
    ap.add_argument("--serp-only", action="store_true", help="Fetch SERP + ranks only; no Jev")
    return ap.parse_args()


def resolve_keywords(args):
    if args.keywords:
        kws = [k.strip() for k in args.keywords.split(";") if k.strip()]
    elif args.only_money:
        kws = list(MONEY_KEYWORDS)
    else:
        kws = list(KEYWORDS)
    if args.limit:
        kws = kws[:args.limit]
    return kws


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = parse_args()
    kws = resolve_keywords(args)

    if args.dry_run:
        sample = {"keyword": kws[0], "tensix_rank": None, "tensix_gsc": None, "position": 1,
                  "title": "Example Competitor — Software Development Company",
                  "snippet": "We build custom software for businesses across India.", "domain": "example.com"}
        print("=== DRY RUN: one Jev request body ===")
        print(json.dumps({"model": OR_DECISIONS_MODEL, "state": sample, "questions": QUESTIONS}, indent=2)[:3500])
        cache = load_cache(SERP_CACHE)
        cached = sum(1 for k in kws if cache_key(k, args.location, args.depth) in cache)
        print(f"\nKeywords: {len(kws)} | cached SERPs: {cached} | live SerpAPI calls needed: {len(kws) - cached}")
        print(f"Jev judgments needed: ~{len(kws) * args.top_k}")
        return

    cache = load_cache(SERP_CACHE)

    serp_key = os.environ.get("SERPAPI_KEY")
    if args.provider == "apify":
        token = os.environ.get("APIFY_TOKEN")
        if not token:
            sys.exit('Set APIFY_TOKEN for --provider apify.')
        pending = [k for k in kws
                   if args.refresh_cache or cache_key(k, args.location, args.depth) not in cache]
        if pending:
            print(f"Apify: fetching {len(pending)} keyword(s) at location '{args.location}'...")
            batch = apify_batch(pending, args.location, args.depth, token)
            for kw in pending:
                data = batch.get(kw.lower())
                if data is not None:
                    cache[cache_key(kw, args.location, args.depth)] = data
                else:
                    print(f"  WARN  Apify returned no result for: {kw}")
            if not args.no_cache_write:
                save_cache(SERP_CACHE, cache)
    elif not serp_key:
        sys.exit('Set SERPAPI_KEY (e.g. $env:SERPAPI_KEY = "...").')

    # Optional ground truth
    gsc = ga4 = None
    if not args.no_gsc and args.creds:
        try:
            gsc = gsc_data(args.creds, args.gsc_site)
            print(f"GSC: {len(gsc)} queries loaded for {args.gsc_site}")
        except Exception as e:
            print(f"GSC skipped: {e}")
    if not args.no_ga4 and args.creds and args.ga4_property:
        try:
            ga4 = ga4_data(args.creds, args.ga4_property)
            print(f"GA4: {len(ga4)} pages loaded for property {args.ga4_property}")
        except Exception as e:
            print(f"GA4 skipped: {e}")

    judge = key = judge_name = None
    if not args.serp_only:
        judge, key, judge_name = select_judge()
        print(f"Judge: {judge_name}")

    results = []
    for kw in kws:
        if args.provider == "apify":
            # Apify batch already populated the cache; a miss means no result.
            data = cache.get(cache_key(kw, args.location, args.depth))
            if data is None:
                print(f"  ERR  {kw}  (no Apify result)")
                continue
            from_cache = True
        else:
            try:
                data, from_cache = get_serp(kw, args.location, args.depth, serp_key, cache,
                                            refresh=args.refresh_cache)
            except Exception as e:
                print(f"  ERR  {kw}  (SERP: {e})")
                continue
        if not from_cache and not args.no_cache_write:
            save_cache(SERP_CACHE, cache)
        rank, _ = rank_of(args.target, data.get("organic_results", []), args.depth)
        comps = top_competitors(data, args.target, args.depth, args.top_k)
        gsc_row = gsc.get(kw.lower()) if gsc else None

        if not args.serp_only:
            for c in comps:
                state = {"keyword": kw, "tensix_rank": rank,
                         "tensix_gsc": gsc_row, "position": c["position"],
                         "title": c["title"], "snippet": c["snippet"], "domain": c["domain"]}
                try:
                    c["ans"] = judge(state, key)
                except Exception as e:
                    c["ans"] = None
                    print(f"       judge failed for {c['domain']}: {e}")
                time.sleep(args.delay)

        syn = synthesize(kw, gsc_row, comps) if not args.serp_only else \
            {"difficulty": "-", "striking": striking_distance(gsc_row), "n_dir": 0,
             "n_real": 0, "actions": []}
        results.append({"keyword": kw, "rank": rank, "gsc_row": gsc_row, "comps": comps, "syn": syn})
        src = "cache" if from_cache else "live"
        print(f"  {'#' + str(rank) if rank else '--':>5}  {kw}  ({len(comps)} comps, {src}) "
              f"[{syn['striking']}/{syn['difficulty']}]")

    if not args.no_cache_write:
        save_cache(SERP_CACHE, cache)

    meta = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "target": args.target,
            "location": args.location, "depth": args.depth,
            "judge": judge_name or "(serp-only)", "gsc": bool(gsc), "ga4": bool(ga4)}
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    out = os.path.join(ROOT, f"keyword_battle_plan_{stamp}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(render_report(results, meta))
    print(f"\nReport saved: {out}")


if __name__ == "__main__":
    main()
