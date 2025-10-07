.PHONY: up down build logs run lint test fmt

up:
	docker compose -f docker/compose.yml up -d --build

down:
	docker compose -f docker/compose.yml down -v

build:
	docker compose -f docker/compose.yml build --no-cache

logs:
	docker compose -f docker/compose.yml logs -f --tail=200 api

run:
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

lint:
	@echo "No linter configured yet"

test:
	@echo "No tests configured yet"
