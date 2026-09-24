# 🛡️ Skill Quality Audit Report

**Skill Target:** `architecture-and-design-skill`
**Overall Score:** `3 / 10`

---

## Score Breakdown

| Pillar | Score | Verdict |
| :--- | :---: | :--- |
| **1. Trigger Precision** | 0/2 | Vague description ("Governs architectural design...") causing magnet skill triggering; lacks explicit negative boundaries. |
| **2. Single Responsibility** | 0/2 | Severe multi-domain scope creep: mixes backend system design, PHP MVC/Hostinger optimization, and Next.js 15 frontend performance. |
| **3. Token Efficiency** | 1/2 | 239 lines long with duplicate prompt instructions pasted from multiple injected engineering prompt templates. |
| **4. Constraint Enforcement** | 1/2 | Contains strict performance budgets and "Never" constraints, but rules conflict across different stack sections (e.g., PHP vs Next.js). |
| **5. Verification Loop** | 1/2 | Mentions `./scripts/architecture-validator.py`, but lacks a structured automated test step in the main execution protocol. |

---

## 🚨 Anti-Patterns & Vulnerabilities Found
* **Prompt Injection & Bloat (Lines 20–238):** Over 80% of the document consists of copy-pasted external prompt dumps ("OMNI-RULES FOR AUTONOMOUS PRODUCTION READINESS" and "PRODUCTION WEB ENGINEER ENHANCEMENTS").
* **Conflicting Stack Directives:** Simultaneously dictates rules for PHP MVC on Hostinger/LiteSpeed (L103) and Next.js 15 / React 19 / Vercel (L116–121).
* **Magnet Skill Anti-Pattern:** Triggers on any request mentioning "architecture", "design", "performance", "Next.js", or "database".
* **Dead / Unchecked External References:** Refers to scripts and reference files without conditional loading or fallback logic.

---

## 🔧 Refactoring Plan to Reach 10/10
1. **Purge Irrelevant Injected Prompts:** Strip out PHP MVC, Lighthouse, Hostinger, and Next.js frontend performance sections. Move web performance rules to a dedicated `web-performance-optimization` skill.
2. **Focus Purely on Architecture:** Scope `SKILL.md` strictly to API design, service-controller layer separation, and DB schema modeling.
3. **Refine Trigger Boundaries:** Add explicit negative triggers in YAML frontmatter (e.g., "Do NOT use for frontend styling or web performance auditing").
4. **Enforce Script Verification:** Require running `architecture-validator.py` as a mandatory blocking step before completing any design task.

---

## 📦 Recommended 10/10 Refactored Version

```markdown
---
name: architecture-and-design-skill
description: Governs backend architectural design, REST API endpoint modeling, database schema definitions (Prisma/PostgreSQL), and layer isolation (Service vs Controller). Use when designing backend systems and schemas. Do NOT use for frontend performance, UI design, Lighthouse audits, or Next.js layout optimization.
tools: [read_file, write_file, run_command]
---

# Architecture & Backend Design Skill

## Core Principles
1. **Layer Isolation**: Service logic must be isolated from API Controllers. No database queries inside route handlers.
2. **Schema Integrity**: All entities must define Prisma schemas and matching Pydantic / TypeScript DTO models.
3. **Dependency Injection**: Services must ingest repositories/adapters via dependency injection.

## Workflow Protocol
1. **Analyze Domain Requirements**: Map entity states, access patterns, and read-to-write ratios.
2. **Inspect Standards**: Read `references/architectural-blueprint.md` and `references/postgres-indexing-rules.md`.
3. **Define Models & Interfaces**: Create entity DTOs and Prisma database schemas.
4. **Validate Architecture**: Run `./scripts/architecture-validator.py` against `assets/architecture-schema.json`.

## Verification Checklist
- [ ] Layer separation maintained (Controller -> Service -> Repository).
- [ ] DTO schemas strictly validate input/output types.
- [ ] Architectural validation script (`architecture-validator.py`) passes with exit code 0.
```
