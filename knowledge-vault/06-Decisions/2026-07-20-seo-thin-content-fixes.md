---
title: SEO Thin-Content & Schema Fixes
tags: [decision, seo]
updated: 2026-07-20
---

# ADR 2026-07-20 — SEO Thin-Content & Schema Fixes

**Context:** Programmatic locality/industry pages counted jobs but never listed them (thin, near-duplicate). JobPosting schema emitted an invalid empty `jobLocationType`. Homepage/jobs pages lacked long-tail CTA + live counts.

**Decision:** Render live job listings on programmatic pages; `noindex` pages with 0 jobs; fix the empty enum; add keyword CTA + live job count.

**Reason:** Turn thin templated pages into genuinely unique content (safe long-tail lever) and stop invalid schema / doorway signals.

**Alternatives:** Mass-generate more keyword pages (rejected — doorway/spam risk on DA 7); do nothing (rejected — thin pages suppress crawl quality).

**Tradeoffs:** `listByLocation` is city/locality LIKE-matched, not industry-filtered — acceptable; live count in `jobs.html` title is client-side JS only (Googlebot renders it; other engines see static title).

**Consequences:** Files changed — `JobRepository.php`, `PdoJobRepository.php`, `locality-template.php`, `job-consultancy-template.php`, `job-details.php`, `index.html`, `jobs.html`, `jobs-loader.js`. Logged in `backend/ARCHITECTURE.md`.

**Rollback:** Revert those files; `listByLocation` addition is additive/safe to leave.

## Related
- [[SEO]] · [[SEO-Ranking-Strategy]] · [[Home]]
- Repo: `../../backend/ARCHITECTURE.md`
