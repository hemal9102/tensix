---
title: System Architecture MOC
tags: [architecture, moc, index]
updated: 2026-07-29
---

# System Architecture Map of Content

**Purpose:** Comprehensive navigation hub for the JobRecruitment codebase, data layer, admin portals, and external automations.

**Summary:** The application is a PHP/JS monolith utilizing modern layered MVC principles (`backend/core`, `backend/controllers`, `backend/repositories`, `backend/services`).

## Architecture Breakdown

### 1. Web Entry Points & Portals
- **Admin Portal (`bhagachor.php`)**: SPA wrapper loading modular JS scripts from `admin/js/` and views from `backend/views/admin/`.
- **Boss Panel (`boss.php`)**: Executive dashboard for financial, client, and placement monitoring using `boss/js/`.
- **Public Website Pages**: `job-details.php`, `locality-template.php`, `article.php`, `faq.php`, `job.php`.

### 2. Dependency Graph (`.graph/`)
- Deterministic static dependency map tracking 828 files and 372 import edges across PHP, JS, and Python.

### 3. Core Automation & External Sync
- **Pendrive Backup Pipeline**: Live server DB and resume backup mirrored directly to external **`D:\jobrecruitment_backup\`**.
- **CV Parser Server**: Python fast API parser (`automation/cv_parser_server.py`) and ML trainer (`ml_resume_parser/`).

## Related
- [[Areas/Database-Architecture|Database & Storage Architecture]]
- [[Areas/Automations-and-Backups|Automations & D:\ Pendrive Pipeline]]
- [[Decisions/2026-07-29-pendrive-sync-and-db-resilience|ADR: Pendrive Sync & DB Resilience]]
- Repo: `../../ARCHITECTURE.md`, `../../CLAUDE.md`
