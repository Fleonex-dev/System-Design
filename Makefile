.PHONY: help setup run clean lint test

VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
ACTIVATE := . $(VENV)/bin/activate

default: run

help: ## Show this help message
	@echo "🤖 System Design Course - Usage"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Create venv and install dependencies
	@echo "🚀 Setting up..."
	@python3 -m venv $(VENV)
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "✅ Setup complete. Run 'make run' to start."

run: ## Start the interactive CLI course
	@if [ ! -d "$(VENV)" ]; then echo "❌ Venv missing. running setup..."; make setup; fi
	@$(PYTHON) learn.py

clean: ## Remove venv and cache files
	@echo "🧹 Cleaning..."
	@rm -rf $(VENV)
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "✨ Cleaned."

lint: ## Check code quality
	@$(PYTHON) -m pylint **/*.py || true

test: ## Run the test suite
	@$(PYTHON) -m pytest tests/

