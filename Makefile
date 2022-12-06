.PHONY: lint, lint-check, test, run-local

lint:
	poetry run autoflake  --in-place --remove-all-unused-imports --verbose -r underwriter tests
	poetry run black underwriter tests --target-version py310 -l120
	poetry run flake8 underwriter tests --max-line-length 120 --ignore "E203, W503" 
	poetry run isort underwriter tests 

lint-check:
	poetry run black underwriter tests --target-version py310 -l120 --check 
	poetry run flake8 underwriter tests --max-line-length 120 --ignore "E203, W503"
	poetry run isort --check underwriter tests

test:
	ENV=test poetry run python3 -m pytest -v --color=yes

run-local:
	ENV=development poetry run uvicorn underwriter.main:app --reload --host "0.0.0.0"
