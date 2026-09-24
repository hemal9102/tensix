---
name: indexnow
description: Submit added, updated, or deleted web page URLs to participating search engines (Bing, Yandex, Seznam, Naver, Yep) using the IndexNow protocol for instant indexing. Use when publishing new pages, updating content, or after regenerating sitemaps. Do NOT use for Google (Google does not support IndexNow; use Google Search Console/Sitemaps for Google).
---

# IndexNow Instant Indexing Protocol

Notify IndexNow participating engines (Bing, Yandex, Seznam, Naver, Yep) immediately when URLs are added, updated, or deleted.

---

## Pre-requisites & Verification Setup

Before issuing IndexNow requests, ensure API key setup is verified:

1. **API Key Generation**: Generate a 32-character hex key (or 8–128 alphanumeric/hyphen string).
   ```bash
   php -r 'echo bin2hex(random_bytes(16));'
   ```
2. **Key File Deployment**: Save plain text key into `<key>.txt` at web root so `https://<host>/<key>.txt` is publicly accessible.
3. **Local Store**: Store the key in `.private/indexnow.key` (do NOT commit to public Git).

---

## 4-Step Execution Workflow

1. **Verify Host Key File**
   * Run verification check: `curl -I https://<host>/<key>.txt`
   * Confirm response is `200 OK` and body equals `<key>`.

2. **Collect Target URLs**
   * Extract absolute, URL-encoded URLs sharing the target hostname.

3. **Dispatch Payload**
   * Execute submission script or POST payload directly:
   ```bash
   # Single URL
   php .claude/skills/indexnow/scripts/submit.php https://www.example.com/job/123

   # Bulk file (one URL per line, max 10,000 per request)
   php .claude/skills/indexnow/scripts/submit.php --file changed-urls.txt
   ```

4. **Validate API Response**
   * Inspect HTTP response status against the validation table below.

---

## HTTP Response Handling

| Code | Status | Meaning | Required Action |
| :--- | :--- | :--- | :--- |
| **200** | Success | URLs accepted for indexing | None. Log success. |
| **202** | Pending | Accepted; key validation pending | Ensure `https://<host>/<key>.txt` is publicly reachable. |
| **400** | Bad Request | Invalid JSON format or URL encoding | Fix URL encoding / JSON body format. |
| **403** | Forbidden | Key invalid or key file missing | Verify key file location and exact content match. |
| **422** | Unprocessable | Host mismatch or invalid key schema | Ensure all URLs share host domain of key file. |
| **429** | Rate Limited | Request rate threshold exceeded | Exponential backoff; reduce batch sizes. |

---

## Execution Rules & Constraints

* ❌ **Don't submit Google URLs**: IndexNow is not supported by Google. Use Google Search Console / XML sitemaps.
* ❌ **Don't cross host domains**: All URLs in a single payload must belong to the exact same host domain as the key location.
* ❌ **Don't exceed payload limit**: Maximum 10,000 URLs per POST request. Split larger payloads into batches.
* ❌ **Don't submit unchanged URLs**: Only trigger submissions for newly added, updated, or removed content.

---

## Verification & Grounding Loop

1. **Pre-flight Check**: HTTP HEAD check on key location `https://<host>/<key>.txt`.
2. **Post-submission Check**: Verify HTTP 200/202 status code returned from `https://api.indexnow.org/indexnow`.
