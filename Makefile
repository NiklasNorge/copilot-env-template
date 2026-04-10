# Reference Makefile for generated data engineering projects.
#
# This file is included as a bootstrap asset. It becomes useful after
# `/setup-project` or manual scaffolding creates `src/` and `tests/`.

.PHONY: help install test test-quick test-watch test-unit test-integration lint format type-check clean dev check

help:
	@echo "Reference commands for a generated project:"
	@echo "  make install          - Install dependencies"
	@echo "  make test             - Run tests with coverage"
	@echo "  make test-quick       - Run tests without coverage"
	@echo "  make test-watch       - Run tests in watch mode"
	@echo "  make lint             - Run ruff"
	@echo "  make format           - Run black and isort"
	@echo "  make type-check       - Run mypy"
	@echo "  make clean            - Remove common Python build artifacts"
	@echo ""
	@echo "Note: these targets assume a generated project with src/ and tests/."

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

test-quick:
	pytest tests/ -v --no-cov

test-watch:
	pytest-watch tests/

test-unit:
	pytest tests/unit/ -v --no-cov

test-integration:
	pytest tests/integration/ -v --no-cov

lint:
	ruff check src/ tests/

format:
	black src/ tests/
	isort src/ tests/

type-check:
	mypy src/ --ignore-missing-imports

clean:
	python -c "import pathlib, shutil; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; [shutil.rmtree(pathlib.Path(n), ignore_errors=True) for n in ['.pytest_cache','.mypy_cache','htmlcov'] if pathlib.Path(n).exists()]"

dev: format lint test-quick
	@echo "Development cycle complete"

check: lint type-check test
	@echo "All checks passed"
