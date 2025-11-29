# ==================================================
# Clean
# ==================================================

.PHONY: clean
clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type d -name '*.py[cod]' -exec rm -f {} +
	@echo "Python cache cleaned."

# ==================================================
# Linting
# ==================================================

.PHONY: format
format:
	ruff format .

.PHONY: lint
lint:
	ruff check .



