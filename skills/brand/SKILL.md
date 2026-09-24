---
name: brand
description: Manages brand identity, voice guidelines, visual style guides, and design token synchronization. Use when establishing brand voice, color palettes, typography rules, or syncing brand guidelines to CSS/JSON design tokens. Do NOT use for general UI component styling or non-branded graphic generation.
---

# Brand Strategy & Asset Governance

Framework for establishing brand identity, maintaining voice/visual standards, and synchronizing brand guidelines across code and asset repositories.

## Core Capabilities
- Extract brand context for prompt injection and content generation.
- Audit asset compliance against visual and voice specifications.
- Synchronize `docs/brand-guidelines.md` with JSON and CSS design tokens (`assets/design-tokens.json` / `assets/design-tokens.css`).

---

## Workflow & Execution Rules

### 1. Brand Token Synchronization Workflow
```bash
# 1. Update source of truth in docs/brand-guidelines.md
# 2. Synchronize to design tokens
node scripts/sync-brand-to-tokens.cjs

# 3. Validate context extraction
node scripts/inject-brand-context.cjs --json
```

### 2. Rules of Engagement

#### ✅ Do
- Treat `docs/brand-guidelines.md` as the single authoritative source of truth.
- Run asset validation scripts (`node scripts/validate-asset.cjs <path>`) on all newly generated visual assets.
- Verify color contrast and WCAG compliance during palette updates (`node scripts/extract-colors.cjs --palette`).

#### ❌ Don't
- Do NOT edit `assets/design-tokens.css` directly without updating `docs/brand-guidelines.md`.
- Do NOT use unapproved custom hex codes or off-brand font families in marketing materials.
- Do NOT release assets that fail naming convention or resolution validation.

---

## Script Architecture & Automation
- `scripts/inject-brand-context.cjs`: Exports JSON brand context for prompt engineering.
- `scripts/sync-brand-to-tokens.cjs`: Transpiles brand markdown specs into CSS variables and JSON tokens.
- `scripts/validate-asset.cjs`: Validates file size, format, aspect ratio, and naming syntax.

---

## Verification Loop

1. **Token Verification**: Verify JSON key integrity after running token sync:
   ```bash
   node -e "const t=require('./assets/design-tokens.json'); assert(t.colors && t.typography);"
   ```
2. **Asset Validation Check**: Confirm brand compliance on newly added assets prior to build/deploy.
