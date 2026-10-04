"""AI-citation readiness audit for every page in sitemap.xml, using TypeSafe System One (Jev).

Code owns the workflow (parse pages, apply policy); Jev supplies the semantic judgments.
Stdlib only. Usage:
    $env:TYPESAFE_API_KEY="..."; python citation_audit.py            # audit all pages
    python citation_audit.py --dry-run                               # print one request, no API call
Writes citation_audit.md. Thresholds below are starting points: tune them on your own results.
"""
import json, os, re, sys, time, urllib.request, urllib.error
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).parent
API = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"
INTRO_CHARS = 1500  # AI answer engines quote short passages; judge the opening, not the whole page.

QUESTIONS = {
    "answers_first": {
        "type": "noul",
        "instructions": "Does `intro` directly answer the question a searcher typing `query` is asking, "
                        "in a self-contained statement that could be quoted on its own without the rest of the page?",
        "criteria": {"true": "A quotable direct answer to the query appears in the intro.",
                     "false": "The intro is a slogan, navigation, or preamble, or never answers the query."},
    },
    "entity_clear": {
        "type": "noul",
        "instructions": "Could a reader of `intro` alone state who is speaking (the company or person by name), "
                        "what they do, and where they are based?",
        "criteria": {"true": "Name, what it does, and location are all explicit in the intro.",
                     "false": "At least one of name, offering, or location is missing or only implied."},
    },
    "specificity": {
        "type": "score",
        "instructions": "How concrete and checkable are the claims in `intro`?",
        "criteria": [
            "Only generic marketing language; nothing a reader could verify.",
            "Some concrete details (named technologies or services) but no numbers, dates, or outcomes.",
            "Concrete, checkable facts: specific numbers, dates, named tools, or measured outcomes.",
        ],
    },
    "unsupported_superlative": {
        "type": "noul",
        "instructions": "Does `intro` make a superlative or guarantee claim (best, fastest, #1, guaranteed, "
                        "elite) that the intro itself gives no evidence for?",
        "criteria": {"true": "Contains an unbacked superlative or guarantee.",
                     "false": "No such claim, or every such claim is backed by evidence in the intro."},
    },
    "intent": {
        "type": "choice",
        "instructions": "What search intent does `query` represent?",
        "criteria": {
            "informational": "Wants to learn or understand something.",
            "commercial": "Comparing providers or evaluating whether to hire or buy.",
            "local": "Wants a provider in a specific city or neighbourhood.",
            "navigational": "Looking for this specific brand or person.",
            "unclear": "None of the above clearly fits.",
        },
    },
}

# Policy lives in code so it can change without re-running inference.
def verdict(a):
    issues = []
    if a["answers_first"]["noul"] < 0.5: issues.append("intro does not answer the query")
    if a["entity_clear"]["noul"] < 0.5: issues.append("who/what/where not explicit")
    if a["specificity"]["score"] < 1.2: issues.append("claims too generic")
    if a["unsupported_superlative"]["noul"] >= 0.6: issues.append("unbacked superlative/guarantee")
    return issues


class Text(HTMLParser):
    SKIP = {"script", "style", "nav", "header", "footer", "noscript", "svg"}
    def __init__(self):
        super().__init__(); self.depth = 0; self.out = []; self.title = ""; self._t = False
    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP: self.depth += 1
        self._t = tag == "title"
    def handle_endtag(self, tag):
        if tag in self.SKIP and self.depth: self.depth -= 1
        self._t = False
    def handle_data(self, d):
        if self._t: self.title += d
        elif not self.depth and d.strip(): self.out.append(d.strip())


def page(path):
    p = Text(); p.feed(path.read_text(encoding="utf-8", errors="ignore"))
    intro = re.sub(r"\s+", " ", " ".join(p.out))[:INTRO_CHARS]
    # The title is the best available proxy for the query a page targets.
    query = re.split(r"\s[|\-–—]\s", p.title.strip())[0] or path.stem.replace("-", " ")
    return {"url": path.relative_to(ROOT).as_posix(), "query": query, "intro": intro}


