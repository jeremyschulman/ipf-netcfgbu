PACKAGE_and_VERSION = $(shell poetry version)
PACKAGE_NAME = $(word 1, $(PACKAGE_and_VERSION))
PACKAGE_VERSION = $(word 2, $(PACKAGE_and_VERSION))

# -----------------------------------------------------------------------------
# Devel targets
# -----------------------------------------------------------------------------

.PHONY: precheck
precheck:
	black $(PACKAGE_NAME)
	pre-commit run -a
	interrogate -c pyproject.toml

.PHONY: doccheck
doccheck:
	interrogate ${PACKAGE_NAME} tests -vv --omit-covered-files

clean:
	rm -rf .pytest_cache
	find . -name '__pycache__' | xargs rm -rf

