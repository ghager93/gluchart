.PHONY: run install migrate source-activate source-deactivate

VENV = venv
PYTHON = $(VENV)/bin/python3
POETRY = $(VENV)/bin/poetry

run:
	$(POETRY) run $(PYTHON) manage.py runserver

install:
	$(POETRY) install

migrate:
	$(POETRY) run $(PYTHON) manage.py migrate


