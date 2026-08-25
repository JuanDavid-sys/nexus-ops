# ADR-004: Always-run CI pipelines over path filtering

- **Status:** Accepted
- **Date:** 2026-08-25
- **Deciders:** JuanDavid-sys

## Context

Two independently reasonable features were combined in the initial CI setup:

1. **Path filtering** — workflows declared `paths:` triggers so, e.g., a frontend-only PR
   would skip Backend CI (~30s of runner time saved)
2. **Branch protection on `main`** — merges require *both* check contexts to report success

PR #24 (a frontend-only fix) exposed the interaction: because Backend CI never triggered,
its required context stayed in *Expected* state forever — **every frontend-only PR was
permanently unmergeable**, even with all relevant checks green. A deadlock by design.

## Decision

Remove path filters. Both pipelines run on every PR and push to `main`, in parallel.
Total wall time is ~45–90s on free runners; correctness of the merge gate matters more
than the compute saved.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| `dorny/paths-filter` (move filtering into job conditions) | Jobs skipped via conditions create check runs that satisfy protection — works, but adds a third-party supply-chain dependency to save seconds |
| Guard jobs (tiny always-run job per workflow just to register the required context) | Works natively, but each workflow now carries a vestigial job whose only purpose is explaining a workaround |
| Relax branch protection (require fewer checks) | Defeats the point of issue #3 — the merge gate is load-bearing |

## Consequences

**Positive**

- The required-check contract is trivially satisfiable: every PR produces both contexts
- Zero third-party actions; smaller supply chain
- `main` is validated end-to-end on every change regardless of touched paths (root files
  like `docker-compose.yml` affect both sides anyway)

**Negative / trade-offs accepted**

- Docs-only or single-side PRs run ~30s of "unnecessary" checks; accepted as the price of
  a deadlock-free gate

## Lesson recorded

Two individually sound decisions can compose into a broken system when their assumptions
are never tested together. The failure appeared not in either feature, but in their
interaction — which is exactly the class of bug integration tests and staged rollouts
exist to catch.
