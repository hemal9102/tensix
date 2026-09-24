---
title: Job Recruitment Offline to Live Migration MOC
tags: [architecture, migration, project]
updated: 2026-08-01
---
# Job Recruitment Offline to Live Migration MOC

**Purpose:** Hub for all architectural decisions and implementations during the migration of the offline PDF tools and Boss Panel into the live PHP application.
**Summary:** This MOC maps out how we solved the PDF scrubbing, ACID transactions, data masking, and Boss Panel UI integration.

## Related Notes
- [[ACID-Transactions-And-Schema-Interconnectivity]]
- [[Double-Lock-Company-Masking]]
- [[Headless-PDF-Scrubber-Daemon]]
- [[Boss-Panel-Invoice-Generation]]
- [[O1-Frontend-Search-And-Sorting]]

## Repo References
- `../../AGENTS.md`
- `../../backend/migrate.php`
