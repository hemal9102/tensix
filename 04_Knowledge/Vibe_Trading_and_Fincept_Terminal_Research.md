# Research: Vibe Trading & Fincept Terminal (AI Financial Intelligence)

---

## 1. What is "Vibe Trading"?

**Concept:**  
"Vibe Trading" is an emerging paradigm adapted from Andrej Karpathy's **"Vibe Coding"** philosophy. Instead of manually writing quantitative algorithms in Python, C++, or Pine Script, traders use **Natural Language prompting + Multi-Agent AI systems** to conceptualize, backtest, and automate trading strategies.

### Core Mechanics
* **Natural Language Strategy Generation:** Traders instruct LLMs (e.g., *"Build a mean-reversion strategy on BTC/USDT when RSI < 28 on 4H timeframe with trailing stop-loss of 1.8%"*).
* **Multi-Agent Execution Swarms:** Frameworks like HKUDS's repository deploy an AI "Investment Committee Swarm":
  * **Macro Analyst Agent:** Macroeconomic trend & interest rate analysis.
  * **Quant/Strategy Agent:** Algorithmic backtesting across equities, crypto, forex, futures, and options.
  * **Risk Controller Agent:** Drawdown limits, position sizing, and volatility checks.
  * **Catalyst & News Agent:** Earnings, regulatory, and event-driven impact analysis.
* **Open Source Engine (`HKUDS/Vibe-Trading`):**
  * Developed by the **University of Hong Kong Data Intelligence Lab (HKUDS)**.
  * PyPI package: `pip install vibe-trading-ai`
  * Features an **Agent Research Harness** with persistent memory, trade-journal diagnostics, session search, and reproducible research artifacts.
  * Official Documentation / Wiki: `vibetrading.wiki`

---

## 2. What is "Fincept Terminal"?

**Concept:**  
**Fincept Terminal** (`fincept.in`) is an open-source, modern **Bloomberg Terminal alternative** built by Fincept Corporation.

### Core Architecture & Capabilities
* **High-Performance Native Desktop Client:** Built with **C++20 and Qt6** for ultra-low latency and smooth rendering (unlike resource-heavy Electron apps).
* **Quant & Analytics Suite:** Integrated with **QuantLib** featuring 18+ quantitative financial modules for derivative pricing, portfolio optimization, and risk modeling.
* **100+ Data Connectors:** Aggregates real-time & historical macroeconomic and market data (FRED, IMF, Yahoo Finance, SEC EDGAR, World Bank).
* **AI Personas & Local LLMs:**
  * Embeds 30+ "AI Investor Personas" (simulating investment philosophies of Warren Buffett, Ray Dalio, Jim Simons).
  * Native integration with local inference engines (Ollama, vLLM) for offline, privacy-first financial research.
* **Licensing:** AGPL-3.0 open-source edition on GitHub with an Enterprise closed-source edition for hedge funds and family offices.

---

## 3. Synergy: How HK Engineering Can Leverage This

1. **AI Quantitative Consulting:** Offering custom AI agent integrations for traders using local Ollama person-models and FastAPI execution wrappers.
2. **Interactive Financial Tools:** Designing terminal-grade dashboards and quantitative SaaS tools using high-performance Python/FastAPI backends.
