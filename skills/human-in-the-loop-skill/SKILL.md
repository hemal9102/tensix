---
name: human-in-the-loop-skill
description: Standardized framework for intercepting high-risk execution phases, unresolvable errors, or ambiguous decisions to prompt human developers with structured choices. Use when an automated task encounters high-risk operations (e.g. destructive DB migrations, breaking API changes), or when automated recovery loops fail after 3 consecutive attempts. Do NOT use for standard low-risk automated execution or non-blocking tasks.
---

# Human-in-the-Loop (HITL) Execution Protocol

Intercept high-risk actions or stalled auto-recovery loops by bundling context and providing structured, actionable decision options to the human developer.

---

## Trigger Conditions

Activate this protocol **ONLY** when:
1. **High Risk Threshold**: Destructive filesystem/database operations, production deployment, or security-sensitive configuration changes.
2. **Loop Exhaustion**: Automated error recovery or self-correction loop fails to converge after **3 consecutive attempts**.
3. **Requirement Ambiguity**: Architectural choices with multiple conflicting trade-offs requiring product/design decisions.

---

## 5-Step HITL Execution Workflow

1. **Pause & State Freeze**
   * Stop mutating files, schemas, or remote environments immediately.
   * Preserve current execution context and draft state.

2. **Context & Telemetry Assembly**
   * Gather exact command outputs, error traces, diffs, and affected resources.
   * Identify root cause or decision fork cleanly.

3. **Formulate Structured Decision Options**
   * Prepare 2–4 concrete, distinct options labeled clearly (e.g., Option A, Option B, Option C).
   * For each option, document:
     * **Description**: Technical summary of action.
     * **Pros / Cons**: Impact, risk, trade-offs.
     * **Next Steps**: Exact downstream execution path.

4. **Present Prompt to Human Developer**
   * Output a clean, scannable summary box containing context, root issue, and decision matrix.
   * Avoid vague questions like *"What should I do now?"*.

5. **Ingest Choice & Execute**
   * Validate human response against available options.
   * Proceed down the selected technical pathway and record the decision.

---

## Decision Matrix Template

```markdown
### ⚠️ Human Decision Required

**Context / Trigger:** [Brief description of high-risk operation or 3x failure]
**Current State:** [Affected files/components & current branch]

#### Options:
- **Option A (Recommended):** [Action summary]
  - *Impact:* [Low/Med/High]
  - *Trade-off:* [Pros/Cons]
- **Option B:** [Alternative action summary]
  - *Impact:* [Low/Med/High]
  - *Trade-off:* [Pros/Cons]
- **Option C (Abort):** Rollback changes to previous working state.

**Reply with your choice (A, B, or C) or provide custom guidance.**
```

---

## Execution Rules & Constraints

* ❌ **Don't ask vague questions**: Never prompt without structured options and recommendations.
* ❌ **Don't mutate state while waiting**: Keep state clean and safe until input is received.
* ❌ **Don't bypass human approval**: Never execute high-risk destructive commands after a failed verification attempt without prompting.

---

## Verification & Grounding Loop

1. **Pre-prompt Check**: Verify that all logs and context snippets are complete before rendering the prompt.
2. **Post-response Check**: After receiving human selection, echo the chosen pathway and run pre-execution safety check command before applying changes.
