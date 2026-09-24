---
name: banner-design
description: Design multi-format marketing and creative banners (social cover, display ads, web hero, print). Use when generating banner graphics, ad layouts, or website headers across various visual styles. Do NOT use for video editing, full site UI engineering, or print production workflows.
---

# Multi-Format Creative Banner Design

Systematic methodology for designing, generating visual assets for, and composing multi-format marketing banners.

## Core Capabilities
- Standard sizing across platforms (Facebook, Twitter/X, LinkedIn, YouTube, Instagram, Google Ads, Web Hero).
- Responsive composition, typography hierarchy, safe zone enforcement, and single CTA placement.
- Automated export formatting via HTML/CSS layout rendering.

---

## Workflow & Execution Rules

### 1. Requirements & Art Direction
- Confirm target platform, exact dimensions, core copy (headline/subtext/CTA), brand color scheme, and aesthetic style.
- Enforce safe zones (keep primary copy and logo within central 75% region).

### 2. Platform Size Specifications

| Platform | Type | Size (px) | Aspect Ratio |
| :--- | :--- | :--- | :--- |
| **Twitter/X** | Header | 1500 × 500 | 3:1 |
| **LinkedIn** | Personal Header | 1584 × 396 | 4:1 |
| **YouTube** | Channel Art | 2560 × 1440 | 16:9 |
| **Instagram** | Square Post / Story | 1080×1080 / 1080×1920 | 1:1 / 9:16 |
| **Google Ads** | Med Rec / Leaderboard | 300×250 / 728×90 | 6:5 / 8:1 |
| **Web** | Hero Section | 1920 × 600 | 16:5 |

### 3. Rules of Engagement

#### ✅ Do
- Maintain contrast ratio ≥ 4.5:1 for text against visual backgrounds.
- Limit typography to maximum 2 font families per banner design.
- Keep copy length concise (<20% canvas area for social ad compliance).

#### ❌ Don't
- Do NOT place crucial text or logos near image boundaries subject to mobile cropping.
- Do NOT include multiple competing calls-to-action (CTAs).
- Do NOT embed low-resolution visual assets (<200 DPI equivalent).

---

## Output Standards & File Naming
- Save HTML layouts and image outputs in `assets/banners/<campaign_name>/`.
- Standard filename format: `<campaign>-<style>-<width>x<height>.png` (e.g., `promo-minimalist-1500x500.png`).

---

## Verification & Grounding Loop

1. **Contrast & Safe Zone Audit**: Inspect generated HTML/CSS layout visually or via headless screenshot to ensure readability.
2. **Dimension Verification**: Confirm exported PNG pixel dimensions match platform requirements exactly:
   ```bash
   python -c "from PIL import Image; img=Image.open('assets/banners/campaign/output.png'); assert img.size == (1500, 500)"
   ```
