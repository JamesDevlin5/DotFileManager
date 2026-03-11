.PHONY: install dev lint test
.DEFAULT_GOAL := install

install:
	uv python pin 3.12
	uv sync
	uv run pre-commit install

test:
	uv run pytest

lint:
	uv run isort --profile black .
	uv run black --target-verion py312 .

# Run everything — useful for CI
ci: lint test
