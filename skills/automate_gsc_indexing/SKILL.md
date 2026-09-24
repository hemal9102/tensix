---
name: automate-gsc-indexing
description: Automates URL submissions and indexing checks via Google Search Console (GSC) Web Search Indexing API. Use when publishing new pages or bulk updates needing fast Google crawling. Do NOT use for Bing, Yandex, non-GSC search engines, or routine sitemap generation.
---

# Google Search Console Indexing Automation

Automate page indexing requests and status checks via the GSC Indexing API for rapid Google search engine crawling.

## Core Capabilities
- Authenticate via Google Cloud Service Account with GSC Owner privileges.
- Submit new or updated URLs (`URL_UPDATED`) or request removal (`URL_DELETED`).
- Manage API quotas (default 200 Indexing requests/day, 2,000 Inspection requests/day).

---

## Workflow & Constraints

### 1. Prerequisites Checklist
- [ ] Google Cloud Project with **Web Search Indexing API** enabled.
- [ ] Service Account created with a downloaded JSON key file (`service-account.json`).
- [ ] Service Account email added as **Owner** in Google Search Console for target domain.

### 2. Execution Rules & Rules of Engagement

#### ✅ Do
- Filter sitemaps by `<lastmod>` to submit only changed or new URLs within the last 7 days.
- Track submission timestamps in local database/storage to avoid redundant submissions within 48 hours.
- Verify status codes and log `200 OK` responses.

#### ❌ Don't
- Do NOT exceed the 200 URLs/day quota without requesting quota increases.
- Do NOT attempt submission without confirming Service Account has GSC Owner permissions.
- Do NOT submit static, unchanged legacy pages repeatedly.

---

## Implementation Example (Python)

```python
import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

SERVICE_ACCOUNT_FILE = 'service-account.json'
SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

def get_authorized_session():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return AuthorizedSession(credentials)

def submit_url(url: str, action: str = "URL_UPDATED") -> dict:
    session = get_authorized_session()
    payload = {"url": url, "type": action}
    response = session.post(ENDPOINT, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()
```

---

## Verification & Grounding Loop

1. **Permission Check**: Validate authentication before batch runs:
   ```bash
   python -c "from auth_check import test_gsc_auth; print(test_gsc_auth())"
   ```
2. **Quota Audit**: Check response headers and status codes. Treat HTTP 429 as quota limit exceeded and pause execution for 24h.
3. **Execution Log**: Log all submitted URLs, status codes, and timestamps into `gsc_indexing_log.json`.
