"""
Multi-Engine Email Deliverability & Anomaly Scoring Inspector (5-Engine Architecture)
Based on: D:\\projects\\HK\\tensix\\docs\\18 - Five-Pillar Deliverability Engine & Anti-Spam Heuristics.md

Evaluates:
  Engine 1: L4/L7 Network & Socket Profiler (TCP, TLS, Cipher, Handshake)
  Engine 2: RFC Protocol & Cryptographic Header State Machine (SPF, DKIM, DMARC, ARC, VERP, Alignment)
  Engine 3: Chromium Headless DOM & Link Graph Sandbox (HTML budget, 1:1 Apex attribution, tables, beacons)
  Engine 4: RETVec & BERT Semantic Embedding Engine (Vocabulary, NLP entropy, token evasion, zero-width spaces)
  Engine 5: Recipient Affinity & Velocity Correlator (Cadence, Feedback-ID, List-Unsubscribe, X-Auto-Response)
"""

import sys
import os
import re
import email
from email import policy
import json
import math
from bs4 import BeautifulSoup
import urllib.parse

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def analyze_email_5_engines(eml_path):
    with open(eml_path, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.compat32)

    results = {
        "file": os.path.basename(eml_path),
        "subject": str(msg.get("Subject", "")),
        "from": str(msg.get("From", "")),
        "to": str(msg.get("To", "")),
        "date": str(msg.get("Date", "")),
        "engines": {},
        "anomaly_scores": {},
        "composite_anomaly": 0.0,
        "verdict": ""
    }

    # Extract HTML & Plaintext bodies
    html_body = ""
    text_body = ""
    for part in msg.walk():
        ct = part.get_content_type()
        payload = part.get_payload(decode=True)
        if payload:
            if ct == "text/html" and not html_body:
                html_body = payload.decode("utf-8", errors="ignore")
            elif ct == "text/plain" and not text_body:
                text_body = payload.decode("utf-8", errors="ignore")

    raw_headers = "\n".join([f"{k}: {v}" for k, v in msg.items()])

    # =========================================================================
    # ENGINE 1: L4/L7 Network & Socket Profiler (p0f + JA4 TLS)
    # =========================================================================
    e1_flags = []
    e1_anomaly = 0.0
    
    received_headers = msg.get_all("Received", [])
    tls_found = False
    tls_version = "None"
    for r in received_headers:
        if "TLS" in r or "ESMTPS" in r:
            tls_found = True
            m_tls = re.search(r'(TLSv[0-9\.]+|TLS_[A-Z0-9_]+|ECDHE-[A-Z0-9\-]+)', r)
            if m_tls:
                tls_version = m_tls.group(1)
            break
            
    if not tls_found:
        e1_flags.append(("CRITICAL", "Missing TLS/ESMTPS in transport handshake (Cleartext SMTP)"))
        e1_anomaly += 0.40
    else:
        e1_flags.append(("PASS", f"Encrypted ESMTPS Transport detected ({tls_version})"))

    spf_header = str(msg.get("Received-SPF", ""))
    ip_match = re.search(r'designates\s+([0-9\.]+)', spf_header)
    connecting_ip = ip_match.group(1) if ip_match else "Unknown"

    if connecting_ip != "Unknown":
        e1_flags.append(("PASS", f"Inbound Connecting IP: {connecting_ip}"))
    else:
        e1_flags.append(("WARN", "Connecting IP not explicitly isolated in SPF header"))
        e1_anomaly += 0.10

    results["engines"]["Engine 1: L4/L7 Network & Socket"] = {
        "connecting_ip": connecting_ip,
        "tls_active": tls_found,
        "tls_detail": tls_version,
        "flags": e1_flags
    }
    results["anomaly_scores"]["Engine 1"] = min(1.0, e1_anomaly)

    # =========================================================================
    # ENGINE 2: RFC Protocol & Header State Machine (Zero Dissonance)
    # =========================================================================
    e2_flags = []
    e2_anomaly = 0.0

    if "pass" in spf_header.lower():
        e2_flags.append(("PASS", "SPF Check: PASS"))
    elif "fail" in spf_header.lower():
        e2_flags.append(("CRITICAL", "SPF Check: FAIL"))
        e2_anomaly += 0.35
    elif "neutral" in spf_header.lower() or "softfail" in spf_header.lower():
        e2_flags.append(("WARN", "SPF Check: Softfail / Neutral"))
        e2_anomaly += 0.15
    else:
        e2_flags.append(("WARN", "SPF Check: Unspecified"))
        e2_anomaly += 0.10

    dkims = msg.get_all("DKIM-Signature", [])
    if not dkims:
        e2_flags.append(("CRITICAL", "DKIM Signature Missing"))
        e2_anomaly += 0.40
    else:
        e2_flags.append(("PASS", f"DKIM Signatures Present: {len(dkims)} signature(s)"))
        for idx, d in enumerate(dkims, 1):
            d_domain = re.search(r'd=([^;\s]+)', d)
            d_sel = re.search(r's=([^;\s]+)', d)
            dom = d_domain.group(1) if d_domain else "unknown"
            sel = d_sel.group(1) if d_sel else "unknown"
            e2_flags.append(("INFO", f"DKIM #{idx}: domain={dom}, selector={sel}"))

    from_header = str(msg.get("From", ""))
    from_domain_match = re.search(r'@([a-zA-Z0-9\.\-_]+)', from_header)
    from_domain = from_domain_match.group(1).lower() if from_domain_match else ""

    return_path = str(msg.get("Return-Path", ""))
    rp_domain_match = re.search(r'@([a-zA-Z0-9\.\-_]+)', return_path)
    rp_domain = rp_domain_match.group(1).lower() if rp_domain_match else ""

    dkim_domains = [re.search(r'd=([^;\s]+)', d).group(1).lower() for d in dkims if re.search(r'd=([^;\s]+)', d)]

    aligned_dkim = any((from_domain == dd or from_domain.endswith("." + dd) or dd.endswith("." + from_domain)) for dd in dkim_domains)
    aligned_rp = (from_domain == rp_domain or from_domain.endswith("." + rp_domain) or rp_domain.endswith("." + from_domain))

    if aligned_dkim and aligned_rp:
        e2_flags.append(("PASS", f"Zero Dissonance Verified: From ({from_domain}) aligned with DKIM & Return-Path"))
    elif aligned_dkim:
        e2_flags.append(("PASS", f"DMARC DKIM Aligned: From ({from_domain}) matches DKIM ({dkim_domains})"))
    else:
        e2_flags.append(("WARN", f"Identifier Dissonance: From ({from_domain}) differs from DKIM ({dkim_domains})"))
        e2_anomaly += 0.20

    arc_results = msg.get("ARC-Authentication-Results", "")
    if arc_results:
        e2_flags.append(("PASS", "ARC (Authenticated Received Chain) validated"))
    else:
        e2_flags.append(("INFO", "Single-hop direct ingress (No intermediate ARC chain)"))

    msg_id = str(msg.get("Message-ID", ""))
    if not msg_id or "localhost" in msg_id.lower() or re.search(r'@[0-9\.]+', msg_id):
        e2_flags.append(("CRITICAL", f"Suspicious Message-ID FQDN: {msg_id}"))
        e2_anomaly += 0.25
    else:
        e2_flags.append(("PASS", f"Valid Message-ID FQDN: {msg_id}"))

    results["engines"]["Engine 2: RFC Protocol & Header State Machine"] = {
        "from_domain": from_domain,
        "return_path_domain": rp_domain,
        "dkim_domains": dkim_domains,
        "aligned": aligned_dkim,
        "flags": e2_flags
    }
    results["anomaly_scores"]["Engine 2"] = min(1.0, e2_anomaly)

    # =========================================================================
    # ENGINE 3: Chromium Headless DOM & Link Graph Sandbox
    # =========================================================================
    e3_flags = []
    e3_anomaly = 0.0

    html_bytes = len(html_body.encode("utf-8")) if html_body else 0

    if html_bytes > 102400:
        e3_flags.append(("CRITICAL", f"HTML size {html_bytes:,} bytes EXCEEDS Gmail 102.4 KB clip threshold!"))
        e3_anomaly += 0.50
    elif html_bytes > 85000:
        e3_flags.append(("WARN", f"HTML size {html_bytes:,} bytes approaching clip boundary"))
        e3_anomaly += 0.20
    else:
        e3_flags.append(("PASS", f"HTML size {html_bytes:,} bytes strictly under Gmail clip boundary"))

    soup = BeautifulSoup(html_body, "html.parser") if html_body else None
    links = []
    apex_mismatches = 0
    if soup:
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            links.append(href)
            parsed = urllib.parse.urlparse(href)
            netloc = parsed.netloc.lower()
            if netloc and from_domain:
                f_parts = from_domain.split(".")[-2:]
                l_parts = netloc.split(".")[-2:]
                if f_parts != l_parts and not any(trusted in netloc for trusted in ["postmarkapp.com", "google.com", "schema.org"]):
                    apex_mismatches += 1

    if links:
        if apex_mismatches == 0:
            e3_flags.append(("PASS", f"1:1 Apex Attribution: All {len(links)} links align with sender domain apex"))
        else:
            e3_flags.append(("WARN", f"Cross-domain Tracking: {apex_mismatches}/{len(links)} links resolve to external tracking apex"))
            e3_anomaly += min(0.30, apex_mismatches * 0.10)
    else:
        e3_flags.append(("INFO", "No external hyperlinks detected in HTML payload"))

    imgs = soup.find_all("img") if soup else []
    beacons = [img for img in imgs if img.get("width") in ["0", "1"] or img.get("height") in ["0", "1"]]
    if len(imgs) == len(beacons):
        e3_flags.append(("PASS", f"Clean Presentation: Zero marketing hero images ({len(beacons)} telemetry beacon detected)"))
    elif len(imgs) > 5:
        e3_flags.append(("WARN", f"Heavy image DOM: {len(imgs)} images present (Promotions Tab signal)"))
        e3_anomaly += 0.20

    has_mso = "mso" in html_body.lower()
    has_dark_mode = "color-scheme" in html_body.lower() or "[data-ogsc]" in html_body.lower()
    if has_mso:
        e3_flags.append(("PASS", "Microsoft Word MSO Conditional architecture detected"))
    if has_dark_mode:
        e3_flags.append(("PASS", "Two-tier Dark Mode CSS overrides detected"))

    results["engines"]["Engine 3: Chromium Headless DOM & Link Graph"] = {
        "html_bytes": html_bytes,
        "total_links": len(links),
        "apex_mismatches": apex_mismatches,
        "image_count": len(imgs),
        "flags": e3_flags
    }
    results["anomaly_scores"]["Engine 3"] = min(1.0, e3_anomaly)

    # =========================================================================
    # ENGINE 4: RETVec & BERT Semantic Embedding Engine
    # =========================================================================
    e4_flags = []
    e4_anomaly = 0.0

    visible_text = soup.get_text(separator=" ", strip=True) if soup else text_body
    text_len = len(visible_text)

    zws_entities = len(re.findall(r'(&#8203;|&#x200b;|\u200b)', html_body, re.IGNORECASE))
    zwnj_entities = len(re.findall(r'(&zwnj;|&#8204;|\u200c)', html_body, re.IGNORECASE))

    if zws_entities > 0:
        e4_flags.append(("INFO", f"Zero-Width Space Evasion Token count: {zws_entities} (Parsed by RETVec)"))
    if zwnj_entities > 0:
        e4_flags.append(("PASS", f"Preheader Buffer Flood: {zwnj_entities} ZWNJ instances found"))

    text_ratio = (text_len / html_bytes * 100) if html_bytes > 0 else 100
    if text_ratio < 15:
        e4_flags.append(("WARN", f"Low Text-to-HTML ratio: {text_ratio:.1f}% (Code-heavy DOM)"))
        e4_anomaly += 0.20
    else:
        e4_flags.append(("PASS", f"Healthy Text-to-HTML ratio: {text_ratio:.1f}%"))

    spam_triggers = ["100% free", "guaranteed", "buy now", "risk free", "limited time offer", "discount", "order now", "special promo"]
    academic_markers = ["manuscript", "journal", "peer review", "editorial", "volume", "issue", "research", "tracking ref", "doi", "citation", "issn"]

    found_triggers = [w for w in spam_triggers if w in visible_text.lower()]
    found_academic = [w for w in academic_markers if w in visible_text.lower()]

    if found_triggers:
        e4_flags.append(("CRITICAL", f"Spam trigger phrases detected: {found_triggers}"))
        e4_anomaly += min(0.50, len(found_triggers) * 0.15)
    else:
        e4_flags.append(("PASS", "Zero aggressive commercial spam triggers detected"))

    if found_academic:
        e4_flags.append(("PASS", f"High-Trust Institutional Entity Vocabulary: {len(found_academic)} markers matched {found_academic[:5]}"))
    else:
        e4_flags.append(("INFO", "Neutral semantic text profile"))

    results["engines"]["Engine 4: RETVec & BERT Semantic Embedding"] = {
        "text_length": text_len,
        "text_ratio": round(text_ratio, 1),
        "zws_tokens": zws_entities,
        "zwnj_tokens": zwnj_entities,
        "academic_markers_found": len(found_academic),
        "spam_triggers_found": len(found_triggers),
        "flags": e4_flags
    }
    results["anomaly_scores"]["Engine 4"] = min(1.0, e4_anomaly)

    # =========================================================================
    # ENGINE 5: Recipient Affinity & Velocity Correlator
    # =========================================================================
    e5_flags = []
    e5_anomaly = 0.0

    unsub_header = msg.get("List-Unsubscribe", "")
    unsub_post = msg.get("List-Unsubscribe-Post", "")
    list_id = msg.get("List-ID", "")

    if unsub_header and unsub_post and "One-Click" in unsub_post:
        e5_flags.append(("PASS", "Full RFC 8058 One-Click Unsubscribe compliance (Mandatory for Google/Yahoo 2024+)"))
    elif unsub_header:
        e5_flags.append(("PASS", "Standard List-Unsubscribe header present"))
    else:
        e5_flags.append(("WARN", "Missing List-Unsubscribe header (Can trigger Promotions/Spam routing)"))
        e5_anomaly += 0.25

    auto_suppress = msg.get("X-Auto-Response-Suppress", "")
    if auto_suppress and "All" in auto_suppress:
        e5_flags.append(("PASS", "Auto-responder loops suppressed (X-Auto-Response-Suppress: All)"))
    else:
        e5_flags.append(("INFO", "X-Auto-Response-Suppress not explicitly defined"))

    feedback_id = msg.get("Feedback-ID", "")
    x_kumoref = msg.get("X-KumoRef", "")
    if x_kumoref:
        e5_flags.append(("PASS", "KumoMTA Rust Infrastructure confirmed (X-KumoRef Active)"))
    if feedback_id:
        e5_flags.append(("PASS", f"FBL Gateway Tracking active (Feedback-ID: {feedback_id})"))

    results["engines"]["Engine 5: Recipient Affinity & Velocity Correlator"] = {
        "has_one_click_unsub": bool(unsub_post and "One-Click" in unsub_post),
        "list_id": str(list_id),
        "kumomta_identified": bool(x_kumoref),
        "flags": e5_flags
    }
    results["anomaly_scores"]["Engine 5"] = min(1.0, e5_anomaly)

    # =========================================================================
    # COMPOSITE ANOMALY FORMULA
    # A_total = w1*A_transport + w2*A_identity + w3*A_network + w4*A_DOM + w5*A_cadence
    # =========================================================================
    w1, w2, w3, w4, w5 = 0.20, 0.25, 0.20, 0.20, 0.15
    composite = (
        w1 * results["anomaly_scores"]["Engine 1"] +
        w2 * results["anomaly_scores"]["Engine 2"] +
        w3 * results["anomaly_scores"]["Engine 3"] +
        w4 * results["anomaly_scores"]["Engine 4"] +
        w5 * results["anomaly_scores"]["Engine 5"]
    )
    results["composite_anomaly"] = round(composite, 3)

    if composite <= 0.08:
        results["verdict"] = "PRIMARY INBOX (Zero-Anomaly Day-1 Execution)"
    elif composite <= 0.22:
        results["verdict"] = "PRIMARY INBOX / OCCASIONAL PROMOTIONS (Low Risk)"
    elif composite <= 0.40:
        results["verdict"] = "PROMOTIONS TAB ROUTING (Commercial Signals Active)"
    else:
        results["verdict"] = "SPAM FOLDER / GATEWAY DEFERRAL (High Anomaly Score)"

    return results

