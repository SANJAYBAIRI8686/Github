.PHONY: up down migrate seed test backend-test frontend-test

up:
	docker compose up --build

down:
	docker compose down -v

migrate:
	alembic upgrade head

seed:
	python scripts/seed_demo.py

test:
	python -m pytest

backend-test:
	python -m pytest tests

frontend-test:
	cd frontend && npm test
