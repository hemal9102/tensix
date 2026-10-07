# Core Web Vitals (CWV) & Lighthouse 100/100 Optimization Method

**Date:** 2026-08-03
**Context:** JobRecruitment.in Production Optimization

This document outlines the exact methodology used to take a PHP/Apache stack with Tailwind CSS from a failing Lighthouse score to 100/100 by systematically eliminating FCP, LCP, and CLS bottlenecks.

## 1. Eliminate Cumulative Layout Shift (CLS) from Web Fonts
**The Problem:** Using `font-display: swap` for Google Fonts causes the browser to render a system fallback font first, and then swap it out for the custom font. The difference in character widths causes the text layout to expand/collapse dynamically, severely penalizing CLS (e.g., 0.134 shift).
**The Solution:**
- Change `font-display: swap` to `font-display: optional` inside the `@font-face` declarations.
- **Why it works:** `optional` gives a very brief blocking period (100ms). If the font isn't downloaded instantly, the browser sticks to the fallback font and aborts the swap completely, guaranteeing zero layout shift. On the next page load, the font is served instantly from the cache.

## 2. Eliminate CLS from Icon Fonts (Material Symbols)
**The Problem:** Icon fonts load as raw text (e.g., "star star star") and then snap into small icons (16x16) when the font finally renders. This snap shrinks the layout, causing a micro-shift (0.007).
**The Solution:**
- Do not use `font-display: optional` for icons, as it will leave raw text on the screen if the network is slow.
- Instead, wrap the icons in a container with a **hardcoded minimum width** and **centered alignment** (e.g., `<div class="flex items-center min-w-[90px] justify-center">`). 
- **Why it works:** The container reserves the exact spatial footprint the icons will need, so when they finally snap from text to icons, the surrounding layout does not move.

## 3. Fixing "Reduce Unused CSS" (Tailwind Inline Issues)
**The Problem:** Inlining the entire `tailwind.css` into `<style>` inside `index.html` eliminates render-blocking network requests (improving FCP), but it leaves behind dead CSS if not properly purged, triggering Lighthouse's "Reduce Unused CSS" warning.
**The Solution:**
- Always run the Tailwind JIT compiler (`npm run build:css`) to aggressively purge unused classes based on the `tailwind.config.js` content paths.
- Write a deployment script (like Python) that dynamically reads the newly minified `assets/tailwind.css` and injects it over the old inline `<style>` block in `index.html` *before* syncing to the live server. 

## 4. Efficient Cache Lifetimes for Fonts (.htaccess)
**The Problem:** Lighthouse flags fonts served from the local domain with "Use efficient cache lifetimes" because standard caching rules often miss modern font extensions like `.woff2`.
**The Solution:**
Add explicit 1-year cache headers for all font MIME types in Apache's `.htaccess`:
```apache
<IfModule mod_expires.c>
    ExpiresByType font/woff2 "access plus 1 year"
    ExpiresByType font/woff "access plus 1 year"
    ExpiresByType font/ttf "access plus 1 year"
</IfModule>

<FilesMatch "\.(woff2|woff|ttf|eot)$">
    Header set Cache-Control "max-age=31536000, public"
</FilesMatch>
```

## Summary Checklist for Deployment
1. Run `npm run build:css` to generate purged CSS.
2. Run injection script to place `font-display: optional` and inline the purged CSS into HTML files.
3. Push via `rsync`.
4. Flush Cloudflare / LiteSpeed Cache on the live server.
