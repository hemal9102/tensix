---
title: Deploy MOC
tags: [moc, deploy]
updated: 2026-07-20
---

# Deploy — Map of Content

**Purpose:** How code reaches production, and the traps.

**Summary:** Two deploy paths with DIFFERENT behavior. Default push = production. Never merge dev→production.

## Key facts (from memory — verify before acting)
- **`git push` (GitHub Actions):** ignores `.rsyncignore` and uses `--delete` → can remove server files not in the repo. Destructive-capable.
- **`deploy.sh push`:** honors `.rsyncignore`, additive-only (safer).
- Default push targets **production**; cherry-pick, don't merge dev→production. Python/CV-parser stays on dev branch only.
- Never-deploy (rsyncignored): `.private/config.json`, `.env`, `knowledge-vault/`, `.claude/`, sessions, uploads.
- Host: Hostinger (sync host `217.21.74.188:65002`, path `domains/jobrecruitment.in/public_html`). Cloudflare CDN in front.

## Source-of-truth
- `../../.rsyncignore` · Root `../../CLAUDE.md` (Never list)
- Memory: `project-deploy-path-mismatch.md`, `feedback-branch-deploy-rule.md`

## Related
- [[Home]] · [[Architecture]]
