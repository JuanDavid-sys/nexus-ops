# ADR-003: Multi-tenancy — shared database, shared schema, tenant foreign key

- **Status:** Accepted
- **Date:** 2026-08-25
- **Deciders:** JuanDavid-sys

## Context

NEXUS OPS serves multiple companies (tenants) from one deployment. Tenant A must never
observe, enumerate or modify Tenant B's data — not through the API, not through a bug, not
through a forgotten filter. Three isolation strategies exist on PostgreSQL, and the choice
shapes migrations, operations and security for the life of the product.

## Decision

**Shared database, shared schema.** Every tenant-scoped table carries a `tenant_id` FK
(NOT NULL). Isolation is enforced structurally, not by discipline:

1. A base abstract model and default queryset manager inject the tenant filter automatically
2. Middleware resolves the active tenant from authenticated membership before any view runs
3. Cross-tenant access by id returns **404, never 403** — existence of another tenant's
   resource is itself information (prevents resource enumeration)

The correctness of this base layer is treated as critical infrastructure: the test suite
(issue #11) includes an IDOR matrix that makes any isolation regression **CI-blocking**.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| Database per tenant | Strongest isolation, but N× migration sprawl, connection-pool exhaustion as tenants grow, and cross-tenant platform analytics becomes an ETL problem; justified only for compliance-heavy enterprise tiers |
| Schema per tenant (PostgreSQL schemas) | Middle ground with real tooling friction: every migration fans out to N schemas, Django support exists but the ecosystem around it is rough |
| Per-view filtering ("remember to filter") | Rejected outright — one forgotten `filter(tenant=…)` in one endpoint is a catastrophic data breach; isolation must be structural so it cannot be forgotten |

## Consequences

**Positive**

- Onboarding a tenant is a row insert, not a provisioning pipeline
- One migration path for all tenants; schema evolution stays cheap
- Platform-wide analytics (the product's own metrics) are plain SQL

**Negative / trade-offs accepted**

- Noisy-neighbour risk at the database level; mitigated in Phase 2 with rate limiting and
  selective row locking
- Defense depends on the correctness of one base model/manager pair; mitigated by the
  CI-blocking IDOR suite rather than by optimism
