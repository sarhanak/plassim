PY ?= python3
PIP ?= pip3

.PHONY: up down build logs shell api test lint fmt

up:
	docker compose -f docker/compose.yml up -d --build

down:
	docker compose -f docker/compose.yml down -v

build:
	docker compose -f docker/compose.yml build

logs:
	docker compose -f docker/compose.yml logs -f api

shell:
	docker compose -f docker/compose.yml exec api /bin/sh

api:
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest -q

lint:
	rufflehog --version >/dev/null 2>&1 || true
	rufflehog --help >/dev/null 2>&1 || true
	ruff --fix --target-version=py311 || true

fmt:
	ruff --fix --target-version=py311 || true
