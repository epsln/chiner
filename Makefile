.PHONY: test

# Check if we're in a virtual env
.check-venv:
	@if [ -z "$(VIRTUAL_ENV)" ]; then \
		echo "You're not in a virtual env. Aborting..."; \
		exit 1; \
	fi

test: .check-venv
	@echo "Running tests for chiner."
	@python -m unittest discover -s src/tests/analyzers/ -p *_test.py
	@python -m unittest discover -s src/tests/database/ -p *_test.py

lint: .check-venv
	@echo "Running linter for chiner."
	@pylint src/chiner
	
install: .check-venv
	@echo "Installing chiner."
	@pip install .
