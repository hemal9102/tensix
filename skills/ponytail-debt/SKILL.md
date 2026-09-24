---
name: ponytail-debt
description: >
  Harvests all `ponytail:` inline comments across a codebase into a consolidated debt ledger.
  Use when the user asks "ponytail debt", "/ponytail-debt", "what did ponytail defer", "list the shortcuts",
  "ponytail ledger", or "what did we mark to do later".
  Do NOT use for general TODO scanning, issue tracking, or code refactoring execution.
---

# Ponytail Debt

Collects and tracks deliberate shortcuts, technical debt markers, and ceiling constraints left behind by ponytail simplifications to prevent them from rotting into permanent tech debt.

## Scan Protocol
Scan the repository while ignoring build directories and dependencies (`node_modules`, `.git`, `dist`, `build`):
- Match explicit pattern: `(#|//) ?ponytail:`
- Extract the file path, line number, ceiling description, and upgrade trigger.

## Ledger Output Structure
Output a structured Markdown table or list:
- Format per item: `<file>:<line>, <simplification description>. ceiling: <limit>. upgrade: <trigger>.`
- Flag items missing upgrade criteria: Tag as `no-trigger` if no explicit upgrade condition is specified.
- Summary line: `<N> markers found, <M> missing upgrade triggers.`
- If clean: `No ponytail debt found. Ledger is clean.`

## Negative Constraints
- ❌ **No Code Edits:** Operate strictly as a read-only reporting tool unless explicitly asked to save output to `PONYTAIL-DEBT.md`.
- ❌ **No False Matches:** Filter out comments that merely reference ponytail conventions rather than active debt markers.

## Verification & Grounding Loop
1. Verify line numbers and file paths against actual repository state.
2. Confirm comment syntax matches valid code comment delimiters for target language.
