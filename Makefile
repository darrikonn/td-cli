### VARIABLES ###

RUN=poetry run
DATE=`date +%Y-%m-%d`
CODE_STYLE_FILE_LIST=todo

ARGS=$(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(ARGS):;@:)


### TARGETS ###

# Install poetry
poetry:
	pip3 install poetry

# Install requirements
requirements:
	poetry install --no-root

deploy_requirements:
	${RUN} pip install wheel

# Install poetry and requirements
dev: poetry requirements

# Spin up shell in virtual environment
venv:
	poetry shell

# Lint using flake8
flake8:
	${RUN} flake8 ${CODE_STYLE_FILE_LIST}

# Lint using black
black:
	${RUN} black --target-version py38 --check ${CODE_STYLE_FILE_LIST}

# Format using black
black_format:
	${RUN} black --target-version py38 ${CODE_STYLE_FILE_LIST}

# Lint using isort
isort:
	${RUN} isort -c ${CODE_STYLE_FILE_LIST}

# Format using isort
isort_format:
	${RUN} isort ${CODE_STYLE_FILE_LIST}

# Lint using mypy
mypy:
	${RUN} mypy ${CODE_STYLE_FILE_LIST}

# Lint using all methods combined
lint: flake8 black isort mypy

# Format using all methods combined
format: black_format isort_format

clean:
	-rm -r dist build td_cli.egg-info 2> /dev/null

build:
	${RUN} python setup.py sdist bdist_wheel

upload_test:
	${RUN} twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload:
	${RUN} twine upload --repository td-cli dist/*

install_test:
	${RUN} python -m pip install --index-url https://test.pypi.org/simple/ td-cli

install:
	${RUN} python -m pip install td-cli

publish_test: clean build upload_test install_test

publish: clean build upload install
