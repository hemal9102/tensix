# 🛡️ Skill Quality Audit Report

**Skill Target:** `gsc_instant_indexing`
**Overall Score:** `7 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Descriptive trigger, but name mismatch (`gsc-instant-indexing` vs directory `gsc_instant_indexing`) and lacks negative triggers. |
| **2. Single Responsibility** | 1/2 | Dedicated to GSC Indexing API, but hardcodes specific environment paths (`H:\portfolio_website...`) and domains (`hemalshah.vercel.app`). |
| **3. Token Efficiency** | 2/2 | Very efficient document layout at 62 lines. |
| **4. Constraint Enforcement** | 1/2 | Good policy context provided, but lacks strict negative rules (`❌ Don't`) and quota guardrails. |
| **5. Verification Loop** | 2/2 | Includes terminal execution commands and explicit success criteria (`HTTP Status [200 OK]`). |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Hardcoded Absolute File Paths & Domains (Lines 29, 34, 42):** References specific local paths `H:\portfolio_website\hemalshah\google-service-account.json`, specific domains `hemalshah.vercel.app`, and local python script `submit_gsc_indexing.py`.
* **Name Mismatch:** YAML frontmatter uses `name: gsc-instant-indexing` (hyphen) whereas the skill directory is `gsc_instant_indexing` (underscore).
* **Missing Negative Trigger & Quota Enforcement:** Lacks explicit warnings against over-submitting non-supported content types or exceeding Google Indexing API daily quota limits (200 requests/day).

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Fix Frontmatter & Naming:** Synchronize skill name in YAML with directory name (`gsc_instant_indexing`) and add explicit `when NOT to use` rules.
2. **Generalize Paths & Credentials:** Replace hardcoded user directory paths and domain names with environment variables/configurable flags (e.g., `GOOGLE_APPLICATION_CREDENTIALS`).
3. **Add Quota Guardrails:** Add strict rules on daily quota limits and content type warnings.

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: gsc_instant_indexing
description: Submits URLs directly to the Google Search Console Indexing API for rapid crawling and indexing notifications. Use when publishing or updating high-priority pages. Do NOT use for Bing/Yandex indexing (use indexnow instead) or for non-urgent bulk page updates exceeding 200 URLs/day.
tools: [run_command]
---

## Purpose

Notify Googlebot instantly of new or updated pages using the Google Search Console Indexing API.

---

## Execution Rules & Constraints

### ❌ Never Do
- Never exceed the daily quota of 200 API calls per Google Cloud project.
- Never use this tool for low-quality, thin, or soft-404 pages.
- Never hardcode service account credentials directly in source code.

### ✅ Always Do
- Store service account key path in `GOOGLE_APPLICATION_CREDENTIALS` environment variable.
- Ensure the Service Account email is added as an **Owner** in Google Search Console.
- Verify structured data validity using Rich Results Test before requesting indexing.

---

## Execution & Automated Submission

1. Verify environment configuration:
   ```bash
   python -c "import os; assert os.path.exists(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'google-service-account.json')), 'Key file missing'"
   ```

2. Execute indexing submission script:
   ```bash
   python scripts/submit_gsc_indexing.py --sitemap sitemap.xml
   ```

---

## Verification & Validation

* Verify output logs for HTTP status code: `200 OK`.
* Expected response schema:
  ```json
  {
    "urlNotificationMetadata": {
      "url": "https://example.com/page",
      "latestUpdate": { "type": "URL_UPDATED" }
    }
  }
  ```
```
