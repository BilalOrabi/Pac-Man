.PHONY: help install run debug clean lint lint-strict

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies using uv"
	@echo "  make run          - Run the Pac-Man game with config.json"
	@echo "  make debug        - Run the game with Python debugger (pdb)"
	@echo "  make clean        - Remove build artifacts and cache files"
	@echo "  make lint         - Run flake8 and mypy type checking"
	@echo "  make help         - Display this help message"

install:
	uv sync

run:
	uv run python pac-man.py config.json

debug:
	uv run python -m pdb pac-man.py config.json


clean:
	@echo "==> Cleaning cache and build artifacts..."
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.egg-info" -exec rm -rf {} +

lint:
	uv run flake8 --count src/
	uv run mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs src/
