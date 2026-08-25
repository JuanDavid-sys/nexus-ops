.PHONY: help install lint format backend-migrate frontend-dev up down logs migrate nuke db-shell

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: backend-install frontend-install ## Install all dependencies

backend-install: ## Create venv (Python 3.13) and install backend deps
	cd backend && uv venv --python 3.13 .venv && uv pip install --python .venv/bin/python -r requirements/local.txt

frontend-install: ## Install frontend dependencies
	cd frontend && npm install

lint: backend-lint frontend-lint ## Run all linters

backend-lint: ## Ruff over backend
	cd backend && .venv/bin/ruff check .

frontend-lint: ## ESLint + Prettier check over frontend
	cd frontend && npm run lint && npm run format:check

format: ## Auto-format frontend code
	cd frontend && npm run format

backend-migrate: ## Apply backend migrations (dev)
	cd backend && .venv/bin/python manage.py migrate

frontend-dev: ## Run Next.js dev server
	cd frontend && npm run dev

up: ## Start the full stack in detached mode (builds if needed)
	docker compose up -d --build

down: ## Stop the stack (data volumes are preserved)
	docker compose down

logs: ## Follow logs from all services
	docker compose logs -f --tail=100

migrate: ## Apply migrations inside the backend container
	docker compose exec backend python manage.py migrate

nuke: ## Stop the stack and delete data volumes (fresh database)
	docker compose down -v

db-shell: ## Open a PostgreSQL shell inside the db container
	docker compose exec db psql -U $${POSTGRES_USER:-nexus} -d $${POSTGRES_DB:-nexus}

# Native (non-Docker) targets below — useful when working outside the stack.
