---
title: "The 12 Core Pillars of Agentic AI & Multi-Agent Systems (MAS) Vocabulary"
type: "knowledge"
status: "active"
project: "[[browser_mas_saas]]"
tags:
  - knowledge
  - vocabulary
  - mas
  - ai-agents
  - mcp
  - sandboxing
  - guardrails
created: 2026-07-26
updated: 2026-07-26
priority: "high"
owner: "Hemal Shah"
related:
  - "[[Enterprise_Autonomous_Agent_Reference_Architecture]]"
  - "[[Browser_Multi_Agent_Systems_SaaS]]"
  - "[[MCP_Retrieval_Pipeline]]"
---

# The 12 Core Pillars of Agentic AI & Multi-Agent Systems (MAS) Vocabulary

This document serves as the authoritative terminology and conceptual foundation for **HK Engineering** and **PR Marketing Ventures** when architecting autonomous agent workflows, client RAG pipelines, and our **In-Browser MAS Coding SaaS (`[[browser_mas_saas]]`)**.

---

## 1. MCP (Model Context Protocol)
* **Definition**: An open standard enabling AI agents to connect tools, APIs, and data sources through a unified, standardized interface.
* **Real-World Example**: Claude connects to GitHub via an MCP server to read repositories, create branches, and write code autonomously without custom ad-hoc API integrations.

## 2. Agent Loop (Perceive → Plan → Act → Observe)
* **Definition**: The continuous reasoning cycle an AI agent executes—sensing environmental input, forming a multi-step execution plan, taking concrete actions, and observing the feedback/results.
* **Real-World Example**: An agent reads a compiler error log (Perceive), formulates a code fix (Plan), edits the file via terminal (Act), and re-runs `pytest` to verify if tests pass (Observe).

## 3. Tool Use (Agent Capabilities)
* **Definition**: The ability of an AI model to invoke external functions—REST APIs, database connectors, code runners, web browsers—to exert change on the real world.
* **Real-World Example**: An AI assistant calls a live weather API mid-conversation to precisely answer *"Should I fly to NYC tomorrow?"* instead of relying on static training weights.

## 4. Orchestrator (Agent Manager)
* **Definition**: The top-level supervisory agent that analyzes high-level goals, decomposes them into atomic subtasks, and delegates execution to specialized worker subagents.
* **Real-World Example**: A coding orchestrator receives a refactor request and simultaneously dispatches a Test Agent, a Lint Agent, and a Deployment Agent in parallel.

## 5. Subagent (Specialized Worker)
* **Definition**: A focused, highly constrained AI agent that executes one specific task within a larger multi-agent pipeline.
* **Real-World Example**: A "Summarizer" subagent condenses 50 PDF research papers into key bullet points before handing the synthesized data back to the main architectural agent.

## 6. Memory (Short-Term & Long-Term)
* **Definition**: How agents retain, index, and retrieve information—either in-context (temporary session memory) or via external persistent stores (vector databases / Markdown vaults).
* **Real-World Example**: An agent recalls your preferred FastAPI project structure and strict typing rules from a previous session stored in a PostgreSQL `pgvector` database.

## 7. Grounding (Reality Tethering)
* **Definition**: Connecting AI reasoning and text generation directly to verified external data sources to eliminate hallucinations and enforce factual accuracy.
* **Real-World Example**: A financial agent cites real-time stock prices directly from a live Bloomberg API payload rather than guessing numbers from pre-trained weights.

## 8. Guardrails (Safety Layer)
* **Definition**: Strict runtime rules, syntax filters, and operational constraints that prevent agents from executing harmful, unauthorized, or out-of-scope actions.
* **Real-World Example**: An agent is programmatically blocked from executing `DROP DATABASE` or deleting production buckets, even if a user explicitly instructs it to *"clean everything up."*

## 9. Sandboxing (Safe Execution)
* **Definition**: An isolated, ephemeral execution environment where agents can compile code, run terminal scripts, and install packages without risking damage to host servers or production systems.
* **Real-World Example**: Claude Code executes user scripts inside an isolated Docker container or AWS Firecracker micro-VM before proposing a merge request to the actual repository.

## 10. Human-in-the-Loop (HITL — Approval Gate)
* **Definition**: A critical design pattern where autonomous agents pause execution and request explicit human confirmation before executing high-stakes or irreversible actions.
* **Real-World Example**: An agent drafts a sensitive client contract or deployment migration script but waits for a human founder's "Approve / Reject" click before executing.

## 11. Context Window (Working Memory Limit)
* **Definition**: The maximum token capacity (text volume) an AI model can ingest, hold in working memory, and reason over during a single interaction—its effective attention span.
* **Real-World Example**: A 200,000-token context window allows an agent to ingest an entire frontend repository and its AST before writing a single line of refactored code.

## 12. Multi-Agent (Collaborative Intelligence)
* **Definition**: An advanced architectural system where multiple specialized AI agents collaborate, peer-review, and hand-off tasks to solve complex engineering goals faster and more reliably than a single LLM prompt.
* **Real-World Example**: One agent conducts web research, a second agent synthesizes code, and a third agent runs adversarial security tests—all synchronized by a central Orchestrator.

---

## 2. Synthesis Matrix: Mapping Vocabulary to Enterprise Architecture

| Vocabulary Term | Corresponding Layer in Rathi's 14-Layer Architecture | Role in Our In-Browser MAS SaaS (`[[browser_mas_saas]]`) |
| :--- | :--- | :--- |
| **MCP** | Layer 09 (MCP Layer) | WebSockets bridge connecting cloud micro-VMs to browser UI |
| **Agent Loop** | Layer 04 $\leftrightarrow$ Layer 05 (Orchestrator + LLM) | The continuous Perceive-Plan-Act-Observe loop in Python/FastAPI |
| **Tool Use** | Layer 10 (Function Calling / Tool Layer) | Executing terminal commands, git diffs, and n8n webhooks |
| **Orchestrator** | Layer 04 (Orchestrator / Planner) | Central Manager routing tasks to Researcher, Coder, and Tester |
| **Subagent** | Layer 11 (Specialized Agents & A2A) | Isolated worker agents handling single atomic coding jobs |
| **Memory** | Layer 07 (Memory & State) | 3-Tier Obsidian Vault + PostgreSQL `pgvector` HNSW index |
| **Grounding** | Layer 08 (Knowledge / RAG Layer) | Tethering AI responses to live codebase ASTs and docs |
| **Guardrails** | Layer 03 (Gateway) & Layer 06 (Guardrails) | Blocking destructive terminal commands and injection attacks |
| **Sandboxing** | Layer 10 (Execution Environment) | AWS Firecracker / E2B / Daytona ephemeral Linux micro-VMs |
| **HITL** | Layer 12 (Human-in-the-Loop) | One-click "Accept / Reject Diff" button in Monaco Editor UI |
| **Context Window** | Layer 05 (LLM Reasoning Engine) | Managing token budgets via selective file retrieval (grep/view) |
| **Multi-Agent** | Layer 11 (A2A Coordination Layer) | Real-time agent collaboration graph rendered in React Flow |
