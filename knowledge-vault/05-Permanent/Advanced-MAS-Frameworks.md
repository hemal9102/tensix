---
title: Advanced MAS Frameworks
tags: [ai, frameworks, mas]
updated: 2026-08-01
---

# Advanced MAS Frameworks

**Purpose:** To list the production-grade frameworks used to build Multi-Agent Systems.

**Summary:** Moving past linear chat prompts requires orchestration frameworks that handle message routing, cyclic graphs, and tool execution between multiple autonomous agents.

## Key Frameworks
1. **Microsoft AutoGen:** The industry standard for multi-agent conversations. It allows developers to define agents, route messages between them, and safely execute Python code in local or Docker environments.
2. **LangGraph (by LangChain):** Built for creating cyclic graphs. Instead of a linear prompt, the AI loops through a state machine (e.g., Plan -> Write Code -> Test -> If Fail, loop back to Plan). Essential for self-correcting agents.
3. **CrewAI:** Focuses on role-based agent design. It allows you to assign specific tools to specific roles, ensuring that a "Backend Agent" doesn't try to execute "Frontend Tools," mirroring real-world team structures.

## Related
- [[Advanced-MAS-And-Agentic-Research-MOC]]
- [[Self-Healing-AEO-GEO-Infra-MOC]]
