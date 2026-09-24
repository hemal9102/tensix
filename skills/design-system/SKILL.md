---
name: design-system
description: Master rules and tokens for design systems, color palettes, typography, spacing, shadows, and component specifications. Use when constructing UI systems, establishing CSS variables, or building reusable component styles. Do NOT use for high-level brand strategy or raw logo generation.
---

# Design System Specification & Token System

Architectural specification for UI design systems, token structures, component classes, and accessibility rules.

## Core Design Tokens

### Color Palette

| Role | Hex | CSS Variable | Usage |
| :--- | :--- | :--- | :--- |
| **Primary** | `#4338CA` | `--color-primary` | Main interactive elements, primary buttons |
| **On Primary** | `#FFFFFF` | `--color-on-primary` | Text on primary elements |
| **Secondary** | `#6366F1` | `--color-secondary` | Secondary buttons, highlights |
| **Accent / CTA** | `#10B981` | `--color-accent` | Conversion points, success states |
| **Background** | `#FFFFFF` | `--color-background` | Default page background |
| **Foreground** | `#0F172A` | `--color-foreground` | Primary typography color |
| **Muted** | `#F1F5F9` | `--color-muted` | Card backgrounds, table headers |
| **Border** | `#E2E8F0` | `--color-border` | Subtle dividers and outlines |
| **Destructive** | `#DC2626` | `--color-destructive` | Error states, delete actions |

### Typography Standards
- **Headings**: Lexend (Weights: 500, 600, 700)
- **Body Text**: Source Sans 3 (Weights: 400, 500)
- **Font Stack Import**:
  ```css
  @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@500;600;700&family=Source+Sans+3:wght@400;500&display=swap');
  ```

---

## Component Specifications

### Buttons
```css
.btn-primary {
  background-color: var(--color-primary);
  color: var(--color-on-primary);
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: background-color 200ms ease, transform 150ms ease;
  cursor: pointer;
}
.btn-primary:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}
```

### Cards
```css
.card {
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: box-shadow 200ms ease;
}
```

---

## Rules of Engagement

#### ✅ Do
- Enforce `cursor: pointer` on all clickable components.
- Maintain minimum contrast ratio of 4.5:1 for body copy against backgrounds.
- Use SVG icons (Lucide, Heroicons); avoid emoji icons in production interfaces.

#### ❌ Don't
- Do NOT hardcode raw hex values in components; reference CSS variables or Tailwind token classes.
- Do NOT introduce un-transitioned layout shifts on hover or focus states.
- Do NOT obscure focus rings for keyboard navigation.

---

## Verification & Compliance Loop

1. **Accessibility Check**: Validate contrast ratios across primary and accent combinations.
2. **Token Audit**: Confirm all UI component classes consume defined CSS variables:
   ```bash
   python -c "import re; css=open('styles.css').read(); assert all(v in css for v in ['--color-primary', '--color-background'])"
   ```
