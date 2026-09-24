---
name: lead-generation-pipeline
description: Builds compliant B2B lead lists, conducts technical prospect audits, and generates cold outreach drafts. Use when finding B2B prospects, auditing business web listings, or drafting cold email campaigns. Do NOT use for general consumer (B2C) data, general SEO audits, or sending automated emails.
---

# Technical Lead Generation & Intelligence Pipeline

Execute compliant B2B lead discovery, automated technical prospect audits, and targeted sales outreach generation.

## Core Capabilities
- Public B2B prospect discovery and enrichment (Decision Maker, Business Email, Domain).
- Technical auditing (HTTP status checks, HTML stack detection, mobile/SSL availability).
- Structured CRM table formatting and personalized cold email drafting.

---

## Execution Pipeline

### 1. Discovery & Data Enrichment
Target public business entities only. Extract company name, decision-maker role (e.g., Founder, CTO, Marketing Director), and corporate email address.

### 2. Technical Audit ("Pain Point Discovery")
Verify infrastructure and web presence using standard tools:
- **Server Health Check**: Run `curl -I -L --max-time 10 <url>` to detect HTTP status codes (200 vs 404/500).
- **DOM Inspection**: Inspect page source for modern meta tags, responsive design, SSL certificate validity, and performance bottlenecks.

### 3. CRM Formatting
Format output as a structured Markdown table:
`| Company | Contact | Email | Technical Audit Result | Pitch Angle |`

### 4. Personalised Outreach Writing
- Limit email body length to under 120 words.
- Reference empirical technical audit findings directly in the opening hook.
- Conclude with a low-friction call-to-action (e.g., "Open to seeing the raw log?").

---

## Rules of Engagement

#### ✅ Do
- Target strictly public business (B2B) entities and corporate contact information.
- Ground all technical claims in empirical command outputs (e.g., specific HTTP status codes).

#### ❌ Don't
- Do NOT target personal/consumer data (PII) or non-business email addresses (`@gmail.com`, `@yahoo.com`).
- Do NOT fabricate technical errors or outage claims.
- Do NOT execute automated email dispatch scripts directly without user confirmation.

---

## Verification & Grounding Loop

1. **Empirical Grounding Check**: Verify that every technical flaw cited in a pitch originates from a recorded audit log.
2. **PII & B2B Filter**: Validate that no consumer contacts or non-business emails exist in the final CRM dataset:
   ```bash
   python -c "import re; data=open('crm_leads.csv').read(); assert not re.search(r'@[gmail|yahoo|hotmail]\.com', data)"
   ```
