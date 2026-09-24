---
name: slides
description: Creates strategic HTML presentations and pitch decks with interactive Chart.js visualizations, responsive layouts, and structured copywriting frameworks. Use when building presentation decks or interactive web slides. Do NOT use for static document exports or general UI components.
---

# Strategic HTML Presentation System

Systematic framework for constructing responsive, data-driven HTML presentation decks and pitch materials.

## Core Capabilities
- Pure HTML/CSS slide architecture with CSS grid/flex layout patterns.
- Data visualization integration using Chart.js.
- Slide copywriting structuring based on proven persuasion formulas (PAS, AIDA).

---

## Creation Workflow & Execution Rules

### 1. Slide Deck Structure
- Enforce 16:9 widescreen slide container aspect ratio (`width: 100vw; height: 56.25vw` or fixed aspect ratio container).
- Maintain distinct slide section components (`<section class="slide">`).
- Limit to one core concept and max 40 words per slide body area.

### 2. Chart Integration Rules
- Initialize Chart.js canvases within container wrappers to maintain responsiveness.
- Use primary and accent brand colors for data series visualization.

### 3. Rules of Engagement

#### ✅ Do
- Use semantic markup (`<section>`, `<h1>`, `<canvas>`).
- Enforce high text contrast ratios (≥4.5:1) for slide presentation displays.
- Include smooth keyboard navigation hooks (`ArrowRight`, `ArrowLeft`).

#### ❌ Don't
- Do NOT overload slides with dense paragraphs of un-formatted text.
- Do NOT hardcode canvas pixel widths; use relative container percentages.
- Do NOT embed external heavy presentation frameworks when lightweight HTML/CSS suffices.

---

## Verification & Grounding Loop

1. **HTML Validity Check**: Validate that generated HTML slides contain no unclosed tags or syntax errors.
2. **Chart Rendering Verification**: Verify Chart.js canvas elements possess unique DOM IDs and matching initialization scripts:
   ```bash
   python -c "import re; html=open('presentation.html').read(); ids=re.findall(r'id=\"(chart-\d+)\"', html); assert len(ids) == len(set(ids))"
   ```
