.PHONY: lint, lint-check, test, run-local

lint:
	poetry run autoflake --verbose .
	poetry run black .
	poetry run flake8 --max-line-length 120 --ignore "E203, W503" .
	poetry run isort .
	poetry run mypy .
	poetry run pylint underwriter

lint-check:
	poetry run black --check .
	poetry run flake8 --max-line-length 120 --ignore "E203, W503" .
	poetry run isort --check .
	poetry run mypy .
	poetry run pylint underwriter

test:
	ENV=test poetry run python3 -m pytest --spec -v --color=yes

run-local:
	ENV=development poetry run uvicorn underwriter.api.main:app --reload --host "0.0.0.0"
