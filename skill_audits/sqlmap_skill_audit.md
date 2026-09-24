# 🛡️ Skill Quality Audit Report

**Skill Target:** `sqlmap_skill`
**Overall Score:** `7 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Specifies positive trigger clearly, but lacks explicit negative triggers (e.g., static sites, unauthorized targets). |
| **2. Single Responsibility** | 2/2 | Focused strictly on running and interpreting `sqlmap` vulnerability testing. |
| **3. Token Efficiency** | 2/2 | Very concise at 47 lines (<150 lines benchmark). |
| **4. Constraint Enforcement** | 1/2 | Includes `--batch` enforcement and warning, but lacks explicit negative rules (`❌ Don't`). |
| **5. Verification Loop** | 1/2 | Directs reading output log, but lacks a deterministic verification check or result-parsing script. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Name Mismatch (Line 2):** Frontmatter specifies `name: sqlmap` while skill directory is named `sqlmap_skill`.
* **Missing Negative Triggers (Lines 1–4):** Lacks explicit `when NOT to use` instructions (e.g., static HTML/CSS sites, untrusted/unauthorized targets).
* **Missing Negative Constraints (Lines 10–44):** Lacks explicit `❌ Don't` constraints around non-batch execution and rate limiting.
* **Informal Verification (Lines 38–39):** Verification relies on manually reading stdout without a structured check or log parsing step.

---

## 🔧 Refactoring Plan to Reach 10/10
1. Align frontmatter name with directory name (`sqlmap_skill`) and add explicit `when NOT to use` boundaries.
2. Structure explicit negative constraints (`❌ Don't`) for authorization and process hanging prevention.
3. Implement a structured result verification protocol to parse sqlmap logs for injection evidence.

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: sqlmap_skill
description: Automates SQL injection testing and database vulnerability assessment using `sqlmap`. Use when explicitly testing web applications with dynamic SQL backends for SQL injection vulnerabilities. Do NOT use on static websites (HTML/CSS/JS without backends), or unauthorized third-party targets.
tools: [Bash, Read, Write]
---

# Sqlmap Automated Vulnerability Assessment

This skill provides deterministic instructions for executing `sqlmap` to perform automated SQL injection detection and database testing.

---

## Operational Constraints

* ❌ **DO NOT** execute against targets without explicit authorization.
* ❌ **DO NOT** run `sqlmap` without the `--batch` flag in automated environments.
* ❌ **DO NOT** execute on static sites lacking database dynamic inputs.

---

## Step-by-Step Execution Protocol

1. **Locate Target & Script**: Ensure `sqlmap.py` exists in workspace or system PATH.
2. **Basic Vulnerability Scan**:
   ```bash
   python sqlmap.py -u "<TARGET_URL>" --batch --random-agent
   ```
3. **Authenticated & POST Parameter Scan**:
   ```bash
   python sqlmap.py -u "<TARGET_URL>" --data="<POST_DATA>" --cookie="<COOKIE>" --batch -p <PARAM>
   ```
4. **Database Enumeration (If Vulnerable)**:
   ```bash
   python sqlmap.py -u "<TARGET_URL>" --dbs --batch
   ```

---

## Verification & Output Validation

1. **Check Output Log**: Search scan output for explicit injection confirmation:
   ```bash
   grep -E "(is vulnerable|type:)" sqlmap_output.log
   ```
2. **Confirm Vulnerability**: Verify payload type (e.g., Boolean-based blind, Time-based blind, UNION query).
3. **Reporting**: Document parameter name, DBMS type, and proof-of-concept payload.
```
