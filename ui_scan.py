#!/usr/bin/env python3
"""
Fast async UI/UX scan of every sitemap page, desktop + mobile, all pages in parallel.
Collects every visible text block (with font size, line-height, contrast, width) and
flags UI/UX problems (rules from ui-ux-pro-max: contrast 4.5, body line-height 1.5-1.75,
touch targets 44px, readable line length, no horizontal overflow, naked lists).

Run:  python ui_scan.py            -> ui_scan/texts.md, ui_scan/findings.md, ui_scan/data.json
"""
import asyncio, http.server, json, os, sys, threading, xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from functools import partial
from urllib.parse import urlparse
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "ui_scan")
PORT, CONCURRENCY = 8766, 12
VIEWPORTS = {"desktop": dict(viewport={"width": 1440, "height": 900}),
             "mobile": dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)}

JS = r"""
() => {
  document.querySelectorAll('.reveal,.reveal-blur,.reveal-left,.reveal-right,.reveal-scale').forEach(e => e.classList.add('active'));
  const W = document.documentElement.clientWidth;
  const parse = c => { const m = c.match(/[\d.]+/g); return m ? m.map(Number) : [0,0,0,0]; };
  const lum = ([r,g,b]) => { const f = v => (v/=255) <= .03928 ? v/12.92 : ((v+.055)/1.055)**2.4; return .2126*f(r)+.7152*f(g)+.0722*f(b); };
  const bgOf = el => {  // first opaque ancestor background; null if gradient/image (can't judge)
    for (let e = el; e; e = e.parentElement) {
      const s = getComputedStyle(e);
      if (s.backgroundImage !== 'none') return null;
      const [r,g,b,a=1] = parse(s.backgroundColor);
      if (a > .95) return [r,g,b];
    }
    return [255,255,255];
  };
  const out = {texts: [], issues: [], overflow: 0, h1: document.querySelectorAll('h1').length};
  out.overflow = Math.max(0, document.documentElement.scrollWidth - W);
  const seen = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const n = walker.currentNode, t = n.textContent.replace(/\s+/g,' ').trim();
    const el = n.parentElement;
    if (!t || /^(SCRIPT|STYLE|NOSCRIPT|SVG|PATH)$/i.test(el.tagName) || el.closest('script,style,noscript,svg')) continue;
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    if (s.display === 'none' || s.visibility === 'hidden' || r.width === 0 || r.height === 0) continue;
    const block = el.closest('p,li,h1,h2,h3,h4,h5,h6,td,th,dd,dt,label,summary,figcaption,button,a,div') || el;
    if (seen.has(block) && !/^(A|SPAN|B|STRONG|EM|CODE)$/.test(el.tagName) ) continue;
    seen.add(block);
    const fs = parseFloat(s.fontSize), lh = s.lineHeight === 'normal' ? 1.2 : parseFloat(s.lineHeight)/fs;
    const fg = parse(s.color), bg = bgOf(el);
    let cr = null;
    if (bg) { const a = lum(fg)+.05, b = lum(bg)+.05; cr = +(Math.max(a,b)/Math.min(a,b)).toFixed(2); }
    const sec = el.closest('section,header,footer,nav,main');
    const rec = {tag: el.tagName.toLowerCase(), cls: (el.className && el.className.baseVal === undefined ? el.className : '').toString().slice(0,60),
      sec: sec ? (sec.id || sec.className.toString().split(' ')[0] || sec.tagName.toLowerCase()) : '',
      text: t.slice(0,200), fs, lh: +lh.toFixed(2), cr, w: Math.round(r.width), x: Math.round(r.left), y: Math.round(r.top + scrollY)};
    out.texts.push(rec);
    const flag = (k, m) => out.issues.push({k, m, tag: rec.tag, cls: rec.cls, sec: rec.sec, text: t.slice(0,80)});
    if (fs < (W < 600 ? 14 : 12) && t.length > 3) flag('small-font', fs + 'px');
    if (cr !== null && cr < 4.5 && fs < 24) flag('low-contrast', cr + ':1');
    if (t.length > 90 && lh < 1.4 && !/^H\d$/i.test(el.tagName)) flag('tight-leading', rec.lh);
    if (t.length > 200 && r.width / (fs * .5) > 90) flag('long-line', Math.round(r.width/(fs*.5)) + ' chars');
    if (el.scrollWidth > el.clientWidth + 2 && ['hidden','clip'].includes(s.overflowX) && el.clientWidth > 0) flag('clipped-text', el.scrollWidth + '>' + el.clientWidth);
    if (r.right > W + 2 || r.left < -2) flag('offscreen-text', Math.round(r.left) + '..' + Math.round(r.right));
    if (t.split(' ').length > 75 && el.tagName === 'P') flag('wall-of-text', t.split(' ').length + ' words');
  }
  document.querySelectorAll('a,button,summary,input,select,textarea').forEach(el => {
    const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    if (!r.width || s.display === 'none' || s.visibility === 'hidden') return;
    if ((r.height < 40 || r.width < 40) && !(el.tagName === 'A' && el.closest('p,li') && el.textContent.trim().length > 12 && s.display === 'inline'))
      out.issues.push({k: 'tap-target', m: Math.round(r.width)+'x'+Math.round(r.height), tag: el.tagName.toLowerCase(), cls: el.className.toString().slice(0,60), sec: '', text: (el.textContent||el.ariaLabel||'').trim().slice(0,60)});
  });
  document.querySelectorAll('ul,ol,dl').forEach(el => {
    if (el.closest('nav,footer,header')) return;
    const s = getComputedStyle(el), li = el.children[0] && getComputedStyle(el.children[0]);
    const styled = s.listStyleType === 'none' ? (li && (li.backgroundColor !== 'rgba(0, 0, 0, 0)' || li.borderTopWidth !== '0px' || li.boxShadow !== 'none' || parseFloat(li.paddingLeft) > 8)) : parseFloat(s.paddingLeft) > 8;
    if (!styled && el.children.length > 1 && el.getBoundingClientRect().width) out.issues.push({k: 'naked-list', m: el.children.length + ' items', tag: el.tagName.toLowerCase(), cls: el.className.toString().slice(0,60), sec: '', text: el.textContent.replace(/\s+/g,' ').trim().slice(0,80)});
  });
  document.querySelectorAll('img').forEach(i => { if (!i.alt && i.getAttribute('role') !== 'presentation') out.issues.push({k:'img-no-alt', m:'', tag:'img', cls:'', sec:'', text:i.src.slice(-60)}); });
  if (out.h1 !== 1) out.issues.push({k: 'h1-count', m: String(out.h1), tag: 'h1', cls: '', sec: '', text: ''});
  return out;
}
"""

