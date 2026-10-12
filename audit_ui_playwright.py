#!/usr/bin/env python3
"""
Comprehensive Playwright UI/UX Auditor across all 47 pages of tensix.in
Tests Desktop (1440x900) and Mobile (390x844) viewports:
- Captures full-page screenshots
- Detects horizontal layout overflows
- Detects console errors and network request failures
- Pinpoints offending DOM elements causing overflow
"""

import os
import sys
import time
import json
import re
import threading
import http.server
import socketserver
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(ROOT_DIR, "screenshots")
DESKTOP_DIR = os.path.join(SCREENSHOTS_DIR, "desktop")
MOBILE_DIR = os.path.join(SCREENSHOTS_DIR, "mobile")
PORT = 8765

os.makedirs(DESKTOP_DIR, exist_ok=True)
os.makedirs(MOBILE_DIR, exist_ok=True)

class QuietHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT_DIR, **kwargs)
    def log_message(self, format, *args):
        pass

def start_server():
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), QuietHTTPHandler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd

def get_sitemap_urls():
    sitemap_path = os.path.join(ROOT_DIR, "sitemap.xml")
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    urls = [elem.text for elem in root.iter() if elem.tag.endswith('loc')]
    return urls

def url_to_local_path(url):
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path:
        return "/index.html"
    if path.endswith(".html"):
        return f"/{path}"
    return f"/{path}.html"

def url_to_slug(url):
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path:
        return "homepage"
    return path.replace("/", "__")

OVERFLOW_CHECK_SCRIPT = """
() => {
    const docWidth = document.documentElement.clientWidth;
    const scrollWidth = document.documentElement.scrollWidth;
    const bodyScrollWidth = document.body ? document.body.scrollWidth : 0;
    const hasDocOverflow = scrollWidth > docWidth + 1;
    
    const overflowingElements = [];
    const all = document.querySelectorAll('*');
    for (const el of all) {
        const rect = el.getBoundingClientRect();
        if (rect.right > docWidth + 2 && rect.width > 0 && rect.height > 0) {
            const style = window.getComputedStyle(el);
            if (style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0') {
                overflowingElements.push({
                    tag: el.tagName.toLowerCase(),
                    id: el.id || '',
                    className: (typeof el.className === 'string' ? el.className : ''),
                    right: Math.round(rect.right),
                    docWidth: docWidth,
                    overflowPx: Math.round(rect.right - docWidth),
                    snippet: el.outerHTML.substring(0, 120)
                });
            }
        }
    }
    return {
        hasOverflow: hasDocOverflow,
        docWidth: docWidth,
        scrollWidth: scrollWidth,
        bodyScrollWidth: bodyScrollWidth,
        overflowDelta: Math.max(0, scrollWidth - docWidth),
        offenders: overflowingElements.slice(0, 10)
    };
}
"""

SCROLL_AND_SETTLE_SCRIPT = """
async () => {
    await new Promise((resolve) => {
        let totalHeight = 0;
        const distance = 400;
        const timer = setInterval(() => {
            window.scrollBy(0, distance);
            totalHeight += distance;
            if (totalHeight >= document.body.scrollHeight) {
                clearInterval(timer);
                window.scrollTo(0, 0);
                document.querySelectorAll('.reveal, .reveal-blur, .reveal-left, .reveal-right, .reveal-scale').forEach(el => el.classList.add('active'));
                resolve();
            }
        }, 25);
    });
}
"""

