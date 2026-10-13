# TENSIX Component Modularization Guide

## 1. Overview
To prevent markup drift and eliminate repetitive manual edits across all 48 static pages, TENSIX uses a **build-time static component architecture**.

- **No Runtime JS Overhead**: Zero client-side JavaScript execution or `fetch()` calls.
- **Sub-400ms TTFB Preserved**: Edge servers deliver 100% pre-rendered static HTML directly to Googlebot, Perplexity, and human users.
- **Zero SEO / Schema Corruption**: Page titles, canonical URLs, meta descriptions, and JSON-LD schema graphs remain unique to every page.

---

## 2. Directory Structure

```
D:\projects\tensix\
├── components\
│   ├── _head_common.html    # Shared Google Tag, charsets, viewport, favicons, fonts, CSS
│   ├── _header.html         # Site logo, navigation links with active state placeholders
│   └── _footer.html         # Studio info, address, social links, complete 10 services list
└── build_components.py      # Automated build & synchronization engine
```

---

## 3. Marker Syntax in HTML Files

Every static HTML file contains delimiters designating the shared sections:

### 3.1 `<head>` Common Tags
```html
<head>
<!-- @include head_common -->
<!-- Google tag (gtag.js) -->
...
<link rel="stylesheet" href="/assets/css/tensix.css?v=1.3"/>
<!-- @endinclude -->

<!-- Page-specific SEO & Schema remain unique below -->
<title>Unique Page Title | TENSIX</title>
<meta name="description" content="..."/>
<link rel="canonical" href="..."/>
<script type="application/ld+json">...</script>
</head>
```

### 3.2 Site Header
```html
<!-- @include header -->
<header class="site-header">
...
</header>
<!-- @endinclude -->
```

### 3.3 Site Footer
```html
<!-- @include footer -->
<footer class="site-footer">
...
</footer>
<!-- @endinclude -->
```

---

## 4. How to Update Global Components

When you want to update the header, footer, or global head tags:
1. Edit the relevant file in `components/`:
   - `components/_head_common.html` (e.g., updating CSS version string `?v=1.4`)
   - `components/_header.html` (e.g., adding a new top-level navigation item)
   - `components/_footer.html` (e.g., adding a new service or changing office details)
2. Run the sync command:
   ```bash
   python build_components.py
   ```
3. Run verification:
   ```bash
   python validate_schemas.py
   ```
4. Commit and push:
   ```bash
   python D:\projects\git-sync.py "D:\projects\tensix"
   ```