def serve():
    class H(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
        def translate_path(self, p):  # cleanUrls: /about -> about.html
            p = p.split('?')[0].split('#')[0]
            if p == '/': return os.path.join(ROOT, 'index.html')
            f = os.path.join(ROOT, p.strip('/'))
            return f + '.html' if os.path.exists(f + '.html') else f
    class Srv(http.server.ThreadingHTTPServer):
        request_queue_size = 128  # default backlog of 5 refuses connections under 12x concurrency
        def handle_error(self, *a): pass  # browser aborts on shutdown are noise
    srv = Srv(("127.0.0.1", PORT), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

async def scan(ctx, sem, name, url):
    path = urlparse(url).path or '/'
    async with sem:
        page = await ctx.new_page()
        for attempt in (1, 2):  # concurrent loads occasionally time out; retry once
            try:
                await page.goto(f"http://127.0.0.1:{PORT}{path}", wait_until="load", timeout=30000)
                await page.evaluate("css => document.head.append(Object.assign(document.createElement('style'), {textContent: css}))", "*{transition:none!important;animation:none!important}.reveal,.reveal-blur,.reveal-left,.reveal-right,.reveal-scale{opacity:1!important;transform:none!important;filter:none!important}")
                await page.wait_for_timeout(200)
                data = await page.evaluate(JS)
                break
            except Exception as e:
                data = {"texts": [], "issues": [{"k": "load-error", "m": str(e)[:120], "tag": "", "cls": "", "sec": "", "text": ""}], "overflow": 0}
        await page.close()
    return name, path, data

async def main():
    os.makedirs(OUT, exist_ok=True)
    urls = [e.text for e in ET.parse(os.path.join(ROOT, "sitemap.xml")).getroot().iter() if e.tag.endswith("loc")]
    srv = serve()
    async with async_playwright() as p:
        b = await p.chromium.launch()
        sem = asyncio.Semaphore(CONCURRENCY)
        ctxs = {n: await b.new_context(**o) for n, o in VIEWPORTS.items()}
        res = await asyncio.gather(*[scan(ctxs[n], sem, n, u) for u in urls for n in VIEWPORTS])
        await b.close()
    srv.shutdown()

    data = defaultdict(dict)
    for n, path, d in res: data[path][n] = d
    json.dump(data, open(os.path.join(OUT, "data.json"), "w", encoding="utf-8"), ensure_ascii=False)

    with open(os.path.join(OUT, "texts.md"), "w", encoding="utf-8") as f:   # every text, per page
        for path, v in sorted(data.items()):
            d = v["desktop"]; f.write(f"\n## {path}\n")
            for t in d["texts"]:
                f.write(f"- `{t['tag']}` [{t['sec']}] {t['fs']:g}px/{t['lh']} cr={t['cr']} — {t['text']}\n")

    tally, per_page = Counter(), defaultdict(Counter)
    with open(os.path.join(OUT, "findings.md"), "w", encoding="utf-8") as f:
        for path, v in sorted(data.items()):
            for vp, d in v.items():
                if d["overflow"]: tally[(vp, 'h-overflow')] += 1; per_page[path][(vp, 'h-overflow')] += 1; f.write(f"- {path} [{vp}] h-overflow {d['overflow']}px\n")
                grouped = Counter((i['k'], i['tag'], i['cls'], i['m'] if i['k'] in ('tap-target','tight-leading','small-font','low-contrast') else '') for i in d["issues"])
                for (k, tag, cls, m), c in grouped.items():
                    tally[(vp, k)] += c; per_page[path][(vp, k)] += c
                    ex = next(i['text'] for i in d['issues'] if i['k']==k and i['tag']==tag and i['cls']==cls)
                    f.write(f"- {path} [{vp}] {k} x{c} <{tag} .{cls}> {m} — \"{ex}\"\n")
    print(f"{len(urls)} pages x 2 viewports scanned -> {OUT}")
    for (vp, k), c in sorted(tally.items()): print(f"  {vp:8} {k:16} {c}")
    worst = sorted(per_page.items(), key=lambda kv: -sum(kv[1].values()))[:10]
    print("worst pages:", [(p, sum(c.values())) for p, c in worst])

if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8": sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())
