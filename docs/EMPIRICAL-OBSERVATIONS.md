# Empirical Observations: The Agent-Readiness Gap

Supporting data for the NLnet / Open Internet Stack proposal and for draft
revision `-01` of `draft-shah-agent-readiness-evaluation`.

**Every number in this document comes from an actual scan run by the Agent
Authority reference implementation.** Nothing here is estimated or borrowed.
The run is reproducible: the tool, the domain list, and the command are all
stated below, and re-running them reproduces these figures (subject to the
point-in-time caveats in the last section).

---

## How this data was produced

| Parameter | Value |
| :-- | :-- |
| Tool | `agent-authority` reference implementation, `batch_scan.py` |
| Command | `python batch_scan.py sample_domains.txt --concurrency 10 --timeout 10` |
| Domain list | `sample_domains.txt` — 25 well-known public domains |
| Date of run | 2026-10-17 |
| Wall-clock | 9.4 seconds |
| Vantage point | single scanner, single region, one point in time |

The domain list is deliberately **skewed toward sophisticated technology
companies** (Stripe, GitHub, Cloudflare, Google, Microsoft, Apple, Mozilla,
OpenAI, Anthropic, and major standards and framework sites). This matters for
interpreting the result: these are among the most engineering-capable site
operators on the web. If the agent-readiness gap shows up even here, it is far
wider across the general web.

> **Scope honesty.** This is a 25-domain *illustrative sample*, not a
> statistically representative census. It is enough to demonstrate that the gap
> is real and large; it is **not** a basis for a precise population percentage.
> The `-01` draft revision will widen this to a versioned Tranco top-N list so
> the figures become representative. This document states clearly what it is.

---

## Headline finding

Of 25 domains attempted, **24 were reachable and scored**. One was not reachable
from the scanner at scan time and is excluded from the pass-rate denominators
(reported separately, never mixed into conformance rates).

Across those 24 reachable, highly-capable domains:

| Metric | Value |
| :-- | :-- |
| Median agent-readiness score | **18 / 100** |
| Mean score | 27.1 / 100 |
| Highest score | 90 / 100 |
| Lowest score | 8 / 100 |
| "Agent-Native" (80–100) | **1 of 24** |
| "Partially Observable" (50–79) | 3 of 24 |
| "Agent Blind" (0–49) | **20 of 24** |

**The plain-English result: even the best-resourced sites on the web are, by and
large, not built for autonomous agents.** 20 of 24 scored in the lowest band.

---

## Per-capability coverage (the specific gaps)

Coverage is the share of the 24 reachable domains that satisfy each check. These
are combined from the scan's per-check records.

| Capability | Standard | Sites with it | Coverage |
| :-- | :-- | :-- | :-- |
| TLS 1.3 negotiated | RFC 8446 | 23 / 24 | **~96%** |
| JSON-LD structured data present | W3C JSON-LD 1.1 | 8 / 24 | ~33% |
| `sameAs` absolute-URI entity anchoring | RFC 3986 | 7 / 24 | ~29% |
| Edge cache / caching policy present | RFC 9111 | 9 / 24 | ~38% |
| `api-catalog` served | RFC 9727 | 3 / 24 | ~12% |
| `Link rel="describedby"` context manifest | RFC 8288 | 1 / 24 | **~4%** |
| Markdown representation advertised | RFC 7763 / RFC 8288 | 1 / 24 | **~4%** |
| `service-doc` relation declared | RFC 8631 | 2 / 24 | ~8% |

**The shape of the gap:** transport security is nearly universal (TLS 1.3 at
~96%), but the agent-facing discovery and ingestion layer is almost absent. The
two mechanisms that most directly let an AI agent find and cheaply ingest a site
— an RFC 8288 `describedby` manifest and an advertised Markdown representation —
are present on roughly **1 in 25** of even these top sites. API discovery via
RFC 9727 is at ~12%.

This is the precise, measurable problem the specification addresses: the web has
solved secure *transport* for machines but has barely begun to solve machine
*discoverability and ingestion*, and there is no open, vendor-neutral way to
measure conformance to the standards that govern it.

---

## Why this justifies the work (for the proposal)

1. **The problem is real and large, not hypothetical.** Measured coverage of the
   agent-discovery layer is in the single-digit percentages even among the most
   capable operators. A method to measure it, and open code to do so, has a clear
   reason to exist.

2. **The standards already exist; conformance does not.** Every gap above maps to
   a published IETF RFC or W3C specification (RFC 9309, 8288, 9727, 3986, 7763,
   9110, 9111, 8446; JSON-LD 1.1). The work is not inventing protocol; it is
   measuring adherence to the open standards the Internet already has — squarely
   within the digital-commons remit.

3. **An open, reproducible measure is a public good.** The only comparable
   measure today (a large CDN's agent-readiness score) is proprietary: its
   formula and weights are unpublished, and it blends that vendor's own
   conventions into the result. An open specification with open reference code,
   produces numbers anyone can reproduce and audit — independent of any single
   vendor's definition of the agent web. That independence is the European /
   open-internet value this funds.

4. **There is running code today.** This document is itself the output of the
   reference implementation. The grant funds the next phase of R&D: widening the
   empirical study to a representative fleet, formalizing a normative output
   schema so independent implementations agree, and handling the real-web edge
   cases the fleet scan surfaces.

---

## Reproducibility and limits (stated honestly)

- **Reproduce it:** install the `agent-authority` repo, then run the command in
  the table above. Per-domain results are written to `fleet_scan.jsonl` and the
  aggregate to `fleet_scan.summary.json`.
- **Sample, not census:** 25 domains, chosen for recognizability and skewed to
  tech leaders. Treat the percentages as indicative of *direction and magnitude*,
  not as population estimates. The `-01` revision replaces this with a versioned
  Tranco top-N run for representativeness.
- **Point-in-time, single vantage:** every observation reflects one scan, from
  one network location, at one moment. TLS, caching, and challenge behavior can
  vary by client, region, and time — the specification's Security Considerations
  already state this, and this data lives by the same caveat.
- **Reachability is not conformance:** the one unreachable domain is reported
  separately and is never counted as a standards failure, consistent with the
  method's "not observed vs. non-conformant" distinction.

---

## One internal note before this goes into the draft

The reference engine currently labels some checks with mixed references (e.g. a
single "RFC 7763 / RFC 8288" line, and a "Content-Signal Spec" line that is a
vendor convention, not an RFC). Before these figures are cited in draft `-01`,
align the engine's check labels and reference attributions with the `-00` draft
text — in particular, keep Content-Signal and llms.txt labelled as conventions,
not standards, and confirm the robots.txt evaluation uses the longest-match
RFC 9309 semantics the draft describes. The data-gathering is sound; the
labelling is what needs a consistency pass so the draft and the code agree.
