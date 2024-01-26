install:
		poetry install

dev:
		poetry run flask --app page_analyzer/app --debug run

PORT ?= 8000
start:
		poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

selfcheck:
		poetry check

check: selfcheck test lint

test:
		cd tests/
		poetry run pytest

lint:
		poetry run flake8

coverage:
		poetry run pytest --cov=gendiff --cov-report xml

build:
		poetry build

package-install:
	python3 -m pip install --force-reinstall --user dist/*.whl

full-install: install build package-install


.PHONY: install dev PORT start install test lint check build update coverage selfcheck check
