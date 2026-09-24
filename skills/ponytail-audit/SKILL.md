---
name: ponytail-audit
description: >
  Scans an entire codebase to audit and identify over-engineering, unnecessary abstractions, and dead code.
  Use when the user requests "audit this codebase", "audit for over-engineering", "find bloat", "what can I delete",
  "ponytail-audit", or "/ponytail-audit".
  Do NOT use for single-file diffs (use ponytail-review), basic code formatting, or routine security/correctness audits.
---

# Ponytail Audit

Whole-repository audit for over-engineering and complexity. Analyzes the file tree to generate a ranked list of simplification opportunities without modifying code.

## Audit Workflow & Tagging
Identify and classify over-engineering using these standardized tags:
- `delete:` Dead code, unused flags/features, or speculative abstractions.
- `stdlib:` Hand-rolled logic that standard library functions cover.
- `native:` Custom code or dependencies replaceable by native platform capabilities.
- `yagni:` Interfaces with one implementation, unused configs, single-caller wrappers.
- `shrink:` Logic that can be implemented cleanly in significantly fewer lines.

## Output Format
1. Format findings as a ranked list (largest reduction first):
   `<tag> <item to simplify>. <suggested replacement>. [<file path>]`
2. Conclude report with total estimated line/dependency reduction:
   `net: -<N> lines, -<M> deps possible.`
3. If no bloat is found: `Lean already. Ship.`

## Negative Constraints & Boundaries
- ❌ **No Code Edits:** Report findings only; do not automatically apply changes.
- ❌ **No Security/Bug Auditing:** Scope strictly to over-engineering and structural bloat. Route correctness or security issues to dedicated review workflows.
- ❌ **No Speculative Bloat:** Do not flag necessary architectural patterns or multi-use interfaces as bloat.

## Verification & Grounding Loop
1. Verify each candidate interface/wrapper has only a single caller/implementation before tagging as `yagni`.
2. Confirm stdlib/native function signatures fully cover existing requirements before suggesting replacement.
