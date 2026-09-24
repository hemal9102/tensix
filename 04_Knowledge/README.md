---
title: "Domain Knowledge Vault Index"
type: "knowledge"
status: "active"
project: "[[hemalshah_portfolio]]"
tags:
  - knowledge
  - index
  - ai-architecture
  - mcp
  - mas
  - rag
  - seo
  - osint
  - cybersecurity
created: 2026-07-26
updated: 2026-07-26
priority: "high"
owner: "Hemal Shah"
---

# Domain Knowledge Vault Index (`04_Knowledge`)

This directory serves as the intelligence core of our Obsidian-first **Knowledge OS**. It contains deep technical research, architectural reference frameworks, industry vocabulary, and engineering playbooks that govern **HK Engineering** and **PR Marketing Ventures**.

Every file in this directory is formatted with standardized YAML frontmatter and bi-directional Wiki-links (`[[Note_Name]]`) to enable instant semantic retrieval by autonomous AI agents and Model Context Protocol (MCP) servers.

---

## Master Knowledge Matrix

| Note Title | Core Domain | Key Frameworks & Topics | Primary Use Case |
| :--- | :--- | :--- | :--- |
| `[[Enterprise_Autonomous_Agent_Reference_Architecture]]` | **Multi-Agent Systems (MAS)** | 14-Layer Reference Architecture (Prashant Rathi), Interactive Mermaid Workflow, A2A Coordination, HITL Approval Gates, Cross-Cutting Enterprise Controls | Enterprise AI consulting proposals & MAS SaaS blueprint |
| `[[The_12_Core_Pillars_of_Agentic_AI_Vocabulary]]` | **Agentic AI Vocabulary** | MCP, Agent Loop (Perceive-Plan-Act-Observe), Tool Use, Orchestrators, Subagents, Memory, Grounding, Guardrails, Sandboxing, HITL, Context Windows, Multi-Agent Collaboration | Core terminology cheat sheet & technical onboarding |
| `[[The_7_MCP_Patterns_and_Ecosystem_Research]]` | **Model Context Protocol (MCP)** | 7 MCP Patterns (Ujjyaini Mitra), Stateless Session Handling, Hacker News Debates, Stack Overflow Logs, GitHub Sandboxes (E2B/Daytona), Practical AI Podcast Insights | Architecting production MCP servers & cloud gateways |
| `[[Browser_Multi_Agent_Systems_SaaS]]` | **SaaS R&D Architecture** | In-Browser Agentic Coding Studio, WebContainer vs. Cloud Micro-VMs, WebSockets Loop, Next.js React Flow UI, Monaco Editor Diff Acceptance | Primary R&D blueprint for our future SaaS product |
| `[[Enterprise_RAG_Architecture]]` | **Retrieval-Augmented Generation** | FastAPI Async Backend, PostgreSQL `pgvector` HNSW Indexing, Hybrid Keyword/Vector Search, Semantic Chunking, Sub-200ms Latency Optimization | Enterprise RAG backend deployments & case studies |
| `[[GEO_AEO_Semantic_SEO]]` | **AI Search Optimization** | Generative Engine Optimization (GEO), Answer Engine Optimization (AEO), Citation Dominance, JSON-LD NextGen Schemas, AI Share of Voice Tracking | AI SEO growth engineering for PR Marketing Ventures |
| `[[SECURITY_REVIEW]]` | **Application Security** | Safe Static Site Testing Workflow, FormSubmit.co Lockdown, DOM XSS Prevention, Immune SQL Injection Architecture | Portfolio security auditing & vulnerability remediation |
| `[[Wireless_Network_Auditing_and_Aircrack_ng_Workflow]]` | **Wireless Network Auditing** | Aircrack-ng Suite (`airmon-ng` vs `aircrack-ng`), 4-Step Professional Workflow, WPA2 4-Way Handshake vs WPA3 SAE Dragonfly, Hardware Compatibility Testing | Private security research & ethical penetration testing |
| `[[Dual_Engine_Instant_Indexing_Architecture]]` | **Instant Indexing Automation** | IndexNow vs. Google Search Console API, OAuth2 Service Account Setup, Automated Python Pipelines (`submit_indexnow.py`, `submit_gsc_indexing.py`), IAM Propagation | Instant SEO & GEO crawl triggering across 100% of global search engines |
| `[[Open_Source_AI_Stack_and_Agent_Ecosystem_Research]]` | **Self-Hosted AI Infrastructure** | Coolify, Dify, Langflow, Open WebUI, Stirling-PDF, Crawl4AI, browser-use, OpenHands, Local Ollama GPU Inference, Docker Network Isolation | Self-hosting private AI platforms & agent orchestration engines |
| `[[AI_Solopreneur_Viral_Launchpad_and_Free_Alternatives_Plan]]` | **Viral SaaS Marketing & Growth** | Zero-Cost Infrastructure (Cloudflare/Vercel/Supabase), Virality Engine (Nano Bana, Seedance 2.0, PoppyAI), 1-3x Daily Video Batching (Hook-Value-CTA), n8n DM Funnels | Launching self-funded viral SaaS products and solopreneur platforms |
| `[[Candle_Ahmia_Haystack_Responsible_Research]]` | **AI Engines & Threat OSINT** | Candle Rust ML Engine, Haystack RAG Pipeline, Ahmia Tor Dark Web Search API, Responsible OSINT Protocols, Zero-Harm Threat Intelligence Mandate | Building high-speed Rust AI engines and ethical threat research monitors |
| `[[VirtualBox_Kali_Linux_and_Antigravity_CLI_Lab_Setup]]` | **Cybersecurity Lab Setup** | WSL 2 vs. VirtualBox USB Wi-Fi Passthrough (`wlan0`), Solving VM "Powering Up..." Hyper-V Conflicts, Standard Operating Procedure for Antigravity CLI (`agy`) in Kali | Configuring sandboxed hacking labs and AI security assistants |
| `[[Scout_AI_ScoutSuite_OSINT_Ecosystem_Research]]` | **Cloud Auditing & AI Scouts** | 3 Pillars of Scout: Scout AI Agents (agno-agi / OpenClaw), ScoutSuite Multi-Cloud Security Auditing (NCC Group), OSINT Scout & Ghost Scout Red Teaming | Performing automated AWS/GCP security audits and web monitoring |
| `[[Start_Me_OSINT_Dashboards_and_Automated_Tooling]]` | **Reconnaissance Dashboards** | Top Curated Start.me OSINT Hubs (OSINT Inception, Ultimate OSINT Collection, NixIntel), Technical Clarification on "OSINstall", Kali Linux OSINT Metapackage SOP | Streamlining OSINT reconnaissance and threat feed management |
| `[[Reverse_Lookup_OSINT_Methodologies_and_Tools]]` | **Threat Reconnaissance** | 5 Vectors of Reverse Lookup: Reverse IP/DNS (ViewDNS), Reverse SSL/Certificates (Censys/Shodan/crt.sh), Reverse Email/Username (Epieos/Sherlock/MOSINT), Reverse Image | Passive infrastructure mapping and identity verification |
| `[[DigitalPlat_and_Zero_Cost_Domain_Hosting_Ecosystem]]` | **Zero-Cost Domain & Hosting** | DigitalPlat FreeDomain (`.dpdns.org`, `.us.kg`, `.qzz.io`), Developer Subdomains (`js.org`, `eu.org`), Cloudflare Edge DNS & Universal SSL Integration, $0/month Solopreneur Stack | Deploying custom AI web apps and landing pages without domain or hosting fees |

