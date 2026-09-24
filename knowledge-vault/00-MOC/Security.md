---
title: Security MOC
tags: [moc, security]
updated: 2026-07-20
---

# Security — Map of Content

**Purpose:** Auth, session, CSRF, and secrets model.

**Summary:** Session-based admin auth via `SessionManager` (single source of truth). CSRF on all writes. Secrets in `.private/`. Read the core file fully before touching it.

## Key facts
- Auth = `$_SESSION['admin_auth'] === true` + role; validated by `SessionManager::isAuthenticated()` (also UA-fingerprint bound via `ip_hash`).
- CSRF: `X-Csrf-Token` header (auto-attached by `admin/js/api-client.js`) or `_csrf` body; fetch via `?action=get_csrf_token`.
- Session cookie: HttpOnly, SameSite=Lax, Secure-on-HTTPS.
- Secrets: `.private/db.php` (PDO), `.private/config.json` (API keys) — rsyncignored.
- Known deviation: ~9 controllers still read `$_SESSION` directly instead of via `SessionManager` (low priority) — see memory `project-session-direct-read-pattern`.
- `super-dev.php` (root) is untouchable — never move/modify/gitignore it.

## Source-of-truth docs
- `../../backend/core/CLAUDE.md` · `../../backend/controllers/CLAUDE.md`

## Related
- [[Home]] · [[Architecture]]
