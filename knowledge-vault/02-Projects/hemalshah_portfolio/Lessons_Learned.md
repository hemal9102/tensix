---
title: "Lessons Learned & Retrospectives"
type: "project"
status: "active"
project: "[[hemalshah_portfolio]]"
tags:
  - project
  - lessons
  - retrospective
created: 2026-07-26
updated: 2026-07-26
priority: "medium"
owner: "Hemal Shah"
---

# Lessons Learned & Retrospectives (`hemalshah_portfolio`)

## 1. Quality Over Quantity in Long-Term Brand Building
- **Lesson**: Generating hundreds of programmatic SEO pages creates short-term keyword spikes but long-term maintenance debt and vulnerability to AI spam filters.
- **Takeaway**: Focus on depth-first, high-information-gain content (benchmarks, code snippets, architecture diagrams) that proves CTO-level engineering rigor.

## 2. Internal Link Weaving is Critical for Static Sites
- **Lesson**: Adding new blog posts or pillar pages without linking them from existing high-traffic core pages (`about.html`, `services.html`, `navrangpura.html`) isolates them from PageRank flow.
- **Takeaway**: Always perform cross-linking updates whenever new content is shipped.

## 3. Machine-Readable Knowledge Endpoints (`llms.txt`) Are the New SEO
- **Lesson**: Modern AI search engines prioritize plain-text structured endpoints over parsing complex visual DOM trees.
- **Takeaway**: Maintain `llms.txt` and `llms-full.txt` as a first-class deployment artifact alongside `sitemap.xml`.
