FLAKE8=$(shell which flake8 || echo venv/bin/flake8)

lint:
	$(FLAKE8) todo

dist:
	python3 setup.py sdist bdist_wheel

upload_test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload:
	twine upload dist/*

install_test:
	python3 -m pip install --index-url https://test.pypi.org/simple/ td-cli

install:
	python3 -m pip install td-cli

publish_test: dist upload_test install_test

publish: dist upload install
