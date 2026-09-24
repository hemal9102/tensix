---
name: ui-ux-master-skill
description: Governs modern UI/UX design, visual aesthetics, design systems, dark modes, glassmorphism, responsive component layouts, micro-animations, and accessibility (WCAG) compliance. Use when designing web interfaces, styling UI components, establishing visual tokens, or auditing accessibility and visual polish. Do NOT use for backend database queries, API routing, or devops deployment.
---

# Master UI/UX & Visual Design Architect

Establishes premium visual design standards, harmonious color systems, responsive layouts, subtle micro-animations, and WCAG accessibility compliance.

## 🎯 When to Use
* Designing or refactoring web application visual layouts, dashboards, or landing pages.
* Building modern UI component libraries with CSS/Tailwind, custom themes, and glassmorphism.
* Implementing micro-animations, smooth hover states, and dynamic interactive transitions.
* Auditing UI components for color contrast, typography hierarchy, and WCAG 2.1 AA accessibility.

## ❌ When NOT to Use
* Server-side backend API logic or database schema setup (use database or backend skills).
* Performance bundle optimization or server-side rendering logic (use production web engineer skill).

---

## 🚫 Non-Negotiable UI/UX Constraints
* **NEVER** use default browser plain red/blue/green colors. Always use curated, harmonious HSL/Hex design tokens.
* **NEVER** use generic browser default fonts. Always import modern Google Fonts (e.g., Inter, Outfit, Roboto).
* **NEVER** create static, lifeless interfaces. Integrate smooth hover states, active indicators, and micro-transitions (`transition: all 0.2s ease`).
* **NEVER** violate WCAG AA accessibility standards. Enforce a minimum 4.5:1 text-to-background contrast ratio and focus outlines.
* **NEVER** use generic placeholder images without generating high-quality visual assets or using curated media.

---

## 🎨 Design System & Visual Tokens

| Design Element | Token Standard | Best Practice |
| :--- | :--- | :--- |
| **Color Palette** | Dark Mode: `#0f172a`, `#1e293b`<br/>Accents: `#6366f1`, `#10b981` | Use CSS Variables (`--primary`, `--background`, `--accent`) |
| **Typography** | Body: `Inter`, Heading: `Outfit`<br/>Base: 16px, Scale: 1.25 (Major Third) | Enforce line-heights (1.5 for body, 1.2 for headings) |
| **Glassmorphism** | `background: rgba(255,255,255,0.05)`<br/>`backdrop-filter: blur(12px)` | Pair with subtle `1px solid rgba(255,255,255,0.1)` border |
| **Elevation & Shadow** | Smooth multi-layered drop shadows | `box-shadow: 0 4px 20px -2px rgba(0,0,0,0.25)` |
| **Grid & Spacing** | 8pt Spatial System (8px, 16px, 24px, 32px, 48px) | Maintain consistent padding across all container blocks |

---

## ♿ Accessibility & Micro-Interaction Rules

1. **Semantic HTML5:** Use `<main>`, `<nav>`, `<header>`, `<footer>`, `<section>`, and `<article>`.
2. **Keyboard Navigation & ARIA:** Provide clear `:focus-visible` outlines and explicit `aria-label`, `aria-expanded`, and `role` attributes on interactive elements.
3. **Interactive Micro-Animations:**
   ```css
   .button-primary {
     transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s ease;
   }
   .button-primary:hover {
     transform: translateY(-2px);
     box-shadow: 0 8px 25px -5px rgba(99, 102, 241, 0.4);
   }
   ```

---

## ⚡ Grounding & Verification Protocol

Before declaring UI/UX completion:
1. **Accessibility Check:** Run lighthouse accessibility audit (`npx axe-cli <url>`) to verify zero contrast or missing label errors.
2. **Responsive Verification:** Test layout behavior across mobile (375px), tablet (768px), and desktop (1440px) breakpoints.
3. **Visual Polish Pass:** Ensure all interactive components feature active, hover, focus, and disabled visual states.
