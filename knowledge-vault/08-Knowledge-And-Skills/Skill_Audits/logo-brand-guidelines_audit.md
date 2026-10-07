# 🛡️ Skill Quality Audit Report

**Skill Target:** `logo-brand-guidelines`
**Overall Score:** `7 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 1/2 | Clear trigger conditions for when to use, but lacks negative triggers ("when NOT to use"). |
| **2. Single Responsibility** | 2/2 | Stays strictly focused on logo usage guidelines and brand standards in UI/marketing. |
| **3. Token Efficiency** | 1/2 | At 240 lines, it is within the 150–300 line range. Contains detailed markdown tables and inline code blocks that could be offloaded to `references/`. |
| **4. Constraint Enforcement** | 2/2 | Clear do's/don'ts, explicit negative constraints ("Never use primary logo where secondary is specified"), and CSS/HTML rules. |
| **5. Verification Loop** | 1/2 | Contains a manual checklist before UI merge, but lacks deterministic/script-driven validation mechanisms. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Missing Negative Triggers:** The YAML description and `Purpose` section state when to use the skill, but fail to outline explicit exclusions (e.g., when generating whole design systems, typography hierarchies, or non-visual coding tasks).
* **Verbose Inline Code & Tables:** Detailed Next.js and CSS code snippets (lines 47–55, 170–182, 196–203) bloat the main `SKILL.md` file beyond 150 lines.
* **Manual Verification Only:** Section 10 relies entirely on developer manual checking (`[ ]`) rather than providing automated audit scripts or linter rules to verify image formats, aspect ratios, or SVG usage.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Add Negative Constraints to YAML Description:** Explicitly specify when NOT to use this skill (e.g. general UI styling without brand assets, color palette generation, structural layout).
2. **Move Technical Examples to `references/`:** Extract Next.js/CSS code examples and co-branding layout snippets into `references/code-examples.md`.
3. **Add Automated Verification Step:** Include a script or automated validation step (e.g., a regex/linter script that scans UI source files for invalid image attributes or unapproved logo file formats).

---

## 📦 Recommended 10/10 Refactored Version
```markdown
---
name: logo-brand-guidelines
description: Enforces logo and brand identity standards when designing, reviewing, or implementing UI — covering logo variations, clearspace, sizing, color specs, typography, do's/don'ts, co-branding, and file format rules. Use when embedding brand logos in UI or marketing assets. Do NOT use for general CSS styling, layout structure, or non-logo design system work.
---

# Logo & Brand Identity Guidelines

Enforce brand identity compliance across UI components, marketing materials, and partner integrations.

## 1. Quick Reference: Logo Variants & Selection

| Variant | Mandatory Use Case | Excluded Use Case |
|---|---|---|
| **Primary** | Default brand mark for high-visibility UI | Compact headers, app icons, favicons |
| **Secondary / Mark** | Mobile navbar, app icons, favicons (<80px width) | Hero sections, primary headers |
| **Inverse** | Dark backgrounds / dark theme overlays | Light/white backgrounds |
| **Monochrome** | Single-color print, watermarks, PDF headers | Multi-color digital layouts |

> ❌ **Constraint:** Never stretch, recolor, rotate, or apply CSS drop-shadows/filters to logo assets. Always preserve original aspect ratio using single-dimension width attributes.

---

## 2. Execution Rules & Standards

### Clearspace & Sizing
- **Clearspace:** Protect a minimum padding zone equal to 1× the logo's height metric. Define padding via CSS tokens (`padding: var(--logo-clearspace)`).
- **Minimum Size:** Web minimum 80px width (wordmark) / 16x16px (favicon icon-only). Never render below legibility thresholds.
- **File Format Rules:** 
  - **SVG:** Always prefer for web (`<Image src="/logo.svg" width={160} height={40} priority />`).
  - **PNG:** Use only when vector output is unavailable or unsupported.

### Co-Branding Protocols
- Equal visual weight between primary brand and partner logo.
- Minimum spacing: 1× clearspace unit + vertical divider rule (`|`).
- Our brand logo must appear first (left-to-right / top-to-bottom).

For extended code implementations and framework templates, see `references/code-examples.md`.

---

## 3. Verification & Compliance Audit

Before marking any logo implementation complete, run the verification script or inspect against these checks:

```bash
# Verify no raster images or non-SVG logos are used in UI codebase
grep -rn "<img" src/ --include="*.tsx" | grep -i "logo" | grep -v "\.svg"
```

- [ ] Logo uses SVG format in web UI.
- [ ] Aspect ratio preserved (only `width` or `height` specified explicitly, not conflicting dual dimensions).
- [ ] WCAG AA contrast (≥4.5:1) against host background.
- [ ] Clearspace protected on all 4 sides.
```
