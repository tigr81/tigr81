

help:
	@echo "Usage: make <target>"


install:
	uv sync --no-dev

install-dev:
	uv sync --extra dev

install-test:
	uv sync --extra test

install-all:
	uv sync --extra dev --extra test

test:
	uv run pytest tests

coverage:
	uv run pytest tests --cov-report html --cov=tigr81

format:
	uv run ruff check . --fix

check:
	uv run ruff check .

lint: format check

clean:
	rm -rf build/ dist/ *.egg-info && find . -type d -name __pycache__ -exec rm -r {} + && find . -type f -name '*.pyc' -delete && find . -type f -name '*.pyo' -delete && rm -rf .ruff_cache .pytest_cache .mypy_cache htmlcov .coverage .venv