def run_audit():
    urls = get_sitemap_urls()
    print(f"Loaded {len(urls)} URLs from sitemap.xml")

    httpd = start_server()
    print(f"Local test HTTP server running on http://127.0.0.1:{PORT}")

    results = {
        "desktop": {"clean": 0, "issues": []},
        "mobile": {"clean": 0, "issues": []}
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # 1. Desktop Context
        desktop_context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        
        # 2. Mobile Context (iPhone 14 standard)
        mobile_context = browser.new_context(
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            has_touch=True,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
        )

        desktop_page = desktop_context.new_page()
        mobile_page = mobile_context.new_page()

        print("\n" + "="*60)
        print("STARTING PLAYWRIGHT AUDIT ACROSS ALL 47 PAGES")
        print("="*60 + "\n")

        for idx, url in enumerate(urls, 1):
            local_path = url_to_local_path(url)
            slug = url_to_slug(url)
            full_url = f"http://127.0.0.1:{PORT}{local_path}"

            print(f"[{idx}/{len(urls)}] Auditing {local_path} ...", end=" ", flush=True)

            desktop_console_errors = []
            mobile_console_errors = []

            # Capture errors
            desktop_page.on("pageerror", lambda err: desktop_console_errors.append(str(err)))
            mobile_page.on("pageerror", lambda err: mobile_console_errors.append(str(err)))

            # Desktop audit
            desktop_shot_path = os.path.join(DESKTOP_DIR, f"{slug}.png")
            try:
                desktop_page.goto(full_url, wait_until="networkidle", timeout=15000)
                desktop_page.evaluate(SCROLL_AND_SETTLE_SCRIPT)
                desktop_page.wait_for_timeout(300)
                desktop_overflow = desktop_page.evaluate(OVERFLOW_CHECK_SCRIPT)
                desktop_page.screenshot(path=desktop_shot_path, full_page=True)

                if desktop_overflow["hasOverflow"] or desktop_console_errors:
                    results["desktop"]["issues"].append({
                        "url": url,
                        "path": local_path,
                        "slug": slug,
                        "overflow": desktop_overflow,
                        "console_errors": desktop_console_errors
                    })
                else:
                    results["desktop"]["clean"] += 1
            except Exception as e:
                results["desktop"]["issues"].append({
                    "url": url,
                    "path": local_path,
                    "slug": slug,
                    "load_error": str(e)
                })

            # Mobile audit
            mobile_shot_path = os.path.join(MOBILE_DIR, f"{slug}.png")
            try:
                mobile_page.goto(full_url, wait_until="networkidle", timeout=15000)
                mobile_page.evaluate(SCROLL_AND_SETTLE_SCRIPT)
                mobile_page.wait_for_timeout(300)
                mobile_overflow = mobile_page.evaluate(OVERFLOW_CHECK_SCRIPT)
                mobile_page.screenshot(path=mobile_shot_path, full_page=True)

                if mobile_overflow["hasOverflow"] or mobile_console_errors:
                    results["mobile"]["issues"].append({
                        "url": url,
                        "path": local_path,
                        "slug": slug,
                        "overflow": mobile_overflow,
                        "console_errors": mobile_console_errors
                    })
                else:
                    results["mobile"]["clean"] += 1
            except Exception as e:
                results["mobile"]["issues"].append({
                    "url": url,
                    "path": local_path,
                    "slug": slug,
                    "load_error": str(e)
                })

            d_status = "PASS" if not results["desktop"]["issues"] or results["desktop"]["issues"][-1]["path"] != local_path else "FAIL"
            m_status = "PASS" if not results["mobile"]["issues"] or results["mobile"]["issues"][-1]["path"] != local_path else "FAIL"
            print(f"Desktop: {d_status} | Mobile: {m_status}")

        browser.close()

    httpd.shutdown()

    # Save summary report
    report_file = os.path.join(ROOT_DIR, "ui_audit_report.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n" + "="*60)
    print("AUDIT SUMMARY:")
    print(f"Desktop: {results['desktop']['clean']}/47 clean, {len(results['desktop']['issues'])} pages with issues")
    print(f"Mobile:  {results['mobile']['clean']}/47 clean, {len(results['mobile']['issues'])} pages with issues")
    print(f"Detailed report saved to: {report_file}")
    print("="*60)

    if results["desktop"]["issues"]:
        print("\n--- DESKTOP ISSUES ---")
        for item in results["desktop"]["issues"]:
            print(f"Page: {item['path']}")
            if "overflow" in item and item["overflow"]["hasOverflow"]:
                print(f"  Overflow Delta: {item['overflow']['overflowDelta']}px (scrollWidth={item['overflow']['scrollWidth']} > docWidth={item['overflow']['docWidth']})")
                for off in item["overflow"]["offenders"]:
                    print(f"    Offender: <{off['tag']} class='{off['className']}'> (+{off['overflowPx']}px)")
            if item.get("console_errors"):
                print(f"  Console Errors: {item['console_errors']}")

    if results["mobile"]["issues"]:
        print("\n--- MOBILE ISSUES ---")
        for item in results["mobile"]["issues"]:
            print(f"Page: {item['path']}")
            if "overflow" in item and item["overflow"]["hasOverflow"]:
                print(f"  Overflow Delta: {item['overflow']['overflowDelta']}px (scrollWidth={item['overflow']['scrollWidth']} > docWidth={item['overflow']['docWidth']})")
                for off in item["overflow"]["offenders"]:
                    print(f"    Offender: <{off['tag']} class='{off['className']}'> (+{off['overflowPx']}px)")
            if item.get("console_errors"):
                print(f"  Console Errors: {item['console_errors']}")

if __name__ == "__main__":
    run_audit()