---

## Architectural Guidelines for New Knowledge
When adding new research or reference architectures to `04_Knowledge/`:
1. **Always Prepend YAML Frontmatter**: Ensure `title`, `type`, `status`, `tags`, `priority`, and `owner` fields are populated.
2. **Embed Visual Diagrams**: Use Mermaid code blocks (`mermaid`) to visualize workflows and sequential data flows.
3. **Map to Production Tech Stack**: Always explain how abstract theory maps directly to our core tools (*Python, FastAPI, Next.js, pgvector, n8n, Vercel, E2B/Daytona*).
4. **Link Bi-Directionally**: Reference related projects in `02_Projects/` and operational skills in `03_Skills/` using double brackets (`[[Note_Name]]`).
5. **Zero Hallucination / No Assumptions Rule**: NEVER add assumptions, invented metrics, or unverified claims to knowledge notes. All information must be explicitly provided by Hemal Shah or rigorously sourced via web searches and cross-checked against reliable developer documentation.
6. **Confidentiality of Future R&D & Sensitive Data**: Future R&D blueprints (e.g., **In-Browser MAS Coding SaaS**, **Crypto Airdrop AI Platform**) and private client metrics must remain strictly in local Obsidian Vault folders (`01_Memory/`, `02_Projects/`, `04_Knowledge/`).
7. **Public vs. Private Tier Separation**: NEVER reference, link, or bundle any file from `04_Knowledge/`, `01_Memory/`, or `02_Projects/` into public-facing HTML/JS portfolio web pages (`index.html`, `work.html`, etc.).