def ask(state, key):
    body = json.dumps({"model": MODEL, "state": state, "questions": QUESTIONS}).encode()
    for attempt in range(6):
        req = urllib.request.Request(API, body, {"Authorization": f"Bearer {key}",
                                                 "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)["answers"]
        except urllib.error.HTTPError as e:
            if e.code not in (429, 529) or attempt == 5: raise
            time.sleep(2 ** attempt)  # docs: exponential backoff on 429/529


def ask_openrouter(state, key):
    """Fallback: OpenRouter's typesafe/jev-router routes to a chat model, so these numbers are
    self-reported, NOT calibrated System One probabilities. Same answer shape as the native API."""
    spec = {q: ("probability 0-1 that the answer is yes" if v["type"] == "noul" else
                f"number 0-{len(v['criteria']) - 1} (fractions allowed)" if v["type"] == "score" else
                "one of " + "|".join(v["criteria"])) for q, v in QUESTIONS.items()}
    prompt = (f"STATE:\n{json.dumps(state, ensure_ascii=False)}\n\nQUESTIONS:\n{json.dumps(QUESTIONS, ensure_ascii=False)}"
              f"\n\nReturn only a JSON object with these keys and value types: {json.dumps(spec)}")
    body = json.dumps({"model": "typesafe/jev-router", "messages": [{"role": "user", "content": prompt}],
                       "response_format": {"type": "json_object"}, "temperature": 0}).encode()
    for attempt in range(6):
        req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", body,
                                     {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                raw = json.loads(re.search(r"\{.*\}", json.load(r)["choices"][0]["message"]["content"], re.S)[0])
            break
        except urllib.error.HTTPError as e:
            if e.code not in (429, 502, 503, 529) or attempt == 5: raise
            time.sleep(2 ** attempt)
    kind = {"noul": "noul", "score": "score", "choice": "choice"}
    return {q: {kind[v["type"]]: (raw[q] if v["type"] == "choice" else float(raw[q]))} for q, v in QUESTIONS.items()}


def pages():
    locs = re.findall(r"<loc>https://[^/]+/([^<]*)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
    for loc in locs:
        f = ROOT / (loc or "index.html")
        if f.suffix != ".html": f = f.with_suffix(".html")
        if f.exists(): yield f


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    files = list(pages())
    if "--dry-run" in sys.argv:
        print(json.dumps({"model": MODEL, "state": page(files[0]), "questions": QUESTIONS}, indent=2)[:4000])
        return print(f"\n{len(files)} pages would be audited.")
    if os.environ.get("TYPESAFE_API_KEY"):
        key, judge, source = os.environ["TYPESAFE_API_KEY"], ask, "TypeSafe System One (calibrated)"
    elif os.environ.get("OPENROUTER_API_KEY"):
        key, judge, source = os.environ["OPENROUTER_API_KEY"], ask_openrouter, "OpenRouter jev-router (NOT calibrated)"
    else:
        sys.exit("Set TYPESAFE_API_KEY or OPENROUTER_API_KEY (server-side only, never commit it).")
    print(f"Judge: {source}")

    rows = []
    for f in files:
        s = page(f); a = judge(s, key); issues = verdict(a)
        rows.append((len(issues), s, a, issues))
        print(f"{'OK ' if not issues else 'FIX'} {s['url']}: {', '.join(issues) or 'citation-ready'}")

    rows.sort(key=lambda r: -r[0])
    out = ["# AI-Citation Readiness Audit", "", f"Judge: {source}", "",
           "| Page | Target query | Intent | Answers first | Entity clear | Specificity (0-2) | Unbacked claim | Fix |",
           "|---|---|---|---|---|---|---|---|"]
    for _, s, a, issues in rows:
        out.append(f"| {s['url']} | {s['query']} | {a['intent']['choice']} | {a['answers_first']['noul']:.2f} | "
                   f"{a['entity_clear']['noul']:.2f} | {a['specificity']['score']:.2f} | "
                   f"{a['unsupported_superlative']['noul']:.2f} | {'; '.join(issues) or 'none'} |")
    (ROOT / "citation_audit.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"\n{sum(1 for r in rows if r[0])}/{len(rows)} pages need work. Report: citation_audit.md")


if __name__ == "__main__":
    main()
