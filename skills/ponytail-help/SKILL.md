---
name: ponytail-help
description: >
  Displays reference documentation and command guides for the ponytail skill family.
  Use when the user asks "/ponytail-help", "ponytail help", "what ponytail commands", or "how do I use ponytail".
  Do NOT use to execute ponytail commands or modify configuration settings.
---

# Ponytail Help

Provides a quick reference guide for ponytail intensity levels, sub-skills, configuration options, and command usages.

## Intensity Modes
| Level | Command / Trigger | Description |
|---|---|---|
| **Lite** | `/ponytail lite` | Build requested solution, suggest minimal alternative in one line. |
| **Full** | `/ponytail` | Enforce ladder: YAGNI → stdlib → native → one line → minimum. (Default) |
| **Ultra** | `/ponytail ultra` | Strict YAGNI. Deletion first, challenge requirements before building. |

## Sub-Skill Overview
| Skill | Slash Command | Purpose |
|---|---|---|
| **ponytail** | `/ponytail` | Enforce minimal, lazy code solutions. |
| **ponytail-audit** | `/ponytail-audit` | Repo-wide over-engineering scan. |
| **ponytail-debt** | `/ponytail-debt` | Harvest `ponytail:` comments into a debt ledger. |
| **ponytail-gain** | `/ponytail-gain` | Show benchmark impact and efficiency scoreboard. |
| **ponytail-help** | `/ponytail-help` | Display this reference documentation. |

## Configuration & Environment
- Deactivate: Say `stop ponytail` or `normal mode`, or run `/ponytail off`.
- Default Mode Priority: `PONYTAIL_DEFAULT_MODE` env var > `~/.config/ponytail/config.json` > `full`.

## Negative Constraints
- ❌ **No Interactive State Changes:** Output documentation text only without changing session variables.

## Verification & Grounding Loop
1. Ensure all listed slash commands match current skill names.
