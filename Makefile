.PHONY: install run debug clean lint lint-strict

install:
	uv sync

run:
	uv run python pac-man.py config.json

debug:
	uv run python -m pdb pac-man.py config.json

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache .venv build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	uv run flake8 --count src/
	uv run mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs src/

lint-strict:
	uv run flake8 src/
	uv run mypy --strict src/