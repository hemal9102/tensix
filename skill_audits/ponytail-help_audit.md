# 🛡️ Skill Quality Audit Report

**Skill Target:** `ponytail-help`
**Overall Score:** `4 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 2/2 | Description in frontmatter clearly defines intent, lists exact slash commands and phrase triggers (`/ponytail-help`, `"ponytail help"`, etc.), and specifies single-shot display. |
| **2. Single Responsibility** | 0/2 | Major anti-pattern! Lines 77–296 contain injected omni-rules for web engineering and performance optimization completely outside the help card's domain. |
| **3. Token Efficiency** | 1/2 | 296 lines total. Over 200 lines are redundant prompt bloat that waste context window capacity. |
| **4. Constraint Enforcement** | 1/2 | Clear rules for mode priorities (env var > config > default) and deactivation commands, but compromised by conflicting injected directives. |
| **5. Verification Loop** | 0/2 | No deterministic validation or syntax verification steps for configuration JSON or output formatting. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Injected Omni-Rules (Lines 77–296):** Appended 220 lines of unrelated instructions (Next.js 15, React 19, PHP MVC, Lighthouse protocol, performance budgets) to a quick-reference cheat sheet.
* **Context Bloat:** Wastes token bandwidth on every invocation of help.
* **Missing Verification:** No automated check to validate config path formats or JSON syntax shown in examples.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Remove Injected Directives:** Delete lines 77–296 completely.
2. **Streamline Markdown Tables:** Keep the clean cheat-sheet tables for levels, skills, deactivation, and configuration.
3. **Add Validation Rule:** Include a verification check to ensure config JSON examples conform to valid JSON format.

---

## 📦 Recommended 10/10 Refactored Version

```markdown
---
name: ponytail-help
description: >
  Quick-reference card for all ponytail modes, skills, and commands.
  One-shot display, not a persistent mode. Trigger: /ponytail-help,
  "ponytail help", "what ponytail commands", "how do I use ponytail".
---

# Ponytail Help

Display this reference card when invoked. One-shot, do NOT change mode,
write flag files, or persist anything.

## Levels

| Level | Trigger | What change |
|-------|---------|-------------|
| **Lite** | `/ponytail lite` | Build what's asked, name the lazier alternative in one line. |
| **Full** | `/ponytail` | The ladder enforced: YAGNI → stdlib → native → one line → minimum. Default. |
| **Ultra** | `/ponytail ultra` | YAGNI extremist. Deletion before addition. Challenges requirements before building. |

Level sticks until changed or session end.

## Skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| **ponytail** | `/ponytail` | Lazy mode itself. Simplest solution that works. |
| **ponytail-review** | `/ponytail-review` | Over-engineering review: `L42: yagni: factory, one product. Inline.` |
| **ponytail-audit** | `/ponytail-audit` | Whole-repo over-engineering audit: ranked list of what to delete. |
| **ponytail-debt** | `/ponytail-debt` | Harvest `ponytail:` shortcut comments into a tracked ledger. |
| **ponytail-gain** | `/ponytail-gain` | Measured-impact scoreboard: less code, less cost, more speed. |
| **ponytail-help** | `/ponytail-help` | This card. |

Codex uses `@ponytail`, `@ponytail-review`, and `@ponytail-help`; Claude Code
and OpenCode use the slash-command forms above (OpenCode ships all six as
slash commands).

## Deactivate

Say "stop ponytail" or "normal mode". Resume anytime with `/ponytail`.
`/ponytail off` also works.

## Configure Default Mode

Default mode = `full`, auto-active every session. Change it:

**Environment variable** (highest priority):
```bash
export PONYTAIL_DEFAULT_MODE=ultra
```

**Config file** (`~/.config/ponytail/config.json`, Windows: `%APPDATA%\ponytail\config.json`):
```json
{ "defaultMode": "lite" }
```

Set `"off"` to disable auto-activation on session start, activate manually
with `/ponytail` when wanted.

Resolution: env var > config file > `full`.

## Update

Enable auto-update once: open `/plugin`, go to Marketplaces, pick ponytail, Enable auto-update. Claude Code then pulls new versions at startup (run `/reload-plugins` when it prompts). Manual refresh: `/plugin marketplace update ponytail` then `/reload-plugins`.

If `/plugin` is not recognized, your Claude Code is out of date. Update it (`npm install -g @anthropic-ai/claude-code@latest`, or `brew upgrade claude-code`) and restart. Other hosts use their own update flow.

## More

Full docs + examples: https://github.com/DietrichGebert/ponytail

## Verification

Confirm all slash commands listed match currently installed plugins and config file JSON snippets validate cleanly.
```
