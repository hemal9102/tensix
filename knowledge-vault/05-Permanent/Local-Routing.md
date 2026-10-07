---
title: Local Routing & Endpoints
tags:
  - environment
  - configuration
  - routing
---

# Local Routing

When accessing the system locally (on `localhost`), the standard URL mapping differs slightly from production due to folder nesting.

- **Admin/Employee Panel (Bhagachor)**: Access via `http://localhost/jobrecruitment/bhagachor`. 
  - *Note*: Do not use `localhost/admin` or `localhost/jobrecruitment/admin` as they may return 404 or 403.
- **Main Site**: `http://localhost/jobrecruitment/`

This is critical for ensuring UI agents (like Playwright subagents) and manual testing can hit the correct endpoints.
