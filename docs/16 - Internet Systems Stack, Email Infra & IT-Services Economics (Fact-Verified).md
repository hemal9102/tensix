# 16 - Internet Systems Stack, Email Infra & IT-Services Economics (Fact-Verified)

> **Document ID:** `SYSTEMS-16`
> **Date:** 2026-10-15
> **Source:** Distilled and fact-checked from a long technical conversation on systems engineering, data scraping, cold-email infrastructure, and the economics of the IT-services industry. Verifiable claims were checked against live sources (Aug–Oct 2026); corrections are flagged inline.
> **Tags:** `#systems-engineering` `#networking` `#email-infrastructure` `#fcrdns` `#scraping` `#kumomta` `#it-services-economics` `#tcs` `#fact-check`

---

## 🎯 Scope & Method

This note keeps the **engineering facts** worth reusing from the conversation and drops the motivational framing. Two classes of claim:

- **Established technical facts** (protocols, physics, open-source tools) — stable, independently well-documented.
- **Recent/specific numbers** (TCS deals, revenue, HFT figures) — these were stated loosely in the chat, so each is **verified or corrected** against a cited source below.

Nothing here is a guarantee or a promise; it is a reference of how these systems actually work.

---

## 📡 1. The Internet, Bottom-Up (established facts)

The chat's "ek room → pipe → crawlers → SEO/email economy" mental model maps to the real layered stack:

