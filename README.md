# NEXUS OPS

> Multi-tenant enterprise operations & AI platform.
> Next.js · TypeScript · Django · PostgreSQL + pgvector · Redis · Celery *(roadmap)*

![Backend CI](https://github.com/JuanDavid-sys/nexus-ops/actions/workflows/backend-ci.yml/badge.svg)
![Frontend CI](https://github.com/JuanDavid-sys/nexus-ops/actions/workflows/frontend-ci.yml/badge.svg)

**Status:** 🚧 under active development — Phase 1 (vertical slice MVP).

A company's information arrives through many channels — WhatsApp, email, forms, files, APIs.
NEXUS classifies it, acts on it with permission-checked AI agents, runs background jobs and
streams progress back to real-time dashboards. Every byte of data belongs to exactly one
tenant, enforced by construction.

## Documentation

- [Project plan & roadmap](PLAN.md)
- [Kanban board](https://github.com/users/JuanDavid-sys/projects/1)
- [Architecture Decision Records](docs/decisions/)

## Quick start

Requires [Docker](https://docs.docker.com/get-docker/) and `make`.

```bash
cp .env.example .env
make up
```

| Service | URL |
|---|---|
| Frontend (Next.js dev) | http://localhost:3000 |
| Backend API / admin | http://localhost:8000/admin/ |
| PostgreSQL 16 + pgvector | localhost:5432 (`nexus` / `nexus`) |
| Redis | localhost:6379 |

Common commands: `make up` · `make down` · `make logs` · `make migrate` · `make nuke` (wipe data) · `make help`.
The stack runs with hot reload — edits under `backend/` and `frontend/` apply without restarting.

## License

[MIT](LICENSE)
