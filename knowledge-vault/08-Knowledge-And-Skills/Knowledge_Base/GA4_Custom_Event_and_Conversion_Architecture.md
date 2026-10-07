# Google Analytics 4 (GA4) Custom Event & Conversion Tracking Architecture

**Base Measurement ID:** `G-RJMCZXJ18Y`  
**Deployment Scope:** 35 Static HTML Pages (`hemalshah.vercel.app`)  
**Implementation Engine:** [`script.js`](../../script.js) via `initGA4Tracking` & `trackGA4Event`

---

## 1. Tracked Events & Conversion Schemas

### A. Lead Generation & Form Conversions
| Event Name | Trigger | Payload Parameters | GA4 Conversion Purpose |
|---|---|---|---|
| `generate_lead` | Contact Form Successful Submit (`#contact-form`) | `event_category: 'Contact'`, `event_label: subject`, `project_type: type` | Core Primary Conversion for Client Acquisition |
| `contact_form_submit` | Form Submit Action | `event_category: 'Form'`, `project_type: type` | Form Engagement Metric |
| `contact_email_click` | Clicks on `mailto:` links | `event_category: 'Lead'`, `email_address: email` | Direct Outreach Tracking |

### B. CTA & Navigation Conversions
| Event Name | Trigger | Payload Parameters | Purpose |
|---|---|---|---|
| `cta_click` | Click on `.cta-button`, `.cta-hero-btn`, `.nav-cta`, `.hero-grid-btn` | `event_category: 'Engagement'`, `cta_text: text`, `cta_target: href`, `page_location: path` | Tracks high-intent button interaction across all landing pages |

### C. Outbound Authority & Social Visits
| Event Name | Trigger | Payload Parameters | Purpose |
|---|---|---|---|
| `outbound_click` | Clicks on external links (`github.com/hemal9102`, LinkedIn, Twitter, etc.) | `event_category: 'Outbound Link'`, `link_domain: domain`, `link_url: url`, `link_text: text` | Tracks traffic referral to open-source repos & profiles |

### D. Scroll Depth & Content Engagement
| Event Name | Milestones | Payload Parameters | Purpose |
|---|---|---|---|
| `scroll_depth` | 50%, 75%, 90% scroll on technical blogs and case studies | `event_category: 'Content Engagement'`, `percent_scrolled: threshold`, `page_path: path` | Measures deep technical reader engagement |

---

## 2. Technical Implementation Pattern

```javascript
function trackGA4Event(eventName, params = {}) {
  try {
    if (typeof window.gtag === 'function') {
      window.gtag('event', eventName, params);
    }
  } catch (err) {
    console.debug('[GA4] Event dispatch ignored:', err);
  }
}
```
- **Zero-Dependency:** Uses native `window.gtag` API safely without slowing down Core Web Vitals.
- **Passive Listeners:** Scroll and pointer listeners run passively with no thread-blocking.