| Layer | Reality |
| :--- | :--- |
| **Physical** | Data centres (Equinix, AWS regions, Hetzner Falkenstein); ~500+ undersea fibre cables carry the large majority of intercontinental traffic through chokepoints (Suez/Red Sea, Malacca, English Channel). |
| **Transport/Net** | TCP/IP sockets; the internet is ~75,000+ independent Autonomous Systems stitched together by **BGP**; congestion control (CUBIC, Google's **BBR**). |
| **Protocols (RFCs)** | TCP (RFC 793/9293), SMTP (RFC 5321), HTTP/1.1 (RFC 9110-series, formerly 2616), email format (RFC 5322). These "boring text documents" define the byte sequences everything exchanges. |
| **Kernel/metal** | NIC → DMA → `sk_buff` ring buffer → IRQ → kernel TCP stack → CPU L1/L2/L3 cache → user space. Kernel-bypass (`io_uring`, DPDK, eBPF/XDP) removes context-switches/copies for wire-speed processing. |

**Why Rust/C beat Python at scale (true):** contiguous memory + hardware prefetch keep data in L1/L2 cache (~1-4 ns) vs RAM (~60-100 ns) and avoid Python's per-object overhead. This is a real, measurable difference, not hype.

---

## 🛰️ 2. Verified "Dark Matter" Claims

- **HFT microwave latency — TRUE.** Light in vacuum ≈ 299,792 km/s; in glass fibre it slows to ≈ **200,000 km/s (~33% slower)**. Radio through air travels near vacuum speed, so firms (e.g. McKay Brothers, Jump) built microwave tower chains Chicago↔New Jersey to beat fibre by milliseconds on market data. Order logic is often on FPGAs/ASICs. **Verified as established market structure.**
- **Hardware attestation / bot farms — TRUE in direction.** Play Integrity API, WebAuthn, TPM 2.0 and Secure Enclaves do hardware-root attestation; scraping operations do use real device farms to pass checks a headless container fails. (The specific "every HTTP packet signed by the CPU" phrasing is a forward-looking simplification, not current universal behaviour.)
- **Undersea-cable geopolitics & sovereign rails — TRUE.** Cable chokepoints, landing-station taps, and national-resilience "network partition" planning are real policy topics; India's UPI/RuPay/DigiLocker reduced dependence on Visa/Mastercard/SWIFT rails.
- **AI power/cooling bottleneck — TRUE.** Rack densities have pushed past air-cooling limits into direct-to-chip liquid cooling; hyperscalers have signed nuclear/SMR power deals (e.g. Three Mile Island restart agreement). "Power electronics & cooling" is a genuinely scarce skill set.

---

## 📧 3. Atomic Email Verification Pipeline (established technique)

A network-level verifier that never sends an email, in order:

1. **Syntax / RFC 5322 parse.**
2. **DNS MX lookup** (Rust `hickory-dns`, formerly `trust-dns`).
3. **Disposable + catch-all detection** — probe an improbable address (`random-hash@domain`); if it returns `250 OK`, the domain is a catch-all and per-mailbox results are unreliable.
4. **FCrDNS (Forward-Confirmed reverse DNS)** — the probing IP's PTR must resolve to a hostname that forwards back to the same IP, or Google/Microsoft throttle or drop the socket. **This is the single most load-bearing requirement and is accurate.**
5. **SMTP socket probe (port 25)** — `HELO/EHLO → MAIL FROM → RCPT TO`, read `250` (deliverable) vs `550` (unknown user), then `QUIT` before `DATA`.

**Proven open-source building blocks (verified to exist):**

| Need | Tool |
| :--- | :--- |
| SMTP/catch-all verification in Rust | `reacherhq/check-if-email-exists` |
| E.164 phone normalisation | `phonenumber` crate (Google libphonenumber port) |
| Historical contact mining | Wayback CDX API (`web.archive.org/cdx/search/cdx`) |
| Chrome TLS/JA3-JA4 impersonation | `rquest` (BoringSSL-backed reqwest fork); `camoufox` for headless anti-detect |
| Fast Rust crawler | `spider-rs` (Tokio) |
| Modern open-source MTA | **KumoMTA** (DKIM signing, FBL, per-domain throttling) |

**OCI port-25 caveat — accurate:** Oracle/AWS block outbound port 25 on free tiers. Workaround: run heavy crawl/compute on an OCI Always-Free Ampere box, and tunnel only the SMTP probe over a Tailscale/WireGuard mesh to a cheap VPS (Hetzner/OVH) that has clean IPv4 + delegated PTR/FCrDNS. Keeps public ports closed (network segmentation).

> These are the same primitives TenSix already uses in its email-deliverability service (SPF/DKIM/DMARC, SES, return-path, Postmaster/SNDS). This note is the systems-level backing for that offering.

---

## 🏢 4. IT-Services Economics — TCS (fact-checked)

The conversation used TCS as a worked example. Verified figures (sources below):

| Claim in chat | Verified (Aug–Oct 2026) |
| :--- | :--- |
| TCS buys Porsche's MHP for €320M | ✅ **Correct** — 100% of MHP, enterprise value €320M, announced 2026-08-24; needs regulatory approval, ~3-4 months to close. |
| Porsche deal €1.25B / 5 years | ✅ **Mostly** — most sources €1.25B over 5 years + dedicated AI Mobility Centre of Excellence; a few report ~€1B. |
| MHP ≈ 4,500 staff | ✅ Correct; MHP turnover ≈ €742M (CY25). |
| TCS total revenue ~$30B | ✅ Roughly — Q1 FY27 ≈ $7.6B/quarter, annualises near $30B. |
| TCS AI revenue "$3.1B FY27" | ⚠️ **Overstated** — actual **$2.6B annualised AI run-rate (Q1 FY27)**, +13.6% QoQ. |
| Operating margin ~24% | ✅ Correct — **24.0%** in Q1 FY27 (down ~130 bps on wage hikes). |
| Workforce ~584,000 | ⚠️ Close but stale — **~593,798** (Q1 FY27). |
| CEO K. Krithivasan | ✅ Correct. |

**Structural read (accurate):** the old "revenue = heads × billed hours × rate" model is under pressure from GenAI; ~90% of TCS cash is still traditional (maintenance, SAP, BFSI legacy, data migration, RAG guardrails), and the "AI/zero-touch" pivot is a slow, margin-defensive turn — not an overnight flip. "Zero-touch" in practice = automated runbooks, self-healing infra (Ignio, Datadog/Dynatrace) with a natural-language layer on top.

---

## 🧭 5. Reusable Takeaways

- The crawl → normalise/verify → deliver pipeline is an **assembly job** over proven OSS, not a from-scratch build. Build it modularly: **atomic email verifier first** (standalone value), then plug into the existing crawler, then KumoMTA dispatch.
- FCrDNS + catch-all detection are the make-or-break correctness points; everything else is plumbing.
- The same async-I/O / socket / zero-copy engineering underpins both a lead-scraper and enterprise telemetry ingestion — the difference is scale and who pays.

---
**Backlinks:**
* [[00 - Index|Domain Index]]
* [[05 - Competitor Reverse-Engineering & Ranking Outflank Endpoints|05 - Competitor Reverse-Engineering]]
* [[06 - MTA Deliverability, RFC Gateways & Mailbox Interrogation Endpoints|06 - MTA Deliverability & RFC Gateways]]

**Sources (verified 2026-10-15):**
* TCS–Porsche / MHP: [yourstory](https://yourstory.com/2026/08/tcs-acquires-porsches-it-arm-for--320-million-bags--125-billion-deal), [Business Today](https://www.businesstoday.in/auto/story/tcs-to-acquire-porsches-it-consulting-arm-mhp-for-eu320-million-signs-five-year-strategic-deal-551055-2026-08-24), [Outlook Business](https://www.outlookbusiness.com/corporate/tcs-to-buy-porsches-it-consulting-unit-mhp-for-320-mn)
* TCS Q1 FY27 (AI run-rate $2.6B, margin 24.0%, workforce 593,798): [TCS IR press release](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q1/IFRS/Press%20Release%20-%20USD.pdf), [bigul summary](https://bigul.co/blog/market-update/tcs-q1-fy27-results-profit-up-46-ai-revenue-hits-26-billion-run-rate)
