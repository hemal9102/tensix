---
name: principal-architect-review
description: >
  Evaluates system architecture, infrastructure design, and distributed systems from a Principal Architect perspective.
  Use when reviewing architectural proposals, system designs, scalability plans, fault tolerance, and capacity planning.
  Do NOT use for syntax checking, basic code reviews, or minor bug fixes.
---

# Principal Architect Review

Provides enterprise-grade system architecture evaluation by identifying scaling bottlenecks, failure modes, and architectural constraints across 7 core pillars.

## Core Architectural Pillars
Evaluate the system design against all 7 pillars:

1. **Scalability:** Identify the primary performance bottleneck under high concurrent load and blocking operations.
2. **Fault Tolerance:** Assess recovery mechanisms, durability checkpoints, retry strategies, and circuit breakers during partial outages.
3. **Isolation:** Evaluate multi-tenant resource sharing, noisy neighbor mitigations, and rate limiting.
4. **Observability:** Verify structured logging, correlation IDs, metrics collection, and distributed tracing.
5. **Consistency:** Determine message delivery guarantees (at-most-once, at-least-once, exactly-once) and idempotency handling.
6. **Capacity Planning:** Identify infrastructure components that fail or require redesign when scaling up load by 10x to 100x.
7. **CEO of Engineering Question:** Pinpoint fundamental design assumptions that break under massive overnight growth.

## Report Structure
Structure the architectural review as follows:
- **Architecture Overview:** Concise summary of system topology and request flows.
- **Pillar Analysis:** Key findings and critical flaws grouped by relevant pillars.
- **Architectural Recommendations:** Concrete, enterprise-grade mitigation strategies (e.g., event-driven decoupling, message queues, database connection pooling).

## Negative Constraints
- ❌ **No Code-Level Nitpicks:** Do not critique variable names, code formatting, or minor syntactical choices.
- ❌ **No Trivial Solutions:** Do not propose basic application fixes (e.g. try-catch blocks) for systemic structural flaws.
- ❌ **No Ideal Assumptions:** Never assume network stability, zero latency, or non-failing external APIs.

## Verification & Grounding Loop
1. Ground review assumptions in actual codebase files and configuration settings before critiquing limits.
2. Verify dependency maps and data paths using repository search tools.
