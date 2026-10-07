---
title: SEO Indexing Automation (IndexNow & GSC)
tags: [seo, automation, infrastructure]
updated: 2026-07-30
---

# SEO Indexing Automation (IndexNow & GSC)

**Purpose:** Document the automated scripts used to force-index our job pages across major search engines.

**Summary:** We use Python automation scripts in the `automation/` directory to ping IndexNow (Bing/Yandex) and Google Search Console APIs whenever sitemaps are updated, ensuring our dynamic job pages are discovered immediately.

## Content

### IndexNow Integration
- **Script:** `automation/indexnow_automation.py`
- **Key Location:** `3e4bc61efbef05cf6a367adc23ccff56.txt` in the web root.
- **Functionality:** Parses `sitemap-main.xml`, `sitemap-jobs.xml`, and `sitemap-programmatic.xml`. Submits up to 10,000 URLs per run to `api.indexnow.org`.
- **Usage:** Run `python automation/indexnow_automation.py` to push URLs to Bing, Yandex, Seznam, and Naver.

### Google Search Console (GSC) Integration
- **Script:** `automation/gsc_automation.py`
- **Authentication:** Requires a Google Cloud Service Account JSON Key stored at `.private/gsc-indexing-key.json` with `https://www.googleapis.com/auth/indexing` scopes.
- **Functionality:** Parses the same sitemaps and pushes to the Google Indexing API. 
- **Constraint:** Google strictly enforces a quota of **200 URLs per day** per project. The script is configured to slice the first 200 URLs.
- **Usage:** Run `python automation/gsc_automation.py` daily to max out the crawling quota.

## Related
- [[SEO-Architecture]]
- Repo: `../../automation/indexnow_automation.py`, `../../automation/gsc_automation.py`

## References
- [IndexNow Protocol](https://www.indexnow.org/documentation)
- [Google Indexing API](https://developers.google.com/search/apis/indexing-api/v3/quickstart)
