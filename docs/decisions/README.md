# Architecture Decision Records

Every significant architectural decision is recorded here as an ADR.

An ADR captures the context, the decision, and its consequences (positive and negative).
Rejected alternatives are stated explicitly — knowing *why not* is as valuable as *why*.

## Index

| ADR | Title | Status |
|---|---|---|
| [ADR-001](ADR-001-modular-monolith.md) | Modular monolith over microservices | Accepted |
| [ADR-002](ADR-002-postgresql-pgvector.md) | PostgreSQL + pgvector as the single datastore | Accepted |
| [ADR-003](ADR-003-multi-tenancy.md) | Multi-tenancy: shared DB, shared schema, tenant FK | Accepted |
| [ADR-004](ADR-004-always-run-ci.md) | Always-run CI pipelines over path filtering | Accepted |

## Format

New ADRs are created from [TEMPLATE](TEMPLATE.md).
