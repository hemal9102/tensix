---
title: "Technical Research: In-Browser Multi-Agent Systems (MAS) Architecture"
type: "knowledge"
status: "active"
project: "[[browser_mas_saas]]"
tags:
  - knowledge
  - architecture
  - mas
  - webcontainers
  - micro-vms
  - websockets
created: 2026-07-26
updated: 2026-07-26
priority: "high"
owner: "Hemal Shah"
---

# Technical Research: In-Browser Multi-Agent Systems (MAS) Architecture

## 1. The Architectural Challenge
To replicate desktop CLI tools (like Claude Code) inside a web browser, the system must execute arbitrary terminal commands, file reads/writes, git operations, and package installations (`npm`, `pip`, `pytest`) securely without compromising server infrastructure or latency.

---

## 2. Sandbox Execution Tiers (Research Evaluation)
When we build this SaaS, we must choose between two primary sandboxing architectures:

### Option A: In-Browser WebContainers (WebAssembly / Node.js in Browser)
- **How it works**: Runs a micro-operating system (Node.js/Linux filesystem) directly inside the user's browser tab using WebAssembly (Wasm) and Service Workers (similar to StackBlitz).
- **Pros**: Zero cloud server compute cost for terminal execution; instant sandbox startup (<1 second); works offline after load.
- **Cons**: Limited to Node.js / web ecosystems; cannot easily run heavy Docker containers or native Linux kernel binaries (e.g., complex Python C-extensions or Postgres servers).

### Option B: Cloud Micro-VM Sandboxes (Firecracker / E2B / Daytona / Modal)
- **How it works**: When a user starts a session, the backend orchestrator spins up an isolated, ephemeral AWS Firecracker micro-VM or Kubernetes pod in <300 milliseconds. The browser connects to this VM via WebSockets/WebRTC.
- **Pros**: Full Linux kernel support; can run Python, Docker, databases, compilers, and heavy multi-agent workloads without browser memory limits.
- **Cons**: Requires cloud compute infrastructure management and careful idle-timeout termination to control AWS/GPU costs.
- **Recommended Strategy**: Use a hybrid approach or start with **Option B (Micro-VMs via E2B / Daytona API)** to support full-stack Python/FastAPI/Next.js repositories out of the box.

---

## 3. Multi-Agent Orchestration Engine (The "Brain")
Instead of a single LLM loop, the SaaS orchestrates a **Multi-Agent System (MAS)** communicating over WebSockets:
1. **Manager / Router Agent**: Analyzes user prompts, breaks down tasks, and assigns subtasks to specialized worker agents.
2. **Researcher / Reader Agent**: Explores the repository file tree, performs grep searches, and reads relevant code ASTs.
3. **Coder Agent**: Proposes file edits, diff patches, and new feature scripts.
4. **Tester / Compiler Agent**: Runs terminal test suites (`npm test`, `pytest`) inside the micro-VM sandbox. If a test fails, it captures the stderr log and loops back to the Coder Agent autonomously.
5. **Reviewer Agent**: Audits code for security vulnerabilities, linting errors, and adherence to `.cursorrules` or `SKILL.md` instructions before presenting the final diff to the user in the browser UI.

---

## 4. Frontend Studio UI (Next.js + React Flow)
- **Live Agent Graph**: A visual canvas (built with React Flow / Mermaid) showing real-time communication between subagents (e.g., *Researcher sending AST to Coder*).
- **Embedded Terminal**: Xterm.js connected via WebSocket to the cloud micro-VM bash shell.
- **Monaco Editor / Diff Viewer**: VS Code's Monaco editor integrated into the browser to display side-by-side code diffs with one-click "Accept/Reject" controls.

---

## 5. Next Steps for Development ("The Cooking Plan")
1. **Prototype Phase**: Build a proof-of-concept (POC) connecting a Next.js frontend (with Xterm.js and Monaco) to an E2B / Daytona cloud sandbox API over WebSockets.
2. **Agent Loop Phase**: Implement a Python/FastAPI backend agent loop (using LangGraph or custom async orchestration) that can read files, execute shell commands in the sandbox, and self-correct on errors.
3. **Beta Launch**: Offer as an invitation-only SaaS through PR Marketing Ventures and HK Engineering.
