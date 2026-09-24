---
name: automate-indexnow
description: Automates URL submission to search engines (Bing, Yandex, Seznam, Naver) via the IndexNow protocol. Use when updating or adding website content to notify non-Google search engines instantly. Do NOT use for Google Search Console (GSC).
---

# IndexNow Protocol Automation

Instantly notify participating search engines (Bing, Yandex, Seznam.cz, Naver) of updated or newly added URLs via IndexNow.

## Core Principles
- Single endpoint submission (`api.indexnow.org` or `bing.com`) distributes notifications across all participating engines.
- Domain ownership verified using a hosted `.txt` key file at root.

---

## Workflow & Verification

### 1. Key & Hosting Setup
1. Generate an API Key string (8–128 alphanumeric/dash characters).
2. Create `<KEY>.txt` containing `<KEY>` UTF-8 plain text.
3. Host at `https://<DOMAIN>/<KEY>.txt` and ensure public HTTP 200 access.

### 2. Operational Rules

#### ✅ Do
- Batch up to 10,000 URLs per POST request.
- Verify key file accessibility via HTTP GET prior to API requests.
- Handle responses: `200 OK` (Success), `202 Accepted` (Pending key check), `403 Forbidden` (Key check failed), `422` (Host/URL mismatch).

#### ❌ Don't
- Do NOT exceed 10,000 URLs per payload.
- Do NOT submit URLs belonging to a domain other than the specified `host`.
- Do NOT repeatedly ping unchanged URLs.

---

## Implementation Example (Python)

```python
import json
import requests

def submit_indexnow(host: str, key: str, key_location: str, urls: list[str]) -> int:
    if not urls:
        return 0
    
    endpoint = "https://api.indexnow.org/indexnow"
    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": urls[:10000]
    }
    
    response = requests.post(
        endpoint,
        headers={"Content-Type": "application/json; charset=utf-8"},
        data=json.dumps(payload),
        timeout=10
    )
    response.raise_for_status()
    return response.status_code
```

---

## Verification Loop

1. **Verify Key File**:
   ```bash
   curl -s -I "https://<DOMAIN>/<KEY>.txt" | grep "200 OK"
   ```
2. **Execution Check**: Verify HTTP 200 or 202 status code returned from `api.indexnow.org`. Log response to `indexnow_submission.log`.
