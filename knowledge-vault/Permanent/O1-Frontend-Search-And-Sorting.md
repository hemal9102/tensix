---
title: O(1) Frontend Search And Sorting
tags: [frontend, performance, features]
updated: 2026-08-01
---
# O(1) Frontend Search And Sorting

**Purpose:** Ensure large datasets (Candidates/Jobs) filter instantly on the frontend.
**Summary:** Implemented a hashed multi-dimensional lookup and explicit Recents-first sorting.

## Content
- **O(1) Search:** Built an inverted index in `candidates.js` for City, Company, and Area to allow sub-millisecond filtering.
- **Explicit Date Sort:** Replaced default database ordering with a forced JavaScript `.sort((a,b) => dateB - dateA)` on `true_upload_timestamp` / `postDate` to strictly enforce a "Newest First" visual flow for recruiters.

## Related
- [[Job-Recruitment-Migration-MOC]]
- Repo: `../../admin/js/candidates.js`, `../../admin/js/jobs.js`
