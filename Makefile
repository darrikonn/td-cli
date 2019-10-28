CODE_STYLE_FILE_LIST=todo

ARGS=$(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(ARGS):;@:)

### TARGETS ###

venv:
	virtualenv venv

requirements:
	venv/bin/pip install -e ".[dev]"
	venv/bin/pip install -e ".[deploy]"

bootstrap: venv requirements

flake8:
	venv/bin/flake8 ${CODE_STYLE_FILE_LIST}

black:
	venv/bin/black --target-version py37 --check ${CODE_STYLE_FILE_LIST}

black_format:
	venv/bin/black --target-version py37 ${CODE_STYLE_FILE_LIST}

isort:
	venv/bin/isort -c -rc ${CODE_STYLE_FILE_LIST}

isort_format:
	venv/bin/isort -rc ${CODE_STYLE_FILE_LIST}

mypy:
	venv/bin/mypy ${CODE_STYLE_FILE_LIST}

lint: flake8 black isort mypy

format: black_format isort_format

clean:
	-rm -r dist build td_cli.egg-info 2> /dev/null

build:
	venv/bin/python3 setup.py sdist bdist_wheel

upload_test:
	venv/bin/twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload:
	venv/bin/twine upload dist/*

install_test:
	venv/bin/python3 -m pip install --index-url https://test.pypi.org/simple/ td-cli

install:
	venv/bin/python3 -m pip install td-cli

publish_test: clean build upload_test install_test

publish: clean build upload install
