---
title: "Safe and Thorough Security Testing Workflow: Portfolio Review"
type: "knowledge"
status: "active"
project: "[[hemalshah_portfolio]]"
tags: ["security", "audit", "knowledge", "portfolio"]
created: 2026-07-26
updated: 2026-07-26
priority: "medium"
owner: "Hemal Shah"
---

# Safe and Thorough Security Testing Workflow: Portfolio Review

Following the **secure-testing-workflow** skill, I have conducted a review of your portfolio website located at `H:\portfolio_website\hemalshah`. 

## 1. Identify the Attack Surface
Since this is primarily a static HTML/JS website, the attack surface is minimal compared to a dynamic backend (Node.js/Django/PHP). The primary interactive elements that accept user input are:
- **Contact Form** (`contact.html`): Accepts `name`, `email`, `subject`, `project_type`, and `message`.
- **Client-side Routing/URL Parameters**: No complex URL parameter parsing was found that would lead to DOM-based XSS.

## 2. Code Review
- **No SQL Injection Risk**: Because this is a static site without a direct database connection or ORM on your end, it is intrinsically immune to SQL injection. 
- **Contact Form Security**: Your form in `contact.html` is handled securely in `script.js` using `fetch` to send a JSON payload to `formsubmit.co`. 
- **Cross-Site Scripting (XSS)**: You are using `textContent` for fallback typewriters and properly isolating DOM manipulations. The only use of `innerHTML` is to restore button state (`btn.innerHTML = originalText`), which is safe because it captures static HTML initially. 
- **Recommendation**: To further lock down the form, ensure `formsubmit.co` has spam protection (like reCAPTCHA or honeypots) enabled to prevent malicious bot submissions.

## 3. Integration Tests & Automated Checks
As a static site, heavy integration tests for API fail-safes are not required. However, you can add automated tests for:
- Checking if form submissions fail gracefully when network requests are blocked.
- Verifying the UI correctly shows the error toast (which you've implemented beautifully with `showToast('Connection error...', 'error')`).

## 4. Static Analysis and Dependency Scans
- You are not relying on heavy npm packages or outdated CDN scripts that would trigger dependency warnings. 
- Your external fonts and icons are correctly preloaded or self-hosted.

## 5. Manual Verification
- Verified that all inputs are collected securely via `JSON.stringify` rather than being concatenated into a URL or executed as raw HTML.
- Verified that your toast notifications correctly handle both success (`data.success === "true"`) and network failures.

**Conclusion:** The codebase is robust from a security standpoint for a static portfolio. By utilizing a third-party form handler (`formsubmit.co`) instead of writing raw backend SQL/email handlers, you've completely avoided the most common vulnerabilities (SQLi, Server-Side Request Forgery).
