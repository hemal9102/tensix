---
title: Automations & D:\ Pendrive Backup Pipeline
tags: [automation, backup, infra, deploy]
updated: 2026-07-29
---

# Automations & D:\ Pendrive Backup Pipeline

**Purpose:** Documents the automated data pipelines, background servers, and physical off-site backup workflow.

**Summary:** Manages the integration between local automation scripts, remote SSH CLI execution on Hostinger shared hosting, and physical backup to external drive `D:\jobrecruitment_backup`.

## 1. Physical Pendrive Backup (`D:\jobrecruitment_backup`)
Driven by `automation/sync_live_to_pendrive.bat`:
1. **Remote DB Export**: Executes `wsl ssh` command to trigger `php backend/cli/export_applications.php` on the live server.
2. **WSL Staging**: Pulls database SQL exports (`.private/db_export/`), candidate resumes (`.private/docs/resumes/`), and documents to WSL `/tmp/hk_backup_stage` using `rsync`.
3. **Robocopy Mirroring to D:\**: Mirrored to `D:\jobrecruitment_backup\` using Windows `robocopy /MIR` for resilient physical drive synchronization.

## 2. CV Parsing & AI Resume Processing
- **Server**: `automation/cv_parser_server.py` runs local resume parsing service.
- **Batch Processing**: `automation/bulk_upload_resumes.py` and `automation/upload-resumes.bat`.
- **ML Training**: `ml_resume_parser/train_resume_parser.py` trains custom extraction models.

## 3. Tunneling & Deployment
- **Cloudflare Tunnel**: `automation/start-cloudflared.bat` and `install-cloudflared.bat` for secure webhook access.
- **Hostinger Deploy**: `deploy.sh` utilizes `.rsyncignore` to shield private data and `knowledge-vault/` from public web deployment.

## Related
- [[00-MOC/System-Architecture|System Architecture MOC]]
- [[Areas/Database-Architecture|Database Architecture]]
