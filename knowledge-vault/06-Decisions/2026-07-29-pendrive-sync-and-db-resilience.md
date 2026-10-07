---
title: ADR: Pendrive Sync & DB Connection Resilience
tags: [decision, adr, database, backup]
updated: 2026-07-29
---

# ADR: Pendrive Sync & DB Connection Resilience

## Context
1. Shared web hosting (Hostinger) frequently drops idle MySQL connections, throwing `2006 MySQL server has gone away` during cron tasks.
2. Cloud-only backups leave candidate resumes and database records vulnerable if remote hosting access is interrupted.

## Decision
1. **Disable PDO Persistent Connections & Add Reconnect Logic**: Configure `.private/db.php` with non-persistent PDO handles and exponential back-off retries (`db_reconnect`).
2. **Automated Physical Pendrive Sync**: Implement `automation/sync_live_to_pendrive.bat` leveraging WSL `rsync` staging and Windows `robocopy /MIR` targeting external drive `D:\jobrecruitment_backup`.

## Consequences
- **Positive**: High database stability under shared hosting constraints; instant offline access to complete database exports and candidate resumes on physical drive `D:\`.
- **Tradeoff**: Requires drive `D:\` to be mounted during local sync runs.

## Rollback
- Revert `.private/db.php` connection options; disable local `sync_live_to_pendrive.bat` cron execution.
