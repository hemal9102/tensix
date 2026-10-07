# 🛡️ Skill Quality Audit Report

**Skill Target:** `ponytail-audit`
**Overall Score:** `6 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 2/2 | Precise frontmatter description with clear activation keywords ("audit for over-engineering", "find bloat") and clear scope limits. |
| **2. Single Responsibility** | 1/2 | Primary skill targets repo-wide over-engineering audits, but includes ~220 lines of injected web-engineering prompt bloat. |
| **3. Token Efficiency** | 1/2 | At 266 lines, it sits within the 150–300 range, but 80%+ of content is redundant injected boilerplate. |
| **4. Constraint Enforcement** | 2/2 | Well-defined tag taxonomy (`delete:`, `stdlib:`, `native:`, `yagni:`, `shrink:`), strict output line format, and clear scope boundaries. |
| **5. Verification Loop** | 0/2 | Completely lacks verification commands or validation scripts to confirm findings. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Injected Prompt Pollution:** Lines 46–266 contain injected web engineering rules and Next.js checklists that directly contradict the audit's stated scope boundaries ("Correctness bugs, security holes, and performance are explicitly out of scope").
* **Zero Verification Mechanism:** As a read-only one-shot auditor, it provides no script or automated command to double-check that flagged files/types are truly unreferenced or dead code before reporting them.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Purge Prompt Injection:** Strip lines 46–266 completely, bringing the file length down to ~45 lines.
2. **Preserve Tag Taxonomy & Output Rules:** Maintain the 5 audit tags and strict one-line output format.
3. **Add Verification Commands:** Include automated grep/ast commands to verify dead code or unused dependencies before listing them in the report.

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: ponytail-audit
description: Scans an entire repository for over-engineering, bloat, and unused abstractions. Outputs a ranked list of items to delete, simplify, or replace with stdlib/native equivalents. Use when the user requests a whole-codebase bloat or YAGNI audit. Do NOT use for single-file reviews, bug fixing, performance profiling, or applying code changes.
---

# Ponytail Repository Audit

Scans the entire codebase to detect over-engineering, speculative abstractions, and redundant dependencies.

## 1. Audit Taxonomy & Classification

Flag issues using strictly these 5 tags:

| Tag | Flag Criteria | Action / Replacement |
| :--- | :--- | :--- |
| `delete:` | Dead code, unused flags, speculative features | Remove entirely (no replacement) |
| `stdlib:` | Custom utility duplicating standard library | Replace with native stdlib call |
| `native:` | External dependency doing what platform supports | Replace with browser/OS native API |
| `yagni:` | Interface with 1 impl, factory with 1 product | Flatten abstraction |
| `shrink:` | Verbose logic that can be written in fewer lines | Simplify implementation |

> ❌ **Out of Scope:** Correctness bugs, security vulnerabilities, and performance tuning are strictly out of scope. Route those to dedicated security or performance checkers.

---

## 2. Output Format

Print findings ranked by line reduction impact (largest cut first):

```text
<tag> <what to cut>. <replacement>. [<path>]
```

End the report with:
```text
net: -<N> lines, -<M> deps possible.
```

---

## 3. Verification Protocol

Before reporting a file/symbol as dead or candidate for `delete:` / `yagni:`, run static reference checks:

```bash
# Verify symbol has zero external callers
grep -rn "TargetSymbol" src/ | wc -l
```

- [ ] Every `delete:` item confirmed to have 0 active callers.
- [ ] Every `stdlib:` recommendation verified against target runtime version.
```
