# 🛡️ Skill Quality Audit Report

**Skill Target:** `structured-data-validator`
**Overall Score:** `5 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Clear positive trigger, but lacks explicit negative triggers ("when NOT to use"). |
| **2. Single Responsibility** | 2/2 | Focused strictly on structured data (JSON-LD, Schema.org) validation. |
| **3. Token Efficiency** | 0/2 | **Severe Bloat (555 lines)**: Massive whitespace, repetitive single-word lists (0/2 rating). |
| **4. Constraint Enforcement** | 1/2 | Contains negative directives ("Never..."), but lacks concrete syntax examples or decision matrices. |
| **5. Verification Loop** | 1/2 | Defines a multi-step checklist, but lacks automated validation scripts or linter commands. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Massive Token Waste (Lines 50–334):** 555 total lines filled with double-spaced, single-word list items (e.g. 50+ lines listing schema types vertically), destroying context window efficiency.
* **Missing Negative Triggers (Lines 1–9):** Lacks explicit `when NOT to use` guidance (e.g., standard API JSON payloads, relational DB schemas).
* **Missing Automated Validation Tooling (Lines 360–412):** Process steps are text-based without providing actionable Node/Python validation commands.

---

## 🔧 Refactoring Plan to Reach 10/10
1. Compress double-spaced 555-line wall-of-text into a tight, efficient file under 120 lines.
2. Add explicit `when NOT to use` triggers to YAML frontmatter.
3. Replace generic checklists with actionable Node/Python CLI commands for schema validation.

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: structured-data-validator
description: Validates and fixes JSON-LD and Schema.org structured data across HTML, PHP, JS, and TS files. Use when auditing or fixing rich snippets, microdata, or JSON-LD markup. Do NOT use for standard REST API JSON schemas, relational database migrations, or general code formatting.
tools: [Read, Grep, Glob, Bash, Write]
---

# Structured Data & JSON-LD Validator

Ensures all structured data (JSON-LD / Schema.org) is valid, syntactically correct, and compliant with Google Rich Results requirements.

---

## Operational Constraints

* ❌ **DO NOT** output relative URLs in `@id` or `url` fields (must be absolute HTTPS URLs).
* ❌ **DO NOT** allow HTML tags or unescaped quotes inside JSON-LD blocks.
* ❌ **DO NOT** generate trailing commas or duplicate `@type` root nodes.

---

## Step 1 — Locate All Structured Data

Search repository for schema blocks:
```bash
grep -rn "application/ld+json" --include="*.{html,php,twig,js,ts,tsx}" .
```

---

## Step 2 — Common Vulnerabilities to Audit

| Error Category | Check | Corrective Action |
|---|---|---|
| **Syntax Errors** | Trailing commas, unquoted keys, single quotes | Format with strict JSON parser |
| **URL Format** | Relative paths (`/blog/post`) | Convert to absolute (`https://domain.com/blog/post`) |
| **Dates** | Non-standard dates (`2026/07/30`) | Convert to ISO-8601 (`2026-07-30T00:00:00Z`) |
| **Duplicates** | Multiple identical `@id` strings | Ensure unique entity URIs |
| **Escaping** | PHP `echo` output unescaped quotes | Use `json_encode()` instead of string interpolation |

---

## Step 3 — Validation Command

Validate extracted JSON-LD blocks using inline Python:

```python
import json, glob, re

for filepath in glob.glob("**/*.html", recursive=True):
    content = open(filepath, 'r', encoding='utf-8').read()
    matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    for idx, block in enumerate(matches):
        try:
            data = json.loads(block)
            assert "@context" in data and "@type" in data
            print(f"✅ {filepath} [Block {idx+1}]: Valid JSON-LD ({data.get('@type')})")
        except Exception as e:
            print(f"❌ {filepath} [Block {idx+1}]: INVALID - {e}")
```

---

## Step 4 — Verification Checklist

- [ ] Valid JSON syntax (no parser errors).
- [ ] Required Schema.org properties present.
- [ ] Absolute URLs for all image and canonical references.
- [ ] Google Rich Results test passes without critical errors.
```
