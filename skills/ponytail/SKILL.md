---
name: ponytail
description: >
  Forces the simplest, shortest, and most minimal working solution for coding tasks (YAGNI principle).
  Use when writing, refactoring, fixing, reviewing, or designing code, selecting dependencies, or when the user mentions
  "ponytail", "be lazy", "lazy mode", "simplest solution", "minimal solution", "yagni", "do less", or "shortest path".
  Do NOT use for non-coding requests (general knowledge, prose, translation, summaries, recipes) or when complex infrastructure architecture is requested.
---

# Ponytail

Enforce maximum simplicity and minimality in all code changes. Lazy means writing clean, efficient code with zero unnecessary abstractions or debt—never careless code.

## Activation & Persistence
- Default: **full** intensity.
- Intensity levels: `lite`, `full` (default), `ultra`.
- Deactivation: Triggered by "stop ponytail" or "normal mode".

## The Decision Ladder
Evaluate rungs in order; stop at the first applicable rung:
1. **YAGNI (Does this need to exist?):** If speculative, skip it and state so in one line.
2. **Existing Code Reuse:** Reuse existing helpers, utilities, types, or patterns in the codebase.
3. **Standard Library:** Prefer stdlib implementations over custom code.
4. **Native Platform Features:** Use native HTML/CSS/DB constraints before adding JS or application logic.
5. **Existing Dependencies:** Use already-installed libraries. Never add a new dependency for what a few lines can do.
6. **One-Liner:** If it can be done safely in one line, do so.
7. **Minimum Code:** Implement the minimal necessary logic.

## Negative Constraints (What NOT to do)
- ❌ **No unrequested abstractions:** No single-implementation interfaces, single-product factories, or static configs for non-varying values.
- ❌ **No premature boilerplate:** Do not write scaffolding for future requirements.
- ❌ **No unrequested prose:** Keep explanations to 3 lines maximum unless explicitly requested.
- ❌ **No shortcutting safety:** Never omit input validation at boundaries, critical error handling, security checks, or accessibility.

## Verification & Grounding Loop
1. Trace the complete call stack and affected files before modifying code.
2. Ensure every non-trivial fix includes a minimal runnable self-check (`assert` or unit test).
3. Run project linter/tests (`npm test`, `pytest`, etc.) to confirm zero regressions before outputting completion.
