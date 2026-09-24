---
name: github-casestudy-factory
description: Orchestrates multiple subagents to ingest high-level GitHub projects, extract their knowledge into Obsidian, build live portfolio projects, and generate AEO/SEO/GEO-optimized case studies.
---

# GitHub Portfolio Case Study Factory

## Core Execution Rules
1. **Multi-Agent Orchestration**: This skill REQUIRES spawning specialized subagents for distinct phases. Do not attempt to execute all phases synchronously in one prompt.
2. **Phase 1: Knowledge Extraction (The Graph)**
   - Clone the target GitHub repository.
   - Run the `codebase-graph-skill` to map the repository's architecture, dependencies, and logic directly into the Obsidian Knowledge Vault (`04_Knowledge`).
3. **Phase 2: Live Project Engineering**
   - Strictly separate **Creative Direction** from **Engineering**.
   - Wait for explicit user approval on Creative Direction (the "feel" and strategy) before writing code.
   - Build a live, premium version of the project suitable for the portfolio.
4. **Phase 3: Authority Generation (SEO/GEO/AEO)**
   - Generate a deeply technical case study detailing the architecture, challenges, and implementation.
   - Optimize content for Answer Engine Optimization (AEO) and Generative Engine Optimization (GEO) based purely on facts extracted from the Knowledge Graph.
   - Inject structured data (Schema.org) and semantic HTML to rank high in AI search engines and Google.

## Workflow Protocol
1. Receive target GitHub repository URL from the user.
2. Spawn an agent to clone the repo and extract knowledge using `codebase-graph-skill`.
3. Halt and present the Creative Direction / Architecture Plan to the user.
4. Upon approval, spawn an engineering agent to build the live project.
5. Spawn a marketing agent to write the AEO/SEO-optimized case study and store it in the knowledge graph.

## ❌ Constraints
- ❌ Do NOT combine Engineering and Creative Direction phases.
- ❌ Do NOT generate vague marketing fluff for case studies. Stick to hard technical facts and data extracted from the Graph.
- ❌ Do NOT skip generating the Obsidian Graph for the target repository.

## Verification & Grounding Loop
- [ ] Obsidian graph generated for the target repo?
- [ ] Creative Direction explicitly approved by user?
- [ ] Case study contains technical facts, semantic HTML, and AEO-optimized schema markup?
