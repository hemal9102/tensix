# 🛡️ Skill Quality Audit Report

**Skill Target:** `static-website-security`
**Overall Score:** `8 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Clear positive triggers, but lacks explicit negative triggers ("when NOT to use"). |
| **2. Single Responsibility** | 2/2 | Single domain focus on static site security hardening (SRI, CSP, security headers). |
| **3. Token Efficiency** | 1/2 | 175 lines (exceeds 150-line target) due to hardcoded repo-specific security state. |
| **4. Constraint Enforcement** | 2/2 | Includes detailed matrix, code snippets, trade-offs, and clear configuration rules. |
| **5. Verification Loop** | 2/2 | Strong verification steps via `curl` header inspection and DevTools network checks. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Hardcoded Instance State (Lines 151–175):** Contains "This Repo's Current Security State" with specific hashes (`typed.js@2.0.12`), mixing generic skill instructions with instance data.
* **Line Count Bloat (175 Lines):** Slightly exceeds the 150-line threshold; offloading repo state to workspace files brings it under 140 lines.
* **Missing Negative Triggers (Lines 1–5):** Frontmatter description lacks explicit `when NOT to use` clauses (e.g., dynamic SSR web apps, SQL backend APIs).

---

## 🔧 Refactoring Plan to Reach 10/10
1. Add explicit negative trigger rules in YAML frontmatter.
2. Remove hardcoded repository state to keep the skill 100% generic and portable across projects.
3. Add explicit operational negative constraints (`❌ Don't`) for CSP management.

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: static-website-security
description: Hardens static websites (HTML/CSS/JS on Vercel, Netlify, GitHub Pages) via SRI hashes, HTTP security headers, and CSP policies. Use when auditing or securing static frontends. Do NOT use for dynamic backend applications with SQL databases, server-rendered frameworks (Next.js/Nuxt), or API authorization testing.
tools: [Bash, Read, Edit, Write, Glob, Grep]
---

# Static Website Security Hardening

Use this skill to audit and secure static HTML/CSS/JS websites against CDN supply-chain attacks, missing HTTP security headers, clickjacking, and XSS.

---

## Operational Constraints

* ❌ **DO NOT** apply SQL injection scanners to static sites.
* ❌ **DO NOT** add SRI attributes to dynamic fonts (e.g. Google Fonts CSS).
* ❌ **DO NOT** deploy CSP without testing dynamic fetch endpoints in `connect-src`.

---

## Step 1 — Audit CDN & Form Endpoints

```bash
# Find external CDN assets
grep -rh "cdnjs\|jsdelivr\|unpkg\|googleapis\|cloudflare" --include="*.html" \
  | grep -oE '(src|href)="https://[^"]+"' | sort -u

# Find external API/form endpoints
grep -rn "fetch\|XMLHttpRequest\|formsubmit\|formspree\|emailjs" --include="*.js" --include="*.html"
```

---

## Step 2 — Generate SRI Hashes

Run inline Python to generate base64 SHA-384 hashes for external CDN files:

```python
import urllib.request, hashlib, base64

urls = ["https://cdnjs.cloudflare.com/ajax/libs/typed.js/2.0.12/typed.min.js"]
for url in urls:
    data = urllib.request.urlopen(url, timeout=15).read()
    h = base64.b64encode(hashlib.sha384(data).digest()).decode()
    print(f"sha384-{h}  {url.split('/')[-1]}")
```

Add `integrity="sha384-..."` and `crossorigin="anonymous"` to `<script>` and `<link>` tags.

---

## Step 3 — Header Configuration (`vercel.json`)

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()" },
        { "key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload" },
        { "key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: blob:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self';" }
      ]
    }
  ]
}
```

---

## Step 4 — Verification

Run live header inspection:
```bash
curl -I https://yourdomain.com | grep -iE "content-security|x-frame|x-content|strict-transport|permissions"
```
Check browser DevTools console for SRI or CSP violations.
```
