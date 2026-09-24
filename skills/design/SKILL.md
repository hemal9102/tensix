---
name: design
description: Comprehensive master design entry point for logos, corporate identity programs (CIP), banners, icons, and pitch decks. Use when routing general graphic design, branding packages, or visual layout tasks. Do NOT use when pure code implementation or specific sub-skills (brand, design-system, ui-styling) are explicitly requested.
---

# Unified Design & Creative Asset System

Central router and orchestrator for brand identity, logos, corporate identity programs (CIP), presentations, and marketing visual assets.

## Core Domain Routing

| Task | Skill / Subsystem | Primary References / Scripts |
| :--- | :--- | :--- |
| **Brand Identity & Voice** | `brand` | `docs/brand-guidelines.md` |
| **Design Tokens & Specs** | `design-system` | `assets/design-tokens.json` |
| **UI Components & Code** | `ui-styling` | Tailwind CSS / Component libraries |
| **Logo Design & AI Generation** | Built-in (Logo) | `scripts/logo/generate.py` |
| **CIP Mockups & Deliverables** | Built-in (CIP) | `scripts/cip/generate.py` |
| **Banner Design** | `banner-design` | Sizing specs & layout rules |
| **SVG Icon Generation** | Built-in (Icon) | `scripts/icon/generate.py` |
| **HTML Pitch Decks** | Built-in (Slides) | Strategic slide templates |

---

## Operational Workflows

### 1. Logo Generation Pipeline
```bash
# 1. Search style and color palette options
python scripts/logo/search.py "minimalist clean" --domain style

# 2. Generate logo (white background enforced)
python scripts/logo/generate.py --brand "BrandName" --style minimalist --industry tech
```

### 2. Corporate Identity Program (CIP) Pipeline
```bash
# Generate complete CIP deliverable set with logo
python scripts/cip/generate.py --brand "BrandName" --logo /path/to/logo.png --industry consulting --set
```

---

## Workflow Rules & Guidelines

#### ✅ Do
- Delegate specialized tasks to specific sub-skills (`brand`, `design-system`, `ui-styling`, `banner-design`).
- Enforce white background on raw logo generation outputs.
- Verify asset file resolution and aspect ratios before output delivery.

#### ❌ Don't
- Do NOT perform monolithic ad-hoc styling when design tokens exist.
- Do NOT bypass safe zone and grid alignment standards.

---

## Verification & Grounding Loop

1. **Routing Check**: Verify the request maps correctly to built-in modules or external sub-skills.
2. **Execution Check**: Verify script outputs exist in target asset directories before declaring task completion:
   ```bash
   python -c "import os; assert os.path.exists('assets/logo_output.png')"
   ```
