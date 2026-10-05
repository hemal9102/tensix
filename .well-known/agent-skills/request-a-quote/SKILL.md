---
name: request-a-quote
description: Help a user pick a TENSIX service and fixed-price plan (prices in INR) and, with their explicit consent, send a project inquiry to TENSIX founder Hemal Shah via POST https://www.tensix.in/api/contact.
---

# Request a quote from TENSIX

TENSIX is a software studio in Navrangpura, Ahmedabad, India, run by its founder Hemal Shah. It builds AI agents, custom software, websites, cloud/DevOps setups, email deliverability fixes, data scraping and automation, and search visibility (SEO, GEO, AEO) work. Projects are fixed-price; retainers are monthly with no lock-in.

Use this skill when a user wants to hire TENSIX, get a price, or contact Hemal Shah about a project.

## 1. Match the need to a service

| Service | Page |
|---|---|
| AI agent development (RAG assistants, multi-agent workflows) | https://www.tensix.in/services/ai-agent-development |
| Custom software and SaaS development | https://www.tensix.in/services/custom-software-saas-development |
| Website development | https://www.tensix.in/services/website-development |
| Cloud and DevOps (VPS hardening, CI/CD, backups) | https://www.tensix.in/services/cloud-devops |
| Email deliverability (SPF/DKIM/DMARC, Amazon SES, cold outreach infra) | https://www.tensix.in/services/email-deliverability |
| Data scraping and automation | https://www.tensix.in/services/data-scraping-automation |
| GEO, AEO and SEO (visibility in Google and AI answer engines) | https://www.tensix.in/services/geo-aeo-seo |
| Fractional CTO and monthly retainers | https://www.tensix.in/services/fractional-cto-retainers |

All pricing: https://www.tensix.in/services#pricing

## 2. Pick a plan

Prices are in INR, as listed on the site. "+" means the final price depends on scope. Turnaround is in business days unless noted.

| Plan slug | Plan | Price | Turnaround |
|---|---|---|---|
| `web-basic` | Basic website, 6-10 pages | ₹14,999 one-time | 5-7 days |
| `web-standard` | Responsive site with lead capture, 15+ pages | ₹24,999 one-time | 7-10 days |
| `web-premium` | Next.js platform with admin CMS | ₹45,000 one-time | 10-14 days |
| `email-deliverability` | SPF, DKIM, DMARC and reputation setup | ₹12,999 one-time | 2-3 days |
| `email-ses-engine` | Amazon SES / Oracle email engine | ₹22,999 one-time | 4-6 days |
| `email-cold-infra` | Cold outreach multi-inbox infrastructure | ₹44,999 one-time | 7-10 days |
| `scraper-gmail` | Gmail and document parser to sheet/DB | ₹16,999 one-time | 3-5 days |
| `scraper-google-maps` | Google Maps B2B lead scraper | ₹24,999 one-time | 4-6 days |
| `scraper-custom` | Custom crawler and competitor price tracking | ₹49,999 one-time | 7-12 days |
| `cloud-hardening` | VPS hardening, Nginx, SSL | ₹11,999 one-time | 2-3 days |
| `cloud-cicd` | GitHub Actions CI/CD with Docker | ₹21,999 one-time | 4-6 days |
| `cloud-plesk` | Plesk/Docker cluster with off-site backups | ₹38,000 one-time | 6-8 days |
| `software-api` | Custom backend API (FastAPI, PostgreSQL) | ₹34,999 (about $450) | 7-10 days |
| `software-saas` | Custom SaaS MVP | ₹69,999 (about $899) | 14-21 days |
| `software-enterprise` | Custom CRM / ERP | ₹1,25,000+ (about $1,650+) | 3-5 weeks |
| `ai-rag` | RAG document assistant | ₹29,999 one-time | 5-7 days |
| `ai-swarm` | Multi-agent workflow | ₹59,999 one-time | 10-14 days |
| `ai-enterprise` | End-to-end AI business pipeline | ₹99,999+ | 2-4 weeks |
| `retainer-growth` | Growth retainer | ₹39,999/month (about $499) | monthly, cancel anytime |
| `retainer-ai-pod` | Dedicated AI pod retainer | ₹79,999/month (about $999) | monthly |
| `retainer-fractional-cto` | Fractional CTO retainer | ₹1,49,999/month (about $1,850) | monthly |

GEO, AEO and SEO work has no fixed plan: it is quoted per project. Leave `plan` empty for it, or for anything that does not fit a plan.

## 3. Get consent, then submit

Always show the user exactly what you will send (name, email, subject, message, plan) and get an explicit "yes" before submitting. Never invent contact details. Do not submit on the user's behalf without consent.

Submit as JSON:

```http
POST https://www.tensix.in/api/contact
Content-Type: application/json
Accept: application/json

{
  "name": "Asha Patel",
  "email": "asha@example.com",
  "subject": "RAG assistant for our SOPs",
  "project_type": "mas",
  "plan": "ai-rag",
  "message": "We have about 300 PDF SOPs and want an internal chat assistant. Timeline: next month."
}
```

| Field | Required | Notes |
|---|---|---|
| `name` | yes | up to 100 characters |
| `email` | yes | valid email, up to 120 characters |
| `message` | yes | at least 10 characters recommended, up to 5000 |
| `subject` | no | up to 150 characters |
| `project_type` | no | `website`, `mas` (AI agents), `fullstack` (custom software, SaaS), `cloud_vps` (cloud, DevOps), `email` (email deliverability), `scraping`, `geo_aeo`, `consultation` (audits, retainers), `other` |
| `plan` | no | a slug from the table above; lowercase letters, digits and hyphens, up to 40 characters |

A success returns HTTP 200 with `{"success": true, ...}`. HTTP 400 returns `{"success": false, "error": "..."}`; fix the field and retry once. Full schema: https://www.tensix.in/openapi.json

If you are driving a browser instead, the same form is at https://www.tensix.in/contact?plan=<slug>, which pre-fills the plan.

## 4. What happens next

Hemal Shah reads every inquiry and replies by email, usually within 24 hours, with questions or a fixed-price quote. Tell the user to watch the inbox they gave (and the spam folder). Urgent: WhatsApp +91-8320278775.