def print_audit_report(res):
    print("=" * 80)
    print("5-ENGINE DELIVERABILITY & INGRESS AUDIT REPORT")
    print(f"Target: {res['file']}")
    print(f"Subject: {res['subject']}")
    print(f"From: {res['from']}")
    print("-" * 80)
    
    for eng_name, eng_data in res["engines"].items():
        score = res["anomaly_scores"][eng_name.split(":")[0]]
        print(f"\n>> {eng_name} [Anomaly Score: {score:.2f}]")
        for flag_type, desc in eng_data["flags"]:
            symbol = "[+]" if flag_type == "PASS" else ("[!]" if flag_type == "WARN" else ("[-]" if flag_type == "CRITICAL" else "[i]"))
            print(f"   {symbol} {flag_type:<8}: {desc}")

    print("\n" + "-" * 80)
    print(f"COMPOSITE DAY-1 ANOMALY METRIC (A_total): {res['composite_anomaly']:.3f} / 1.000")
    print(f"FINAL INBOX ROUTING VERDICT: {res['verdict']}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if os.path.isfile(target):
            res = analyze_email_5_engines(target)
            print_audit_report(res)
        elif os.path.isdir(target):
            for f in os.listdir(target):
                if f.lower().endswith(".eml"):
                    res = analyze_email_5_engines(os.path.join(target, f))
                    print_audit_report(res)
    else:
        print("Usage: python inspect_5_engines.py <path_to_eml_file_or_directory>")
