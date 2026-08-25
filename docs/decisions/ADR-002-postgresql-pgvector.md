# ADR-002: PostgreSQL + pgvector as the single datastore

- **Status:** Accepted
- **Date:** 2026-08-25
- **Deciders:** JuanDavid-sys

## Context

The platform needs strict relational integrity today — tenant foreign keys, uniqueness
constraints, transactional audit writes — and will need semantic search over documents
(RAG) in Phase 3. The datastore choice must be made before either concern is at scale.

## Decision

PostgreSQL 16 is the only datastore. The `pgvector` extension is enabled from day one
(via database initialization scripts), so embeddings will live next to relational rows,
filtered by the same `tenant_id` that protects every other resource.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| Dedicated vector DB (Pinecone / Qdrant / Weaviate) | Adds a service to operate, secure and pay for before vector count justifies it; tenant isolation would have to be duplicated across two systems; data sync becomes a new failure mode |
| MongoDB / document stores | Weaken the relational constraints (FKs, unique constraints, transactions) that multi-tenancy and audit correctness depend on |
| MySQL | No native vector extension; weaker fit with the Django/DRF ecosystem conventions used here |

## Consequences

**Positive**

- One backup/restore path, one connection pool, one migration tool
- Vectors inherit tenant isolation structurally (`tenant_id` FK) instead of relying on
  per-query discipline against an external service
- Transactions span relational mutations and their metadata — critical for audit integrity

**Negative / trade-offs accepted**

- pgvector's ANN performance has a ceiling below dedicated engines; accepted until
  measured p95 semantic-search latency degrades. The migration path (sync job feeding a
  specialized engine) is deliberately documented but not built — no speculative infra.
