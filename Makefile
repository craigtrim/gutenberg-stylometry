.PHONY: all install lint format test clean build

all: install lint test

install:
	poetry install

lint:
	poetry run ruff check gutenburg_stylometry tests scripts

format:
	poetry run ruff check --fix gutenburg_stylometry tests scripts
	poetry run ruff format gutenburg_stylometry tests scripts

test:
	poetry run pytest tests -v

clean:
	rm -rf dist .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build:
	poetry build

# TTR computation targets
ttr-list:
	poetry run python scripts/compute_ttr.py --list

ttr-%:
	poetry run python scripts/compute_ttr.py $*
