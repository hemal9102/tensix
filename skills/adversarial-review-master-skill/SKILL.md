---
name: adversarial-review-master-skill
description: Performs aggressive adversarial code review, anti-bloat audits, and behavior-preserving code simplification. Use when reviewing pull requests, refactoring over-engineered logic, eliminating unnecessary abstractions or dependencies, or reducing code footprint. Do NOT use for initial feature drafting or when adding expansive new capabilities.
---

# Adversarial Code Review & Simplification

Applies strict restraint, code simplification, and adversarial auditing to reduce codebase complexity, eliminate bloat, and maintain minimal diff footprint while preserving exact runtime behavior.

---

## Core Principles & Rules

1. **Restraint Over Expansion (Moyu Principle)**
   - Touch only explicitly specified files and lines.
   - Prefer existing built-in features and codebase helpers over new dependencies or abstractions.
   - Eliminate unnecessary wrapper classes, single-use interfaces, and redundant intermediate state.

2. **Behavior Preservation**
   - Ensure external contracts, return values, exception types, and side effects remain 100% identical.
   - Do not alter formatting or indentation outside of functional change lines.

3. **Adversarial Audit Vectors**
   - **Scope Control:** Check diff for scope creep, unrequested comments, or unsolicited test additions.
   - **Structural Complexity:** Replace nested ternaries, deep conditional branches, and flag arguments with clear guard clauses or direct return paths.
   - **Dependency Bloat:** Remove unnecessary libraries when standard/built-in methods suffice.

---

## Execution Workflow

1. **Scope Determination & Diff Analysis**
   - Inspect precise file target lines via git diff or file view before making modifications.
2. **Multi-Perspective Audit**
   - *Code Reuse:* Identify pre-existing helpers in the codebase.
   - *Quality & Clarity:* Identify redundant state, dead code, or stringly-typed variables.
   - *Efficiency:* Eliminate duplicate reads, unnecessary re-renders, or hot-path allocations.
3. **Refactoring & Simplification Edit**
   - Apply minimal, targeted edits preserving exact functionality.
4. **Verification & Testing**
   - Run existing unit tests or linter commands to verify 0 regressions.
