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
