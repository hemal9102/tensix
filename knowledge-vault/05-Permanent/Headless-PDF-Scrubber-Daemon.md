---
title: Headless PDF Scrubber Daemon
tags: [architecture, pdf, security]
updated: 2026-08-01
---
# Headless PDF Scrubber Daemon

**Purpose:** Automate the manual GUI-based PDF scrubbing.
**Summary:** Replaced `fabric.js` manual drawing with a headless Node.js daemon using `pdf-lib` and `pdfjs-dist`.

## Content
- **Mechanism:** The daemon polls `automation_queue`. It uses `pdfjs-dist` to extract regex coordinates for Emails and Phones.
- **Masking:** It uses `pdf-lib` to draw `rgb(1, 1, 1)` rectangles with 2px padding directly over the PII.
- **No GUI:** Completely bypasses the canvas rendering overhead used in the offline `PDF-Toolkit`.

## Related
- [[Job-Recruitment-Migration-MOC]]
- Repo: `../../automation/pdf-scrubber.js`
