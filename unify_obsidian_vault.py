import os, sys, shutil, json, time, hashlib
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path("D:/projects/tensix")
VAULT = ROOT / "knowledge-vault"

print(f"[*] Starting Obsidian Vault Consolidation at: {VAULT}")
VAULT.mkdir(exist_ok=True)

# 1. Ensure target folders exist in knowledge-vault
TARGET_DIRS = [
    VAULT / "00-MOC",
    VAULT / "01-System-And-Memory",
    VAULT / "02-Projects",
    VAULT / "03-Business-And-Strategy",
    VAULT / "04-Research-And-GEO",
    VAULT / "05-Permanent",
    VAULT / "06-Decisions",
    VAULT / "07-Areas",
    VAULT / "08-Knowledge-And-Skills",
    VAULT / "09-Archive",
    VAULT / "Attachments",
    VAULT / ".obsidian",
]

for d in TARGET_DIRS:
    d.mkdir(parents=True, exist_ok=True)

# Helper to safely move or merge directories
def safe_move_or_merge(src: Path, dst: Path):
    if not src.exists():
        return
    print(f"[MOVE] {src.name} -> {dst.relative_to(VAULT)}")
    if not dst.exists():
        shutil.move(str(src), str(dst))
    else:
        for item in src.iterdir():
            target_item = dst / item.name
            if target_item.exists():
                if item.is_dir():
                    safe_move_or_merge(item, target_item)
                else:
                    # Rename or replace if newer
                    shutil.copy2(str(item), str(target_item))
                    item.unlink()
            else:
                shutil.move(str(item), str(target_item))
        # Remove empty src directory
        try:
            src.rmdir()
        except Exception:
            pass

# 2. Consolidate numeric folders into vault
safe_move_or_merge(ROOT / "00_System", VAULT / "01-System-And-Memory" / "System")
safe_move_or_merge(ROOT / "01_Memory", VAULT / "01-System-And-Memory" / "Memory")
safe_move_or_merge(ROOT / "07_AI", VAULT / "01-System-And-Memory" / "AI")

safe_move_or_merge(ROOT / "02_Projects", VAULT / "02-Projects")

safe_move_or_merge(ROOT / "06_Business", VAULT / "03-Business-And-Strategy")
safe_move_or_merge(ROOT / "08_Life", VAULT / "03-Business-And-Strategy" / "Life")

safe_move_or_merge(ROOT / "knowledge_base", VAULT / "04-Research-And-GEO" / "knowledge_base")

safe_move_or_merge(ROOT / "03_Skills", VAULT / "08-Knowledge-And-Skills" / "Skills_Overview")
safe_move_or_merge(ROOT / "04_Knowledge", VAULT / "08-Knowledge-And-Skills" / "Knowledge_Base")
safe_move_or_merge(ROOT / "05_Learning", VAULT / "08-Knowledge-And-Skills" / "Learning")
safe_move_or_merge(ROOT / "skill_audits", VAULT / "08-Knowledge-And-Skills" / "Skill_Audits")

safe_move_or_merge(ROOT / "09_Archive", VAULT / "09-Archive" / "Legacy_09_Archive")

# Merge existing Permanent, Decisions, Areas, Projects inside knowledge-vault
if (VAULT / "Permanent").exists() and (VAULT / "05-Permanent").resolve() != (VAULT / "Permanent").resolve():
    safe_move_or_merge(VAULT / "Permanent", VAULT / "05-Permanent")

if (VAULT / "Decisions").exists() and (VAULT / "06-Decisions").resolve() != (VAULT / "Decisions").resolve():
    safe_move_or_merge(VAULT / "Decisions", VAULT / "06-Decisions")

if (VAULT / "Areas").exists() and (VAULT / "07-Areas").resolve() != (VAULT / "Areas").resolve():
    safe_move_or_merge(VAULT / "Areas", VAULT / "07-Areas")

if (VAULT / "Projects").exists() and (VAULT / "02-Projects").resolve() != (VAULT / "Projects").resolve():
    safe_move_or_merge(VAULT / "Projects", VAULT / "02-Projects")

if (VAULT / "Archive").exists() and (VAULT / "09-Archive").resolve() != (VAULT / "Archive").resolve():
    safe_move_or_merge(VAULT / "Archive", VAULT / "09-Archive")

# 3. Copy root markdown docs into vault
ROOT_DOCS = [
    ("DOCS_GEO_RESEARCH_IMPLEMENTATION.md", VAULT / "04-Research-And-GEO" / "DOCS_GEO_RESEARCH_IMPLEMENTATION.md"),
    ("MASTER_PROMPT.md", VAULT / "01-System-And-Memory" / "MASTER_PROMPT.md"),
    ("SECURITY_REVIEW.md", VAULT / "01-System-And-Memory" / "SECURITY_REVIEW.md"),
    ("KPI_TRACKING.md", VAULT / "03-Business-And-Strategy" / "KPI_TRACKING.md"),
    ("NEURAL_DECISION_BOUNDARY_EMAIL.md", VAULT / "03-Business-And-Strategy" / "NEURAL_DECISION_BOUNDARY_EMAIL.md"),
    ("optimization_log.md", VAULT / "09-Archive" / "optimization_log.md"),
    ("README.md", VAULT / "00-MOC" / "TENSIX_Repository_README.md"),
]

for src_name, dst_path in ROOT_DOCS:
    src_file = ROOT / src_name
    if src_file.exists():
        shutil.copy2(str(src_file), str(dst_path))
        print(f"[COPY ROOT DOC] {src_name} -> {dst_path.relative_to(VAULT)}")

print("[OK] All markdown files and documentation unified into knowledge-vault.")
