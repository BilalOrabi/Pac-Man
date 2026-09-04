.PHONY: help install run debug clean lint test package

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies using uv"
	@echo "  make run          - Run the Pac-Man game with config.json"
	@echo "  make debug        - Run the game with Python debugger (pdb)"
	@echo "  make clean        - Remove generated files and cache directories"
	@echo "  make lint         - Run flake8 and mypy type checking"
	@echo "  make test         - Run the test suite"

install:
	uv sync

run:
	uv run python pac-man.py config.json

debug:
	uv run python -m pdb pac-man.py config.json

clean:
	@echo "==> Cleaning generated files and cache directories..."

	find . -type d \( \
		-name "__pycache__" -o \
		-name ".pytest_cache" -o \
		-name ".mypy_cache" -o \
		-name ".ruff_cache" -o \
		-name ".tox" -o \
		-name ".nox" -o \
		-name "*.egg-info" \
	\) -prune -exec rm -rf {} +

	find . -type f \( \
		-name "*.pyc" -o \
		-name "*.pyo" -o \
		-name "*.coverage" \
	\) -delete

	rm -rf .coverage
	rm -rf htmlcov
	rm -rf coverage.xml
	rm -rf dist
	rm -rf build

	@echo "==> Clean complete."

lint:
	@echo "==> Running flake8..."
	uv run flake8 --count src/

	@echo "==> Running mypy..."
	uv run mypy \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		src/

test:
	@echo "==> Running tests..."
	uv run pytest

package:
	@echo "==> Packaging project for distribution..."
	uv run python package.py