---
title: "Research and GEO Map of Content"
type: "moc"
tags:
  - moc
  - research
  - geo
  - rag
  - ai-citation
updated: 2026-10-07
---

# 🔬 Research and Competitive GEO Map of Content (MOC)

> **"Visibility in modern AI answer engines depends not on ranking on a blue-link page, but on being selected, entailed, and cited first (`[1]`)."**

---

## 📚 The 6 Canonical Research Foundations

| Paper | Focus Area | Empirical Finding / Law |
| :--- | :--- | :--- |
| **[[Competitive-GEO-2605.25517\|arXiv:2605.25517]]** | **Competitive GEO** | 252k trials: Explicit pricing/numbers + fresh timestamps are the primary drivers of winning the first citation `[1]`. |
| **[[DeepMind-SAFE-2403.18802\|arXiv:2403.18802]]** | **Long-Form Factuality (SAFE)** | Autonomous evaluators decompose output into atomic claims. Discrete key-value specs maximize precision $F_1$. |
| **[[ALCE-Citations-2305.14627\|arXiv:2305.14627]]** | **Attributed Generation (ALCE)** | LLMs require high NLI entailment ($D \models S$) to prevent stripping or hallucinating citations. |
| **[[Stanford-Verifiability-2304.09848\|arXiv:2304.09848]]** | **Engine Verifiability Audit** | Stanford audited commercial engines (Bing, Perplexity) finding only 51.5% of sentences were supported by citations. |
| **[[Princeton-GEO-2311.09735\|arXiv:2311.09735]]** | **GEO Benchmark** | Structured data, JSON-LD, and authoritative technical summaries increase LLM visibility by up to 40%. |
| **[[RUPBench-Robustness-2406.11020\|arXiv:2406.11020]]** | **Reasoning Under Noise** | LLMs degrade under lexical/syntactic perturbations. Explicit entity disambiguation prevents concept collapse. |

---

## 🛠️ Production Implementation in TENSIX

- **[[DOCS_GEO_RESEARCH_IMPLEMENTATION]]** — Master architectural reference document for all changes applied to `tensix.in`.
- **Top-200 Tokens Citation Grounding (`.geo-citation-grounding`)** — Injected into hero sections of all 8 service pages, `index.html`, and `services.html`.
- **Schema Hardening** — `numberOfEmployees: 1`, `disambiguatingDescription`, `dateModified: "2026-10-07T00:00:00Z"`.
- **Dynamic Schema Validation** — `validate_schemas.py` enforcing 46/46 valid JSON-LD graphs with 0 collisions.
- **Markdown & Agent Twin Generation** — `build_agent_files.py` generating `md/*.md`, `llms.txt`, and `llms-full.txt`.

---

## 📁 Knowledge Base & Comparative Notes

- [[Gap_Analysis_Rajput_vs_Hemal]] — Detailed comparative systems analysis between RB Engineering and TENSIX.
- [[Indexing_Pipeline_Architecture]] — End-to-end multi-engine crawler and indexing workflow.
- [[Community_Hacks_Indexing]] — Advanced discovery protocols across non-Google indexes.
- [[Kagi_Brave_Mojeek_Indexing]] — Independent search engine crawler behavior and parameters.
- [[Privacy_Engines_Indexing]] — Anonymous search engine RAG harvesting mechanisms.

---

## 🔗 Related MOCs
- [[00-MOC/Home|Home Dashboard]]
- [[00-MOC/TENSIX-Master-MOC|TENSIX Master MOC]]
- [[00-MOC/TENSIX-Services-And-Pricing-MOC|Services & Pricing MOC]]
- [[00-MOC/System-Architecture|System Architecture MOC]]
