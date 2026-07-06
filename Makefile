.PHONY: help install dev lint format test test-cov clean run

help:
	@echo "Yahtzee development commands:"
	@echo "  make install    - Install the package"
	@echo "  make dev        - Install with dev dependencies"
	@echo "  make lint       - Run ruff linter"
	@echo "  make format     - Format code with black"
	@echo "  make format-check - Check formatting without modifying"
	@echo "  make test       - Run tests"
	@echo "  make test-cov   - Run tests with coverage report"
	@echo "  make clean      - Remove build artifacts and cache"
	@echo "  make run        - Run the game"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

lint:
	ruff check src/ tests/

format:
	black src/ tests/

format-check:
	black --check src/ tests/

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src/yahtzee --cov-report=html --cov-report=term-missing

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .coverage -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name *.egg-info -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/

run:
	python -m yahtzee
