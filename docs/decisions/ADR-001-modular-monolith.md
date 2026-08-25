# ADR-001: Modular monolith over microservices

- **Status:** Accepted
- **Date:** 2026-08-25
- **Deciders:** JuanDavid-sys

## Context

NEXUS OPS is a multi-tenant SaaS platform built by a single developer, pre-product-market-fit,
with a roadmap that includes background jobs, WebSockets and AI orchestration. The question is
how to structure the backend: one deployable with internal boundaries, or distributed services
from the start.

Microservices trade development simplicity for operational complexity — service discovery,
network failure modes, eventual consistency, distributed tracing, deployment orchestration.
That cost pays off only when multiple teams need to deploy independently at different cadences.
This project has no teams, no independent release trains, and no scale pressure yet.

## Decision

Build a single Django deployable organized as a **modular monolith**: each domain
(`accounts`, `tenants`, `customers`, `orders`, `audit`, …) lives in its own app under `apps/`
as a bounded context with an explicit interface, minimizing shared models.

Extraction into a service remains possible because boundaries exist *inside* the codebase —
but extraction is deferred until an actual forcing function appears (organizational or load).

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| Microservices from day 0 | Operational cost (distributed debugging, infra, contracts) with no organizational benefit; a solo developer would spend more time operating plumbing than building product |
| Serverless functions per feature | Poor fit for stateful features already on the roadmap (WebSockets, long-running AI jobs); ORM-driven domain logic fragments across runtimes |
| Monolith without module discipline | The default trap: cheap now, but boundary erosion makes later extraction impossible; rejected because it forecloses options rather than deferring them |

## Consequences

**Positive**

- Single transaction scope — tenancy-critical invariants (audit + mutation) commit atomically
- One deploy, one log stream, trivial local debugging, fast iteration
- Refactors across domains stay mechanical (IDE-level), not API-contract migrations

**Negative / trade-offs accepted**

- Scaling is all-or-nothing at first; mitigated progressively via Celery workers for async
  load (Phase 2) before any service split
- Module boundaries can silently erode; mitigation planned as import-linting rules once the
  number of modules makes violations non-obvious
