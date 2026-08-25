# NEXUS OPS — Project Plan

> Multi-tenant enterprise operations & AI platform.
> Built as a demonstration of production-grade software engineering: architecture, security,
> async processing, observability and AI orchestration — not just CRUD.

**Status:** Phase 1 in progress · **Tracking:** [GitHub Projects board](https://github.com/users/JuanDavid-sys/projects) · **ADRs:** [`docs/decisions/`](docs/decisions/)

---

## Vision

Companies feed NEXUS with information from many channels (WhatsApp, email, web, files,
forms, APIs). The platform classifies, processes and acts on it: AI-driven intent detection,
permission-checked tool execution, background jobs, real-time dashboards — with **strict
per-tenant data isolation**.

The differentiator vs. a typical portfolio project is not the feature list. It is that every
component exists for a documented reason (see ADRs), is tested, measured, and designed to
fail gracefully.

## Guiding principles

1. **Vertical slices over horizontal layers** — one domain end-to-end before adding depth.
2. **Modular monolith first** — extract services only when a proven reason exists.
3. **Evidence over claims** — metrics only if actually measured; failure modes implemented, not described.
4. **Security by default** — tenant isolation enforced at the data-access layer, never per-view.
5. **Docs are part of the deliverable** — ADRs, runbooks and threat model ship with the code.

## Tech stack

| Layer | Choice |
|---|---|
| Frontend | Next.js · React · TypeScript (strict) · Tailwind · TanStack Query · Zustand |
| Backend | Python · Django · Django REST Framework |
| Database | PostgreSQL 16 + pgvector |
| Async / cache | Redis · Celery *(Phase 2)* |
| Realtime | WebSockets via Django Channels *(Phase 2)* |
| AI | LLM provider behind an internal gateway · embeddings + pgvector RAG · tool calling *(Phase 3)* |
| Infra | Docker Compose · GitHub Actions · Railway/Fly.io |
| Testing | pytest (+factory_boy) · Vitest · Playwright *(later phases)* |
| Quality | ruff · ESLint · Prettier · mypy |

## Roadmap

### Phase 1 — Vertical slice MVP (weeks 0–3) ← current

A complete slice of one domain (Customers → Orders) proving tenancy end-to-end:
auth, RBAC, isolation, audit, tests, CI, deploy, live demo.

| # | Deliverable | Board column |
|---|---|---|
| 1 | Scaffold monorepo structure | This week |
| 2 | Docker Compose dev environment (PostgreSQL+pgvector, Redis) | This week |
| 3 | CI pipeline (lint, typecheck, tests, build) | This week |
| 4 | ADR-001–003 foundational decisions | This week |
| 5–12 | Tenancy core, JWT rotation, RBAC, Customers/Orders CRUD, audit trail, IDOR+RBAC test suite, OpenAPI docs | Backlog |
| 13–18 | Next.js foundation, auth flow, app shell, Customers page, Orders page, audit view | Backlog |
| 19–21 | Demo seed script, production deploy, README v1 | Backlog |

**Definition of done (every feature):**
- Acceptance criteria met and covered by automated tests
- Tenant isolation verified (cross-tenant access returns 404)
- Lint/type/tests green in CI
- Public-facing behavior documented where non-obvious

### Phase 2 — Senior signals (weeks 4–8)

Celery + Redis background jobs (`process_document`, `send_notification`, `generate_report`) ·
internal event bus (`ORDER_CREATED` → audit/notification/analytics handlers) ·
Django Channels WebSockets with job progress streaming · structured logging with `request_id`
correlation across API→worker→DB · metrics + `/health`, `/ready` · rate limiting hardening ·
query optimization with before/after EXPLAIN evidence.

### Phase 3 — Differentiators (weeks 9–14)

AI orchestration layer (intent detection → permission check → context retrieval → LLM →
structured output validation → tool execution → audit) · RAG over tenant documents with
pgvector · agent tool-calling with explicit permission gates · k6 load testing with published
results · chaos/failure scenarios (retries, idempotency keys, circuit breakers, DLQ strategy).

## Key architectural decisions

| ADR | Decision |
|---|---|
| [ADR-001](docs/decisions/ADR-001-modular-monolith.md) | Modular monolith over microservices — no organizational or technical scale to justify the operational cost yet |
| [ADR-002](docs/decisions/ADR-002-postgresql-pgvector.md) | PostgreSQL + pgvector — one datastore for relational data and vectors; trivial tenant filtering |
| [ADR-003](docs/decisions/ADR-003-multi-tenancy.md) | Shared DB, shared schema, `tenant_id` FK — isolation enforced in base querysets/middleware, cross-tenant access impossible by construction |

## Interview readiness

Every question below has a real implementation or ADR behind it:

Why a modular monolith? · How is tenant isolation guaranteed? · What happens on refresh-token reuse? ·
How do you prevent duplicate webhook processing? · What if Redis/Postgres/the LLM provider goes down? ·
Where's the bottleneck and how was it measured? · When would you extract Kafka/microservices?

## Non-goals (for now)

Microservices · Kubernetes · multi-region · billing integration · mobile clients.
