# 🛡️ Skill Quality Audit Report

**Skill Target:** `indexnow`
**Overall Score:** `7 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Clear trigger description, but name mismatch in YAML (`indexnow-submission` vs folder `indexnow`) and missing negative triggers. |
| **2. Single Responsibility** | 1/2 | Single domain (IndexNow protocol), but hardcodes specific local paths (`C:\dump\hemalshah`) and specific key filenames (`c4b69324e...txt`). |
| **3. Token Efficiency** | 2/2 | Exceptionally concise at 36 lines. |
| **4. Constraint Enforcement** | 1/2 | Easy-to-follow steps, but lacks strict negative rules (`❌ Don't`) and key location validation checks. |
| **5. Verification Loop** | 2/2 | Includes terminal execution command (`python submit_indexnow.py`) and explicit status check (`HTTP Status 200`). |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Hardcoded Local Directories & Keys (Lines 24, 25):** References hardcoded path `C:\dump\hemalshah` and a specific static key file `c4b69324e9334bbba3ff6f3f02db4fb6.txt`.
* **Name Mismatch:** YAML name field is `indexnow-submission`, while the directory is named `indexnow`.
* **Missing Negative Trigger:** Does not explicitly clarify that IndexNow is NOT supported by Google (Google uses GSC Indexing API / `gsc_instant_indexing`).

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Synchronize Naming & Add Negative Triggers:** Update YAML name to `indexnow` and add explicit `when NOT to use` (e.g. for Google indexing).
2. **Generalize Key & Path Parameters:** Parameterize key location and host domain instead of hardcoding user paths.
3. **Add Key File Verification Step:** Add an explicit automated pre-check to confirm the verification key file is publicly accessible.

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: indexnow
description: Submits updated website URLs to Bing, Yandex, and Seznam via the IndexNow API for instant indexing. Use ONLY when updating pages intended for IndexNow search engines. Do NOT use for Google Search indexing (use gsc_instant_indexing instead).
tools: [run_command]
---

## Purpose

Notify Bing, Yandex, and other IndexNow-compliant search engines instantly when web content or structured metadata changes.

---

## Execution Guardrails

### ❌ Never Do
- Never submit URLs without ensuring the IndexNow API key file is hosted at root domain (`/INDEXNOW_KEY.txt`).
- Never submit broken 404 or un-indexed URLs to the API.

### ✅ Always Do
- Validate key file accessibility (`curl -I https://your-domain.com/<key>.txt`) prior to submission.
- Ensure sitemap URLs match the exact canonical domain structure.

---

## Automated Submission Workflow

1. Validate key file presence on server:
   ```bash
   curl -s -f https://example.com/c4b69324e9334bbba3ff6f3f02db4fb6.txt > /dev/null && echo "Key Validated"
   ```

2. Execute submission script:
   ```bash
   python scripts/submit_indexnow.py --sitemap sitemap.xml
   ```

---

## Verification & Response Validation

* Check script output for HTTP status code: `200 OK` (or `202 Accepted`).
* HTTP Status Codes:
  * `200`: URLs submitted successfully.
  * `202`: Key valid, submission queued.
  * `403`: Invalid API key or domain mismatch.
```
