"""Build the agent-facing files from the production HTML pages (stdlib only).

Writes: md/<path>.md, llms.txt, llms-full.txt, sitemap.xml, sitemap_index.xml,
and the SKILL.md sha256 digest in .well-known/agent-skills/index.json.
Run before validate_schemas.py / screaming_frog_audit.py. Deterministic and idempotent.

Usage: python build_agent_files.py [YYYY-MM-DD]   (default date for uncommitted files)
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.tensix.in/"
TODAY = sys.argv[1] if len(sys.argv) > 1 else "2026-10-05"
SKIP_DIRS = ("hk", "skills", "resources", "assets", "node_modules", ".git", "09_Archive")

CORE = [
    "index.html", "about.html", "services.html", "work.html", "case-studies.html",
    "contact.html", "hemal-shah.html", "team.html", "frameworks.html", "gallery.html",
    "resources.html", "tensix-vs-traditional-agencies.html", "blogs.html",
]
LOCAL = [
    "software-company-in-navrangpura-ahmedabad.html", "ahmedabad-software-engineering.html",
    "saas-developer-ahmedabad.html", "best-software-company-in-gota.html",
    "hk-engineering-ahmedabad.html",
]


def discover():
    """Same discovery rules as screaming_frog_audit.py."""
    pages = []
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".html") and not f.startswith("google") and not f.startswith("rajputbhavin"):
                pages.append(os.path.relpath(os.path.join(dirpath, f), ROOT).replace("\\", "/"))
    return sorted(pages)


def page_url(rel):
    return SITE + ("" if rel == "index.html" else rel[:-5])


def canonical_href(href, base):
    """Absolute URL; internal links become www + extensionless."""
    if href.startswith(("mailto:", "tel:")):
        return href
    if href.startswith("javascript:"):
        return ""
    u = urlparse(urljoin(base, href))
    if u.netloc not in ("tensix.in", "www.tensix.in"):
        return u.geturl()
    path = u.path
    if path.endswith(".html"):
        path = path[:-5]
    if path in ("/index", ""):
        path = "/"
    return "https://www.tensix.in" + path + ("?" + u.query if u.query else "") + ("#" + u.fragment if u.fragment else "")


DROP = {"script", "style", "nav", "header", "footer", "svg", "noscript", "button", "form",
        "template", "iframe", "select", "textarea"}
BLOCK = {"p", "div", "section", "article", "aside", "blockquote", "figure", "figcaption",
         "dl", "dt", "dd", "details", "summary", "address", "hr"}
WRAP = {"strong": "**", "b": "**", "em": "*", "i": "*", "code": "`"}


class Page(HTMLParser):
    def __init__(self, html, base):
        super().__init__(convert_charrefs=True)
        self.base = base
        self.scope = "main" if re.search(r"<main[\s>]", html, re.I) else "body"
        self.active = False
        self.skip = 0
        self.pre = False
        self.out = []
        self.stack = []      # (tag, start index, extra) for inline wrappers / links / cells
        self.lists = []      # [kind, counter]
        self.row = None
        self.rows = 0
        self.title = ""
        self.in_title = False
        self.description = ""
        self.feed(html)
        self.close()

    def blank(self):
        self.out.append("\n\n")

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "meta" and (a.get("name") or "").lower() == "description":
            self.description = a.get("content") or ""
        if tag == self.scope:
            self.active = True
            return
        if not self.active:
            return
        if self.skip or tag in DROP:
            if tag in DROP:
                self.skip += 1
            return
        if re.fullmatch(r"h[1-6]", tag):
            self.blank()
            self.out.append("#" * int(tag[1]) + " ")
        elif tag in BLOCK or tag == "table":
            self.blank()
            if tag == "table":
                self.rows = 0
        elif tag in ("ul", "ol"):
            self.out.append("\n" if self.lists else "\n\n")
            self.lists.append([tag, 0])
        elif tag == "li":
            depth = max(len(self.lists), 1)
            marker = "- "
            if self.lists and self.lists[-1][0] == "ol":
                self.lists[-1][1] += 1
                marker = f"{self.lists[-1][1]}. "
            self.out.append("\n" + "  " * (depth - 1) + marker)
        elif tag == "br":
            self.out.append("\n")
        elif tag == "pre":
            self.blank()
            self.out.append("```\n")
            self.pre = True
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.stack.append((tag, len(self.out), None))
        elif tag == "a":
            self.stack.append((tag, len(self.out), canonical_href(a.get("href") or "", self.base)))
        elif tag in WRAP and not (tag == "code" and self.pre):
            self.stack.append((tag, len(self.out), None))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if not self.active:
            return
        if tag == self.scope:
            self.active = False
            return
        if self.skip:
            if tag in DROP:
                self.skip -= 1
            return
        if re.fullmatch(r"h[1-6]", tag) or tag in BLOCK:
            self.blank()
        elif tag in ("ul", "ol"):
            if self.lists:
                self.lists.pop()
            if not self.lists:
                self.blank()
        elif tag == "pre":
            self.out.append("\n```")
            self.blank()
            self.pre = False
        elif tag == "tr" and self.row is not None:
            if self.row:
                self.out.append("| " + " | ".join(self.row) + " |\n")
                if self.rows == 0:
                    self.out.append("|" + " --- |" * len(self.row) + "\n")
                self.rows += 1
            self.row = None
        elif tag == "table":
            self.blank()
        elif self.stack and self.stack[-1][0] == tag:
            _, idx, extra = self.stack.pop()
            text = "".join(self.out[idx:])
            del self.out[idx:]
            if tag in ("td", "th"):
                if self.row is not None:
                    self.row.append(re.sub(r"\s+", " ", text).strip().replace("|", "\\|"))
                return
            core = text.strip()
            if not core:
                self.out.append(text)
                return
            lead = text[: len(text) - len(text.lstrip())]
            trail = text[len(text.rstrip()):]
            if tag == "a":
                core = re.sub(r"\s*\n\s*", " ", core)
                wrapped = f"[{core}]({extra})" if extra else core
            else:
                wrapped = WRAP[tag] + core + WRAP[tag]
            self.out.append(lead + wrapped + trail)

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if not self.active or self.skip:
            return
        self.out.append(data if self.pre else re.sub(r"\s+", " ", data))

    def markdown(self):
        lines, fenced = [], False
        for line in "".join(self.out).split("\n"):
            if line.strip().startswith("```"):
                fenced = not fenced
                lines.append(line.strip())
                continue
            if fenced:
                lines.append(line.rstrip())
                continue
            line = line.rstrip()
            if not re.match(r"\s*(- |\d+\. )", line):
                line = line.lstrip()
            lines.append(re.sub(r"(?<=\S) {2,}", " ", line))
        text = "\n".join(lines)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return re.sub(r"^(#+ |- |\d+\. )\s*$", "", text, flags=re.M).strip()


def clean(s):
    return re.sub(r"\s+", " ", s).strip()


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def git_dates(pages):
    dirty = set()
    try:
        st = subprocess.run(["git", "status", "--porcelain", "-uall"], cwd=ROOT,
                            capture_output=True, text=True, encoding="utf-8").stdout
        for line in st.splitlines():
            dirty.add(line[3:].strip().strip('"').replace("\\", "/"))
    except OSError:
        return {p: TODAY for p in pages}
    dates = {}
    for p in pages:
        d = ""
        if p not in dirty:
            d = subprocess.run(["git", "log", "-1", "--format=%cs", "--", p], cwd=ROOT,
                               capture_output=True, text=True).stdout.strip()
        dates[p] = d or TODAY
    return dates


def main():
    pages = discover()
    services = [p for p in pages if p.startswith("services/")]
    blogs = [p for p in pages if p.startswith("blogs/")]
    core = [p for p in CORE if p in pages]
    local = [p for p in LOCAL if p in pages]
    rest = [p for p in pages if p not in core + local + services + blogs]
    core += rest
    order = core + services + local + blogs

    info = {}
    for rel in order:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            html = f.read()
        url = page_url(rel)
        pg = Page(html, SITE + rel)
        title, desc = clean(pg.title), clean(pg.description)
        body = pg.markdown()
        md = (f"---\ntitle: {json.dumps(title, ensure_ascii=False)}\nurl: {url}\n"
              f"description: {json.dumps(desc, ensure_ascii=False)}\n---\n\n{body}\n")
        write("md/" + rel[:-5] + ".md", md)
        label = re.sub(r"\s*\|\s*TENSIX$", "", title)
        info[rel] = (url, label, desc, md)

    # Remove stale mirrors of pages that no longer exist
    want = {os.path.normpath(os.path.join(ROOT, "md", r[:-5] + ".md")) for r in order}
    for dirpath, _, files in os.walk(os.path.join(ROOT, "md")):
        for f in files:
            p = os.path.normpath(os.path.join(dirpath, f))
            if p not in want:
                os.remove(p)

    # llms.txt
    def section(name, rels):
        return [f"## {name}"] + [f"- [{info[r][1]}]({info[r][0]}): {info[r][2]}" for r in rels] + [""]

    llms = [
        "# TENSIX — Software, AI and Websites from Ahmedabad",
        "",
        "> TENSIX (https://www.tensix.in/) is a one-person software and AI studio in Navrangpura, "
        "Ahmedabad, Gujarat, India, founded and run by Hemal Shah. It builds websites, custom software "
        "and SaaS, AI agents and assistants, cloud and DevOps setups, email deliverability, data "
        "scraping and automation, and AI search visibility (GEO/AEO/SEO), at fixed prices in INR.",
        "",
    ]
    llms += section("Core pages", core)
    llms += section("Services", services)
    llms += section("Local pages", local)
    llms += section("Guides & articles", blogs)
    llms += [
        "## Machine-readable",
        f"- [Full text of every page]({SITE}llms-full.txt): All pages as Markdown in one file.",
        f"- [OpenAPI description]({SITE}openapi.json): OpenAPI 3.1 for POST /api/contact (send a project inquiry).",
        f"- [Agent Skills index]({SITE}.well-known/agent-skills/index.json): Skill for picking a service and plan and requesting a quote.",
        "- Every page is also available as Markdown: send `Accept: text/markdown` to the page URL, "
        f"or fetch {SITE}md/<path>.md (for example {SITE}md/index.md, {SITE}md/services/cloud-devops.md).",
        "",
    ]
    write("llms.txt", "\n".join(llms))

    # llms-full.txt
    full = [
        "# TENSIX — full text of www.tensix.in",
        "",
        "> Every production page as Markdown. One-person software and AI studio in Navrangpura, "
        "Ahmedabad, India, founded and run by Hemal Shah. Canonical: https://www.tensix.in/",
        "",
    ]
    for rel in order:
        full += [f"--- Page: {info[rel][0]} ---", "", info[rel][3]]
    write("llms-full.txt", "\n".join(full))

    # sitemap.xml + sitemap_index.xml
    dates = git_dates(order)

    def priority(rel):
        if rel == "index.html":
            return "1.0"
        if rel == "services.html" or rel.startswith("services/"):
            return "0.9"
        return "0.7" if rel.startswith("blogs/") else "0.8"

    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for rel in order:
        sm += ["  <url>", f"    <loc>{info[rel][0]}</loc>", f"    <lastmod>{dates[rel]}</lastmod>",
               f"    <priority>{priority(rel)}</priority>", "  </url>"]
    sm += ["</urlset>", ""]
    write("sitemap.xml", "\n".join(sm))
    write("sitemap_index.xml", "\n".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        "  <sitemap>", f"    <loc>{SITE}sitemap.xml</loc>", f"    <lastmod>{TODAY}</lastmod>",
        "  </sitemap>", "</sitemapindex>", ""]))

    # Agent Skills digest
    idx_path = os.path.join(ROOT, ".well-known", "agent-skills", "index.json")
    with open(idx_path, encoding="utf-8") as f:
        idx = json.load(f)
    for skill in idx.get("skills", []):
        rel = urlparse(skill["url"]).path.lstrip("/")
        with open(os.path.join(ROOT, rel), "rb") as f:
            skill["digest"] = "sha256:" + hashlib.sha256(f.read()).hexdigest()
    write(".well-known/agent-skills/index.json", json.dumps(idx, indent=2, ensure_ascii=False) + "\n")

    print(f"Pages: {len(order)} (core {len(core)}, services {len(services)}, "
          f"local {len(local)}, blogs {len(blogs)})")
    print("Wrote md/*.md, llms.txt, llms-full.txt, sitemap.xml, sitemap_index.xml, agent-skills digest.")


if __name__ == "__main__":
    main()
