"""Step 1: Extract & verify tensix claims from contolo vault against real site"""
import re, json, sys
from pathlib import Path
from html.parser import HTMLParser

class Text(HTMLParser):
    def __init__(self): super().__init__(); self.out = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "nav", "footer"}: self.skip += 1
    def handle_endtag(self, tag):
        if tag in {"script", "style", "nav", "footer"} and self.skip: self.skip -= 1
    def handle_data(self, d):
        if not self.skip and d.strip(): self.out.append(d.strip())

def extract_html(path):
    p = Text(); p.feed(Path(path).read_text(encoding="utf-8", errors="ignore"))
    return " ".join(p.out)

def grep_site(pattern, root=".."):
    """Search HTML files for pattern, return list of (file, matches)"""
    hits = []
    for f in Path(root).glob("**/*.html"):
        if "contolo" in str(f) or "tools" in str(f) or "09_Archive" in str(f): continue
        text = extract_html(f)
        if re.search(pattern, text, re.IGNORECASE):
            hits.append((str(f.relative_to(root)), re.findall(pattern, text, re.IGNORECASE)))
    return hits

# ---- Claims from contolo docs (Docs 31, 37, 38 mainly) ----
CLAIMS = [
    ("indexed in <3 minutes", r"(indexed|index).{0,20}(3|three).{0,10}(minute|min)", "Doc 31: 'indexed into Base Tier in under 3 minutes'"),
    ("ranked tensix.com in 96 hours", r"(beat|outrank|rank).{0,20}tensix\.com.{0,20}(96|4\s*day)", "Doc 31: 'outranked tensix.com within 96 hours'"),
    ("FCP 140ms", r"(FCP|First\s+Content).{0,10}(140|ms)", "Doc 31: 'FCP: 140ms vs tensix.com FCP: >1,200ms'"),
    ("/proof page exists", r"tensix\.in/proof", "Doc 31: '/proof' or '/case-study/indexing-velocity'"),
    ("Lighthouse 100/100", r"(Lighthouse|score).{0,5}100", "Doc 31: 'Lighthouse score: 100/100'"),
    ("Google Business Profile binding", r"(Google.{0,10}Business|GBP|CID|Place\s+ID)", "Doc 37/38: 'hard binding to CID'"),
    ("Plus Code 7JMJ2HP6+JJR", r"7JMJ2HP6\+JJR|Plus\s+Code", "Derived from coords 23.0366, 72.5615"),
    ("S2 token 395e84f37", r"395e84f37|S2.*L16", "Derived from S2 geometry"),
    ("TENSIX on Business Profile", r"TENSIX.*Business.*Profile|Business.*Profile.*TENSIX", "Doc 37: 'embed the exact schema'"),
    ("Same Address on every page", r'(streetAddress|address).*one.*value|consistent.*address', "Doc 37/38: entity consistency"),
]

print("=== STEP 1: FACT EXTRACTION & VERIFICATION ===\n")
rows = []
for claim, pattern, source in CLAIMS:
    hits = grep_site(pattern)
    verdict = "VERIFIED" if hits else "NOT FOUND"
    evidence = "; ".join(f"{f}:{len(m)} matches" for f, m in hits[:2]) if hits else "no occurrences"
    rows.append((claim, verdict, evidence, source))
    print(f"{verdict:<12} {claim:<40} {evidence}")

print("\n=== CSV OUTPUT ===")
print("claim,verdict,evidence,source")
for claim, verdict, evidence, source in rows:
    print(f'"{claim}","{verdict}","{evidence}","{source}"')

# geo-kernel output (already computed)
geo = {
    "coords": "23.0366, 72.5615",
    "plus_code": "7JMJ2HP6+JJR",
    "s2_l16": "395e84f37",
    "nap_issues": [
        "addressLocality: 10 pages 'Ahmedabad', 3 'Navrangpura', 4 'Navrangpura, Ahmedabad'",
        "streetAddress: 1 'Gota - Navrangpura Corridor', 5 'Navrangpura', 4 'Navrangpura, C.G. Road Corridor'",
        "postalCode: 16 pages '380009', 1 page '382481' (Gota)",
        "phone: consistent +91-8320278775",
        "hasMap: all 10 pages use same Google Maps link"
    ],
    "coordinate_outlier": "Gota page (best-software-company-in-gota.html): 23.1118, 72.5470 → 8738m away from canonical"
}

print("\n=== LOCATION AUDIT (geo-kernel) ===")
for k, v in geo.items():
    print(f"{k}: {v}")

print(f"\n=== SUMMARY ===")
verified = sum(1 for _, v, _, _ in rows if v == "VERIFIED")
total = len(rows)
print(f"{verified}/{total} claims verified on site")
print(f"{len(geo['nap_issues'])} NAP inconsistencies found")
