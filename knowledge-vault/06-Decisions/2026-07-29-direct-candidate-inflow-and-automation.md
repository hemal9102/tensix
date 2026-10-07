---
title: ADR: Direct Candidate Inflow, Enhanced Search, Radius Excel Export & Automations
tags: [decision, adr, candidates, excel, whatsapp, automation]
updated: 2026-07-29
---

# ADR: Direct Candidate Inflow, Enhanced Search, Radius Excel Export & Automations

## Context
1. Admin user requested direct inflow of job applications into the Candidates database without requiring manual approval from the Applications tab.
2. Sidebar tab needed to be renamed from "Approved" to "Candidates".
3. Candidates tab required enhanced phone number and resume content/filename search capability.
4. Radius Search tool required a direct Excel/CSV export option for filtered candidates by job role and location.
5. Modular WhatsApp and Email dispatchers were needed in `automation/`.

## Decision
1. **Default Candidate Inflow**: Updated `SubmitApplicationService.php` to set `'status' => 'Approved'` on new application submissions, placing candidates directly in the Candidates table.
2. **Sidebar Navigation**: Renamed sidebar navigation item in `sidebar.php` to **Candidates**.
3. **Phone & Resume Search**: Enhanced inverted indexing in `admin/js/candidates.js` to index sanitized phone digits and resume filenames (`c.cv`).
4. **Radius Search Excel Export**: Added `exportRadiusToExcel()` in `admin/js/radius-search.js` generating downloadable `.csv` spreadsheets with complete candidate metadata.
5. **Automation Services**: Created `automation/whatsapp_service.py` and `automation/email_service.py` for automated messaging.

## Consequences
- **Positive**: Streamlined recruiter workflow; zero-touch application-to-candidate pipeline; instant spreadsheet export for candidate location searches.
