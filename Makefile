.PHONY: install dev lint test
.DEFAULT_GOAL := install

install:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest

lint:
	black .
	isort .

# Run everything — useful for CI
ci: lint test
