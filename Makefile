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
	rm -rf __pycache__ .pytest_cache .mypy_cache .venv build dist
	find . -type d \( -name "__pycache__" -o -name "*.egg-info" \) -exec rm -rf {} +

lint:
	uv run flake8 --count src/
	uv run mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs src/
