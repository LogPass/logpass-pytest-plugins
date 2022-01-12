SHELL:=/usr/bin/env bash

BASE_UNIT_STAGE:=unit_local
ifeq ($(CI), true)
	BASE_UNIT_STAGE:=unit_ci
endif


.PHONY: lint_python
lint_python:
	poetry run flake8 .
	poetry run mypy .
	poetry run lint-imports


.PHONY: unit_local
unit_local:
	poetry run pytest


.PHONY: unit_ci
unit_ci:
	poetry run pytest \
		--junitxml .tests_reports/junit.xml


.PHONY: unit
unit: $(BASE_UNIT_STAGE)
	poetry run pytest --dead-fixtures --dup-fixtures


.PHONY: lint_package
lint_package:
	poetry check
	poetry run pip check
	poetry run safety check --full-report


.PHONY: test
test: \
	lint_python \
	unit \
	lint_package
