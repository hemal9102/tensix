---
title: Double-Lock Company Masking
tags: [security, frontend, backend]
updated: 2026-08-01
---
# Double-Lock Company Masking

**Purpose:** Ensure public visitors cannot see the real client company name.
**Summary:** We implemented a server-side masking rule in PHP so the network tab never exposes PII.

## Content
- **Backend Lock:** `JobController.php` checks if the user is a panel user. If not, `$cName` and `$realCompany` are hardcoded to "Job Recruitment" and the logo is overridden.
- **Frontend Fallback:** The public `jobs-loader.js` strictly renders the masked data. Real company names are only available in the verified `bhagachor.php` or `boss.php` endpoints.

## Related
- [[Job-Recruitment-Migration-MOC]]
