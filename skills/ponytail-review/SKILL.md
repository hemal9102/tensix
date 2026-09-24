---
name: ponytail-review
description: >
  Reviews diffs, pull requests, or code snippets specifically for over-engineering and unnecessary complexity.
  Use when the user requests "review this diff for over-engineering", "ponytail-review", "/ponytail-review",
  or "find bloat in this PR".
  Do NOT use for full codebase audits (use ponytail-audit), general security scanning, or formatting/lint checks.
---

# Ponytail Review

Performs an over-engineering code review on diffs, staged changes, or snippets. Tags specific line numbers with concrete deletion or simplification feedback.

## Line Tagging Schema
For each line or block containing bloat, prepend one of the following tags:
- `L<line_number>: delete: <description>` (Dead code, speculative features, unused wrappers)
- `L<line_number>: stdlib: <function>` (Replace custom logic with standard library call)
- `L<line_number>: native: <feature>` (Replace custom code or library with native platform features)
- `L<line_number>: yagni: <reason>` (Remove single-implementation abstractions or unused flexibility)
- `L<line_number>: shrink: <shorter form>` (Express identical logic in fewer lines)

## Review Protocol
1. Focus exclusively on diff changes and their immediate call site impact.
2. Provide concise inline comments indicating line numbers, tag, and exact replacement.
3. Summary line: End with estimated line savings (e.g., `net: -14 lines`).
4. If code is minimal: `Lean diff. Ship.`

## Negative Constraints
- ❌ **No Style/Lint Nitpicks:** Ignore formatting, variable naming preferences, and minor stylistic choices.
- ❌ **No Security/Bug Auditing:** Direct non-complexity issues (e.g. race conditions, injection flaws) to appropriate review tools.

## Verification & Grounding Loop
1. Verify line numbers match current diff context.
2. Confirm suggested stdlib or native replacements exist in target environment/language version.
