### VARIABLES ###

RUN=uv run
DATE=`date +%Y-%m-%d`
CODE_STYLE_FILE_LIST=todo

ARGS=$(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(ARGS):;@:)


### TARGETS ###

.PHONY: check_python check_uv install_uv install_python

PYTHON_VERSION := 3.12

# Detect OS
UNAME_S := $(shell uname -s)

# Check if uv is installed and install if not
check_uv:
	@if ! command -v uv >/dev/null 2>&1; then \
		$(MAKE) install_uv; \
	else \
		echo "uv is already installed."; \
	fi

# Install uv based on platform
install_uv:
ifeq ($(UNAME_S),Darwin)
	@echo "Installing uv on macOS..."
	@if command -v brew >/dev/null 2>&1; then \
		brew install uv || true; \
	else \
		echo "Homebrew not found. Installing uv via official installer..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
else ifeq ($(UNAME_S),Linux)
	@echo "Installing uv on Linux..."
	curl -LsSf https://astral.sh/uv/install.sh | sh
else ifeq ($(OS),Windows_NT)
	@echo "Installing uv on Windows..."
	@if command -v scoop >/dev/null 2>&1; then \
		echo "Installing uv via scoop..."; \
		scoop install uv || true; \
	else \
		echo "Installing uv via PowerShell..."; \
		powershell -Command "irm https://astral.sh/uv/install.ps1 | iex" || powershell -Command "Invoke-WebRequest -UseBasicParsing https://astral.sh/uv/install.ps1 | Invoke-Expression"; \
	fi
else
	@echo "Installing uv (generic installer)..."
	curl -LsSf https://astral.sh/uv/install.sh | sh
endif

# Check if Python 3.12 is available and install if not
check_python: check_uv
	@if ! uv python list 2>/dev/null | grep -q "$(PYTHON_VERSION)"; then \
		echo "Python $(PYTHON_VERSION) not found. Installing..."; \
		uv python install $(PYTHON_VERSION) || true; \
	else \
		echo "Python $(PYTHON_VERSION) is already available."; \
	fi

# Install uv
uv: check_uv

# Install requirements (including dev dependencies)
requirements: check_python
	uv sync --extra dev

deploy_requirements:
	${RUN} pip install wheel

# Install uv, Python, and requirements
dev: check_python requirements

# Spin up shell in virtual environment
venv:
	uv shell

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
	-rm -rf dist build td_cli.egg-info .pytest_cache .mypy_cache

build:
	${RUN} python setup.py sdist bdist_wheel

upload_test:
	${RUN} twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload:
	${RUN} twine upload --repository td-cli dist/*

install_test:
	${RUN} python -m pip install --index-url https://test.pypi.org/simple/ td-cli

install:
	${RUN} python -m pip install --upgrade td-cli

publish_test: clean build upload_test install_test

publish: clean build upload install
