---
title: ACID Transactions And Schema Interconnectivity
tags: [database, architecture, decision]
updated: 2026-08-01
---
# ACID Transactions And Schema Interconnectivity

**Purpose:** Document the database structure supporting the unified Boss Panel.
**Summary:** We migrated the offline `recruitcrm-data.json` logic into strict MySQL relationships without duplicate entries.

## Content
- **Single Source of Truth:** `clients` holds company details, `jobs` link to `client_id`, `job_applications` link to `job_id`, and `placements` link `client_id` to `candidate_application_id`.
- **ACID Compliance:** All `CandidateController` and `JobController` data mutations are wrapped in `$pdo->beginTransaction()` and `$pdo->commit()` to prevent orphan records.

## Related
- [[Job-Recruitment-Migration-MOC]]
- Repo: `../../backend/migrate.php`
