.PHONY: manage run install migrate venv shell

VENV = venv
PYTHON = $(VENV)/bin/python3
POETRY = $(VENV)/bin/poetry

manage:
	$(POETRY) run $(PYTHON) manage.py

run:
	$(POETRY) run $(PYTHON) manage.py runserver

install:
	$(POETRY) install

migrate:
	$(POETRY) run $(PYTHON) manage.py makemigrations
	$(POETRY) run $(PYTHON) manage.py migrate

shell:
	$(POETRY) run $(PYTHON) manage.py shell


