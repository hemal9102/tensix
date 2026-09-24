---
name: live-web-search-skill
description: Real-time web search integration workflow for retrieving up-to-date documentation, API syntax, package version changes, and error solutions. Use when encountering unhandled runtime errors, API deprecations, new package releases, or real-time web verification tasks. Do NOT use for querying internal project files or searching local codebase history.
---

# Live Web Search & Technical Information Retrieval

Execute optimized web search queries to retrieve official documentation, resolve runtime stack traces, and verify real-time facts.

---

## 4-Step Search Execution Workflow

1. **Query Optimization & Intent Extraction**
   * Strip natural language fluff, conversational words, and generic terms.
   * Combine exact error codes, library versions, and canonical keywords (e.g. `"Next.js 15" "app router" "revalidatePath"` or `"Prisma" "P2025"`).

2. **Execute Search Query**
   * Perform live web search using search API or search tool.
   * Prefer official documentation, GitHub issues, or release notes over generic blog aggregator posts.

3. **Information Extraction & Validation**
   * Extract target syntax, code blocks, API signatures, or official deprecation notices.
   * Verify domain authority and sanity-check code against current workspace environment (e.g. Node version, TS target).

4. **Synthesis & Grounded Application**
   * Integrate retrieved solutions directly into task context.
   * Cite source URLs and official documentation paths when introducing architectural updates.

---

## Execution Rules & Constraints

* ❌ **Don't use verbose natural language queries**: Never query `"How do I fix this error in my nextjs app when I get P2025"`. Use focused tokens: `"Prisma error P2025 record not found"`.
* ❌ **Don't accept unverified blog advice**: Prioritize official documentation domains, framework repositories, and verified release notes.
* ❌ **Don't hallucinate API signatures**: If search results are ambiguous, issue a targeted secondary search rather than guessing syntax.

---

## Verification & Grounding Loop

1. **Source Check**: Confirm retrieved code examples match current project library major versions (e.g., React 19 vs React 18).
2. **Runtime Verification**: Test fetched code pattern locally via syntax check or build command before declaring solution validated.
