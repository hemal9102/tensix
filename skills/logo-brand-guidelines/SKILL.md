---
name: logo-brand-guidelines
description: Enforces logo and brand identity standards across web UI, marketing assets, and co-branding. Covers logo variants (primary, secondary, inverse, mono), clearspace padding, size boundaries, WCAG contrast, file formats (SVG/PNG), and co-branding layout rules. Use when designing, reviewing, or implementing UI components that display brand logos. Do NOT use for general typography, CSS styling outside logos, or non-brand graphic design.
---

# Logo & Brand Identity Implementation Guidelines

Enforce strict brand asset usage, clearspace, scaling, color contrast, and co-branding standards in code and UI assets.

---

## 1. Logo Selection & Variant Matrix

| Variant | Target Context | Rule |
| :--- | :--- | :--- |
| **Primary** | Main web header, desktop navigation | Default brand identity mark. |
| **Secondary / Icon** | Mobile nav, favicons, app icons | Compact mark for restricted dimensions. |
| **Inverse (Light)** | Dark backgrounds, hero overlays | High contrast on dark surfaces. |
| **Monochrome** | Print, embroidery, single-color UI | Pure black/white vector renderings. |

* **Constraint**: Never stretch, recolor, or retype logotypes manually. Always use official vector source files.

---

## 2. Clearspace & Sizing Standards

* **Clearspace Protected Zone**: Maintain minimum padding equal to 1x the height of the primary mark's capital letter (or brand token) around all 4 sides.
* **Aspect Ratio**: Always preserve aspect ratio. Scale using width only (`width="160"` in HTML/CSS).
* **Size Thresholds**: Digital minimum = 80px width (favicons = 16x16 icon mark); maximum size enforced per container.

```css
/* CSS Clearspace Wrapper Pattern */
.logo-container {
  display: inline-flex;
  align-items: center;
  padding: var(--brand-logo-clearspace, 1rem);
}
```

---

## 3. Background Contrast & Formats

* **Contrast Compliance**: Ensure ≥ 4.5:1 WCAG AA contrast ratio against background surfaces.
* **Background Mapping**:
  * Light Background $\rightarrow$ Primary Color Logo
  * Dark Background $\rightarrow$ Inverse / Light Logo
  * Brand Accent Surface $\rightarrow$ Monochrome White Logo
* **Web File Format**: Prefer **SVG** for all web rendering. Use transparent **PNG** only when SVG is unsupported.

---

## 4. Co-Branding Layout Protocol

When displaying partner logos (e.g. payment processors, integrations):
1. **Equal Visual Weight**: Balance scale so neither logo dominates.
2. **Clearspace Separation**: Insert visual divider (`<span className="w-px h-6 bg-border" />`) or 2x clearspace gap.
3. **Primary Positioning**: Host brand logo placed first (left/top in LTR layout).

---

## 5. Critical Execution Rules

* ❌ **Don't distort geometry**: Never modify aspect ratio, rotate, or skew logos.
* ❌ **Don't apply UI effects**: Never add CSS drop-shadows, gradients, filters, or unauthorized animations.
* ❌ **Don't place on busy backgrounds**: Never place colored logos directly over complex imagery without a protective semi-transparent backdrop.

---

## Verification & Grounding Loop

Before merging or delivering any logo component:
1. **Asset Integrity Check**: Verify format is SVG with valid `alt` text (e.g. `alt="Company Name"`).
2. **Aspect Ratio Check**: Confirm no explicit height/width mismatches causing distortion.
3. **Contrast Audit**: Verify WCAG AA 4.5:1 contrast against container background color.
