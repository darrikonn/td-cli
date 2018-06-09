FLAKE8=$(shell which flake8 || echo venv/bin/flake8)

lint:
	$(FLAKE8) todo
