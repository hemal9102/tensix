# Global Agent Rules

## Mandatory Skills & Philosophy

### 1. Ponytail Skill (`ponytail`) — Always Active
- **Every coding, refactoring, designing, reviewing, or fixing task must adhere to the `ponytail` skill.**
- Channel a pragmatic senior engineer: choose the simplest, shortest, cleanest, and most minimal solution that actually works.
- Always climb the ladder:
  1. **YAGNI**: Question whether speculative code or features need to exist at all.
  2. **Codebase Reuse**: Reuse existing utilities, helpers, and patterns already in the repository before writing new ones.
  3. **Standard Library First**: Prefer stdlib over external packages.
  4. **Native Platform Features**: Use native platform capabilities (HTML/CSS, native APIs, database constraints) before pulling dependencies.
  5. **No Bloat**: Avoid unnecessary dependencies, boilerplate, or over-engineering.

### 2. TypeSafe Skill (`typesafe-ai` / `typesafe`) — Always Active
- **Every AI-powered workflow, semantic decision, routing, or LLM-driven task must leverage the `typesafe-ai` skill.**
- Treat AI units of intelligence as typed programming primitives rather than arbitrary free-form generation.
- Use System One models (e.g. Jev) for fast, calibrated, typed judgments:
  - **Choice**: Categorization and option selection with probability distributions.
  - **Noul**: Calibrated binary condition probabilities.
  - **Score**: Probability-weighted ranking across ordered dimension levels.
- Keep workflows deterministic in application code; use TypeSafe judgments for programmable common sense and semantic evaluations.
