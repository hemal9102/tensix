# 🛡️ Skill Quality Audit Report

**Skill Target:** `ponytail-debt`
**Overall Score:** `8 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 2/2 | Hyper-specific frontmatter description listing exact triggers ("ponytail debt", "ponytail ledger") and scope boundaries. |
| **2. Single Responsibility** | 1/2 | Single core responsibility (harvesting ponytail debt markers into a ledger), but includes ~220 lines of injected web-engineering prompt bloat. |
| **3. Token Efficiency** | 1/2 | Total length is 269 lines (within 150–300 range), but 80%+ consists of redundant injected prompt boilerplate. |
| **4. Constraint Enforcement** | 2/2 | Explicit execution constraints, exact grep command rules, rot-risk tagging (`no-trigger`), and output templates. |
| **5. Verification Loop** | 2/2 | Deterministic verification using shell pattern matching (`grep -rnE '(#|//) ?ponytail:' .`) to construct the report. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Prompt Injection Pollution:** Lines 49–269 contain injected Next.js 15, Core Web Vitals, and Lighthouse audit guidelines completely unrelated to tracking code comments and debt ledgers.
* **Redundant Instruction Overhead:** Over 2,000 tokens wasted on every trigger execution due to appended web engineer prompt injection.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Purge Prompt Injection:** Remove lines 49–269 completely to reduce line count from 269 down to ~45 lines.
2. **Preserve Command & Output Syntax:** Retain the deterministic grep pattern and ledger formatting rules.
3. **Add Save File Option:** Keep the optional `PONYTAIL-DEBT.md` file generation instructions.

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: ponytail-debt
description: Harvests every `ponytail:` comment in the codebase into a debt ledger to track deliberate shortcuts and deferrals. Use when the user asks for "ponytail debt", "ponytail ledger", or "list shortcuts". Read-only report. Do NOT use for active code editing or general todo tracking.
---

# Ponytail Debt Ledger

Harvests deliberate engineering deferrals and shortcuts marked with `ponytail:` comments across the repository into a central ledger.

## 1. Extraction Protocol

Execute regex scanning across all code files (excluding `.git`, `node_modules`, `dist`, `build`):

```bash
grep -rnE '(#|//|/\*) ?ponytail:' . --exclude-dir={node_modules,.git,dist,build,out}
```

---

## 2. Formatting & Classification Rules

1. Format each output line as:
   ```text
   <file>:<line>, <what was simplified>. ceiling: <limit named>. upgrade: <trigger to revisit>.
   ```
2. **Rot Risk Tagging:** If a `ponytail:` comment names no upgrade trigger or ceiling condition, append `[no-trigger]` tag to flag silent rotting.

---

## 3. Report Output Template

Group findings by file and conclude with the ledger summary:

```text
[file:line], [summary]. ceiling: [limit]. upgrade: [trigger].
...
--------------------------------------------------
Total: <N> markers found, <M> with no trigger.
```

*If no markers are found, output:* `No ponytail debt. Clean ledger.`
```
