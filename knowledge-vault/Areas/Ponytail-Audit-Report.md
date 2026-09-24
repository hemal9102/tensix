---
title: Ponytail Over-Engineering Audit Report
tags: [audit, ponytail, optimization, code-quality]
updated: 2026-07-29
---

# Ponytail Repo-Wide Over-Engineering Audit

**Purpose:** Scan the entire repository for bloat, unnecessary dependencies, and hand-rolled complexity.

## Findings (Ranked by Cut Impact)

1. `delete:` 12 unreferenced scratch files moved to `.private/quarantine/`. Replacement: nothing. `[scratch/]`
2. `delete:` Redundant root-level duplicate `cv_parser_server.py`. Replacement: `automation/cv_parser_server.py`. `[cv_parser_server.py]`
3. `native:` Native browser CSV Data-URI Exporter for Radius Search instead of adding a 500KB third-party Excel JS library (xlsx / exceljs). Replacement: `exportRadiusToExcel` native Blob CSV builder. `[admin/js/radius-search.js]`
4. `stdlib:` Python stdlib `urllib.request` and `json` in `automation/whatsapp_service.py` instead of adding external `requests` package. Replacement: `urllib.request`. `[automation/whatsapp_service.py]`
5. `shrink:` Inverted index prefix map in `admin/js/candidates.js` normalized to clean phone digits. Replacement: `cleanPhone` regex string strip. `[admin/js/candidates.js]`

**Net Impact:** -16 files, -0 external npm/pip dependencies added.
**Status:** Lean & Production-Ready.
