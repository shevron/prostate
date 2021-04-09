# Package / Project specific configuration
PACKAGE_NAME := prostate
DOCKER_IMAGE_NAME := prostate

# Useful commands and tools
SHELL := bash
PYTHON := python
PIP := pip
PIP_COMPILE := pip-compile
PYTEST := pytest
MYPY := mypy
GIT := git
SED := sed

# Paths, directories and default names
PACKAGE_DIRS := prostate
TESTS_DIR := tests
SENTINELS := .make-cache
DIST_DIR := dist

# Optional arguments
PYTEST_EXTRA_ARGS :=

# Computed values
VERSION := $(shell $(PYTHON) -c 'import $(PACKAGE_NAME) as p; print(p.__version__);')
SOURCE_FILES := $(shell find $(PACKAGE_DIRS) $(TESTS_DIR) -type f -name "*.py")
TEST_PATHS := $(PACKAGE_DIRS) $(TESTS_DIR)

default: help

dev-requirements.txt: dev-requirements.in
	$(PIP_COMPILE) --no-emit-index-url dev-requirements.in -o $@

requirements.txt: requirements.in
	$(PIP_COMPILE) --no-emit-index-url requirements.in -o $@

## Update requirements files for the current Python environment
requirements: $(SENTINELS)/requirements

## Set up development environment
dev-setup: $(SENTINELS)/dev-setup

## Run all tests
test: $(SENTINELS)/dev-setup
	$(MYPY) $(PACKAGE_DIRS)
	$(PYTEST) $(PYTEST_EXTRA_ARGS) $(TEST_PATHS)

## Print current version as stated in package code
print-version:
	@echo "$(VERSION)"

.PHONY: test requirements dev-setup print-version

$(SENTINELS):
	mkdir $@

$(SENTINELS)/requirements: requirements.txt dev-requirements.txt | $(SENTINELS)
	@touch $@

$(SENTINELS)/install: requirements.txt | $(SENTINELS)
	$(PIP) install -r requirements.txt
	@touch $@

$(SENTINELS)/install-dev: dev-requirements.txt | $(SENTINELS)
	$(PIP) install -r dev-requirements.txt
	$(PIP) install -e .
	@touch $@

$(SENTINELS)/dev-setup: requirements $(SENTINELS)/install $(SENTINELS)/install-dev setup.py | $(SENTINELS)
	@touch $@

# Help related variables and targets

GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)
TARGET_MAX_CHAR_NUM := 20

## Show help
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
	  helpMessage = match(lastLine, /^## (.*)/); \
	  if (helpMessage) { \
	    helpCommand = substr($$1, 0, index($$1, ":")-1); \
	    helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
	    printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
	  } \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
