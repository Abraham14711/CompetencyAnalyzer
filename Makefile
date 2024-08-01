install:
	poetry install

test:
	poetry run pytest

package-install:
	python3 -m pip install --user dist/*.whl

publish:
	poetry publish --dry-run

test-coverage:
	poetry run pytest --cov=competencyAnalyser --cov-report xml

lint:
	poetry run flake8 competencyAnalyser

selfcheck:
	poetry check

check: selfcheck test lint

build: check
	poetry build

.PHONY: install test lint selfcheck check build

run:
	poetry run competency-analyser
