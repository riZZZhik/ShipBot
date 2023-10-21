SHELL := /usr/bin/env bash -o errtrace -o pipefail -o noclobber -o errexit -o nounset
.DEFAULT_GOAL := help

SOURCES ?= app
PROJECT_CONFIG ?= pyproject.toml

IMAGE_NAME ?= ship-bot:latest

.PHONY: help
help: ## Show this help
	@echo "Usage: make [target] ..."
	@echo
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-38s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

####################################################################################################
# Build
####################################################################################################

.PHONY: install
install: ## Install project dependencies
	poetry install

.PHONY: install.dev
install.dev: ## Install project dependencies for development
	poetry install --with lint

.PHONY: build
build: ## Build the docker image
	docker build -t $(IMAGE_NAME) .

####################################################################################################
# Lint
####################################################################################################

.PHONY: format
format: ## Format the source code
	poetry run black $(SOURCES)
	poetry run isort $(SOURCES)

.PHONY: lint.mypy
lint.mypy:
	poetry run mypy --pretty $(SOURCES)

.PHONY: lint.refurb
lint.refurb:
	poetry run refurb $(SOURCES)

.PHONY: lint.flake8
lint.flake8:
	poetry run flake8 $(SOURCES)

.PHONY: lint.xenon
lint.xenon:
	@# xenon is not configurable by itself
	source /dev/stdin <<<"$$(grep xenon_ $(PROJECT_CONFIG)|tr -d ' ')" \
		&& poetry run xenon -e $${xenon_exclude} -b $${xenon_max_absolute} -m $${xenon_max_modules} -a $${xenon_max_average} $(SOURCES)

.PHONY: lint.isort
lint.isort:
	poetry run isort --check-only --diff $(SOURCES)

.PHONY: lint.black
lint.black:
	poetry run black --check --diff $(SOURCES)

.PHONY: lint
lint: lint.mypy lint.refurb lint.flake8 lint.xenon lint.isort lint.black ## Lint the source code

####################################################################################################
# Run
####################################################################################################

.PHONY: run
run: ## Run the bot
	poetry run python app/bot.py

.PHONY: run.docker
run.docker: build ## Run the bot in a docker container
	docker run --rm -it -v $(PWD):/app $(IMAGE_NAME)
