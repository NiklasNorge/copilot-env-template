# Common commands for data engineering projects
# Usage: make [command] (e.g., make test, make lint)

.PHONY: help install test lint format type-check clean run docs

help:
	@echo "Common commands:"
	@echo "  make install          - Install dependencies"
	@echo "  make test             - Run tests with coverage"
	@echo "  make test-quick       - Run tests without coverage"
	@echo "  make test-watch       - Run tests in watch mode"
	@echo "  make lint             - Run linters (ruff)"
	@echo "  make format           - Format code with black + isort"
	@echo "  make type-check       - Run type checker (mypy)"
	@echo "  make clean            - Remove build artifacts"
	@echo ""
	@echo "Data Engineering:"
	@echo "  make validate         - Run data quality checks"
	@echo "  make pipeline         - Run main ETL pipeline"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs             - Generate documentation"

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
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name ".mypy_cache" -delete
	find . -type d -name "*.egg-info" -delete
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -delete
	find . -type d -name ".DS_Store" -delete

# validate:
# 	python -m src.data.validators.quality
# Note: Uncomment after creating src/data/validators/quality.py via /setup-project

# pipeline:
# 	python -m src.data.pipelines.main
# Note: Uncomment after creating src/data/pipelines/main.py via /setup-project

# docs:
# 	cd docs && python -m sphinx . _build/html
# Note: Uncomment after installing sphinx (pip install sphinx)

# Quick development cycle
dev: format lint test-quick
	@echo "✓ Development cycle complete"

# Full validation before push
check: lint type-check test
	@echo "✓ All checks passed - ready to push"

# Docker (optional)
docker-build:
	docker build -t data-pipeline:latest .

docker-run:
	docker run -it data-pipeline:latest /bin/bash
