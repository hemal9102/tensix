import os, sys, json, time, hashlib
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

VAULT = Path("D:/projects/tensix/knowledge-vault")
OBSIDIAN_DIR = VAULT / ".obsidian"
OBSIDIAN_DIR.mkdir(exist_ok=True)

# 1. Write .obsidian/app.json
app_config = {
    "useMarkdownLinks": False,
    "newFileLocation": "current",
    "attachmentFolderPath": "Attachments",
    "promptDelete": False,
    "alwaysUpdateLinks": True,
    "showLineNumber": True,
    "foldHeading": True,
    "foldIndent": True,
    "tabSize": 2
}
with open(OBSIDIAN_DIR / "app.json", "w", encoding="utf-8") as f:
    json.dump(app_config, f, indent=2)
print("[OBSIDIAN] Wrote app.json")

# 2. Write .obsidian/core-plugins.json
core_plugins = [
    "file-explorer",
    "global-search",
    "switcher",
    "graph",
    "backlink",
    "canvas",
    "outgoing-link",
    "tag-pane",
    "page-preview",
    "daily-notes",
    "templates",
    "note-composer",
    "command-palette",
    "markdown-importer",
    "word-count",
    "outline",
    "bookmarks"
]
with open(OBSIDIAN_DIR / "core-plugins.json", "w", encoding="utf-8") as f:
    json.dump(core_plugins, f, indent=2)
print("[OBSIDIAN] Wrote core-plugins.json")

# 3. Write .obsidian/appearance.json
appearance = {
    "baseFontSize": 16,
    "theme": "obsidian",
    "accentColor": "#1d4ed8",
    "cssTheme": ""
}
with open(OBSIDIAN_DIR / "appearance.json", "w", encoding="utf-8") as f:
    json.dump(appearance, f, indent=2)
print("[OBSIDIAN] Wrote appearance.json")

# 4. Write .obsidian/graph.json
graph_config = {
    "collapse-filter": False,
    "search": "",
    "colorGroups": [
        {"query": "path:00-MOC", "color": {"a": 1, "rgb": 16737792}},         # Yellow
        {"query": "path:01-System-And-Memory", "color": {"a": 1, "rgb": 4159487}}, # Blue
        {"query": "path:02-Projects", "color": {"a": 1, "rgb": 5824767}},      # Cyan
        {"query": "path:03-Business-And-Strategy", "color": {"a": 1, "rgb": 15418879}}, # Pink
        {"query": "path:04-Research-And-GEO", "color": {"a": 1, "rgb": 4443903}}, # Emerald/Green
        {"query": "path:05-Permanent", "color": {"a": 1, "rgb": 10839039}},    # Purple
        {"query": "path:06-Decisions", "color": {"a": 1, "rgb": 16744272}},    # Orange
        {"query": "path:07-Areas", "color": {"a": 1, "rgb": 3394815}},        # Indigo
        {"query": "path:08-Knowledge-And-Skills", "color": {"a": 1, "rgb": 10066329}}, # Gray
        {"query": "path:09-Archive", "color": {"a": 1, "rgb": 5592405}}        # Dark Gray
    ]
}
with open(OBSIDIAN_DIR / "graph.json", "w", encoding="utf-8") as f:
    json.dump(graph_config, f, indent=2)
print("[OBSIDIAN] Wrote graph.json")

# 5. Connect with Obsidian application (%APPDATA%/obsidian/obsidian.json)
appdata = os.environ.get("APPDATA")
if appdata:
    obsidian_json_path = Path(appdata) / "obsidian" / "obsidian.json"
    if obsidian_json_path.exists():
        try:
            with open(obsidian_json_path, "r", encoding="utf-8") as f:
                obs_data = json.load(f)
            
            vaults = obs_data.setdefault("vaults", {})
            vault_str_path = str(VAULT.resolve())
            
            # Check if already present
            found = False
            for vid, vinfo in vaults.items():
                if os.path.normpath(vinfo.get("path", "")) == os.path.normpath(vault_str_path):
                    found = True
                    vinfo["open"] = True
                    vinfo["ts"] = int(time.time() * 1000)
                    print(f"[OBSIDIAN REGISTRATION] Vault already registered with id {vid}, marked active.")
                    break
            
            if not found:
                vault_id = hashlib.md5(vault_str_path.encode()).hexdigest()[:16]
                vaults[vault_id] = {
                    "path": vault_str_path,
                    "ts": int(time.time() * 1000),
                    "open": True
                }
                print(f"[OBSIDIAN REGISTRATION] Successfully registered new vault ID: {vault_id} -> {vault_str_path}")
            
            with open(obsidian_json_path, "w", encoding="utf-8") as f:
                json.dump(obs_data, f, indent=2)
            print("[OBSIDIAN REGISTRATION] obsidian.json updated successfully!")
        except Exception as e:
            print(f"[WARN] Could not update obsidian.json: {e}")
