---
name: architecture-and-design-skill
description: Governs software system architecture, database schema design, REST/GraphQL API endpoint definitions, and layer isolation (Controllers vs Services vs Data Access). Use when designing application architectures, defining data models, mapping endpoints, or structuring backend services. Do NOT use for frontend UI styling or minor bug fixes.
---

# Architecture and System Design

Defines clean, scalable system blueprints, database schemas, and API contracts while enforcing strict layer separation and architectural patterns.

---

## Core Architectural Guidelines

1. **Layer Isolation & Dependency Direction**
   - **Controllers / Handlers:** Validate inputs, handle HTTP/RPC protocols, and delegate to Services. Zero business logic.
   - **Services:** Implement pure business logic and transaction boundaries. No protocol awareness (e.g. no direct request/response objects).
   - **Data Access / Repositories:** Enapsulate ORM (Prisma/SQLAlchemy) or database queries.

2. **Schema & Model Design**
   - Normalize relational database schemas (3NF) unless denormalization is explicitly justified for read-heavy workloads.
   - Mandate foreign key constraints, explicit indexing on queried/joined columns, and soft-delete or timestamp fields (`created_at`, `updated_at`).
   - Define strict type contracts (Pydantic, TypeScript interfaces, or Protobuf) at API boundaries.

3. **REST & API Endpoint Conventions**
   - Use standard HTTP verbs (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
   - Enforce consistent JSON error response schemas across all endpoints (`{ "error": { "code": string, "message": string } }`).
   - Design idempotent state mutations for non-POST operations.

---

## Step-by-Step Execution Workflow

1. **Requirement & State Analysis**
   - Identify domain entities, relationships (1:1, 1:N, N:M), transaction boundaries, and read/write ratios.
2. **Schema & Model Definition**
   - Draft database migration files / ORM schemas (Prisma, TypeORM, SQLAlchemy) and API DTO contracts.
3. **Service & Layer Structuring**
   - Map business logic into decoupled service functions with explicit interface contracts and dependency injection.
4. **Validation & Verification**
   - Verify architectural integrity and layer isolation using project linters or custom schema validators.

---

## Constraints

* ❌ **No Leakage:** Controller types/HTTP headers must never leak into the service layer.
* ❌ **No Direct DB Calls in Controllers:** Handlers must never query database instances or ORMs directly.
* ❌ **No Unindexed Foreign Keys:** Always generate index definitions for join keys.

---

## Verification Checklist

- [ ] All database relations have explicit indexes on foreign keys.
- [ ] DTO schemas validate incoming API payloads at the transport layer boundary.
- [ ] Service methods contain zero HTTP framework dependencies.
- [ ] Schema changes include incremental migration scripts.
