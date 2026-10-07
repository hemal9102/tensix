# 🛡️ Skill Quality Audit Report

**Skill Target:** `ponytail-review`
**Overall Score:** `5 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 2/2 | Frontmatter description is precise and lists triggers (`/ponytail-review`, `"review for over-engineering"`, `"what can we delete"`, etc.) and explicitly notes what is out of scope. |
| **2. Single Responsibility** | 0/2 | Anti-pattern! Lines 63–282 contain injected omni-rules for performance engineering and web development, directly contradicting the skill's explicit boundaries (which exclude performance review). |
| **3. Token Efficiency** | 1/2 | 282 lines total. Over 200 lines are unneeded prompt bloat. |
| **4. Constraint Enforcement** | 2/2 | Excellent core constraints: precise line output tags (`stdlib:`, `yagni:`, `delete:`), concise line-by-line format, concrete ✅ and ❌ examples, and explicit output metric (`net: -<N> lines possible`). |
| **5. Verification Loop** | 0/2 | No execution verification step (e.g. running unit tests after flagging code for deletion/inlining). |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Injected Omni-Rules Contradiction (Lines 63–282):** Injected instructions force performance and web engineering reviews, directly breaking line 52 ("performance are explicitly out of scope").
* **Prompt Bloat:** Context window is polluted with 220 lines of irrelevant performance checklists.
* **Missing Post-Review Verification:** No guidance on running tests to confirm that flagged abstractions can be safely removed without breaking functionality.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Remove Injected Directives:** Completely strip lines 63–282.
2. **Add Verification Loop:** Add a rule requiring test execution (e.g., `npm test` or `pytest`) after code refactoring/simplification is applied.
3. **Preserve High-Quality Core:** Retain the tag system (`delete:`, `stdlib:`, `native:`, `yagni:`, `shrink:`) and concise example structure.

---

## 📦 Recommended 10/10 Refactored Version

```markdown
---
name: ponytail-review
description: >
  Code review focused exclusively on over-engineering. Finds what to delete:
  reinvented standard library, unneeded dependencies, speculative abstractions,
  dead flexibility. One line per finding: location, what to cut, what replaces
  it. Use when the user says "review for over-engineering", "what can we
  delete", "is this over-engineered", "simplify review", or invokes
  /ponytail-review. Complements correctness-focused review, this one only
  hunts complexity.
---

Review diffs for unnecessary complexity. One line per finding: location, what
to cut, what replaces it. The diff's best outcome is getting shorter.

## Format

`L<line>: <tag> <what>. <replacement>.`, or `<file>:L<line>: ...` for
multi-file diffs.

Tags:

- `delete:` dead code, unused flexibility, speculative feature. Replacement: nothing.
- `stdlib:` hand-rolled thing the standard library ships. Name the function.
- `native:` dependency or code doing what the platform already does. Name the feature.
- `yagni:` abstraction with one implementation, config nobody sets, layer with one caller.
- `shrink:` same logic, fewer lines. Show the shorter form.

## Examples

❌ "This EmailValidator class might be more complex than necessary, have you
considered whether all these validation rules are needed at this stage?"

✅ `L12-38: stdlib: 27-line validator class. "@" in email, 1 line, real validation is the confirmation mail.`

✅ `L4: native: moment.js imported for one format call. Intl.DateTimeFormat, 0 deps.`

✅ `repo.py:L88: yagni: AbstractRepository with one implementation. Inline it until a second one exists.`

✅ `L52-71: delete: retry wrapper around an idempotent local call. Nothing replaces it.`

✅ `L30-44: shrink: manual loop builds dict. dict(zip(keys, values)), 1 line.`

## Scoring

End with the only metric that matters: `net: -<N> lines possible.`

If there is nothing to cut, say `Lean already. Ship.` and stop.

## Boundaries

Scope: over-engineering and complexity only. Correctness bugs, security holes,
and performance are explicitly out of scope. Route them to a normal review
pass, not this one. A single smoke test or `assert`-based
self-check is the ponytail minimum, not bloat, never flag it for deletion.
Does not apply the fixes, only lists them.
"stop ponytail-review" or "normal mode": revert to verbose review style.

## Verification

If suggestions are accepted and code is edited, automatically run the project's test suite to ensure functionality remains 100% intact after removing over-engineered constructs.
```
