---
title: MAS Auto-Patching Pipeline
tags: [mas, automation, ci-cd, testing]
updated: 2026-08-01
---

# MAS Auto-Patching Pipeline

**Purpose:** The automated worker pipeline that fixes the website, tests the code, and deploys it.

**Summary:** A Multi-Agent System (MAS) operates on isolated Git worktrees. It reads the error, writes the code, runs End-to-End tests, and merges the fix to production without human input.

## Content
Once a decay or error is detected, the self-healing orchestration begins:

1. **Isolation (Git Worktree):** The pipeline automatically checks out a new branch (`fix/auto-geo-update`).
2. **Diagnosis Agent:** Reads the error log and queries the [[RAG-Knowledge-Graph-Integration]] for the correct business logic.
3. **Code Agent:** Modifies the codebase. This could be rewriting a PHP controller, injecting a new keyword cluster into `index.html`, or regenerating an XML sitemap.
4. **Verification Agent:** Runs End-to-End (E2E) tests. If the tests fail (e.g., the schema is invalid), it sends the error back to the Code Agent in a loop until it passes.
5. **Deployment & Indexing:** Once verified, a shell script executes `git commit`, pushes to production, and instantly fires the **IndexNow API** and **Google Web Search Indexing API**. This forces search engines to crawl the healed page immediately, completing the loop.

## Related
- [[Self-Healing-AEO-GEO-Infra-MOC]]
