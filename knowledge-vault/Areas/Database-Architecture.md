---
title: Database & Storage Architecture
tags: [database, architecture, resilience]
updated: 2026-07-29
---

# Database & Storage Architecture

**Purpose:** Details database connection management, error recovery, and document storage conventions.

**Summary:** Handles MySQL connections with automatic retry logic to combat connection drops on shared web hosting.

## 1. Connection Resilience (`.private/db.php`)
- **Non-Persistent Handles**: Sets `PDO::ATTR_PERSISTENT => false` to ensure fresh connection handles per request.
- **Retry Mechanism**: Implements a 3-attempt connection loop with back-off delays (200ms, 400ms) to recover from `2006 MySQL server has gone away` errors.
- **Runtime Reconnect Helper**:
  - `db_is_gone_away(PDOException $e)` identifies lost connections.
  - `db_reconnect(&$pdo, $dsn, $user, $pass, $opts)` re-establishes PDO connections during long-running background tasks or cron processes.

## 2. Data Access Layer (`backend/repositories/`)
- Uses Interface-Pdo implementation pattern:
  - `ApplicationRepository.php` -> `PdoApplicationRepository.php`
  - `CandidateRepository.php` -> `PdoCandidateRepository.php`
  - `JobRepository.php` -> `PdoJobRepository.php`

## Related
- [[00-MOC/System-Architecture|System Architecture MOC]]
- [[Decisions/2026-07-29-pendrive-sync-and-db-resilience|ADR: Pendrive Sync & DB Resilience]]
