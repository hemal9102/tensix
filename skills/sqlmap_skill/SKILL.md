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
