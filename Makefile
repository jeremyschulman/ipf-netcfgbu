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

.PHONY: test
test:
	pytest \
		--cov-report=term --cov-report=html \
		--cov=${PACKAGE_NAME}/api \
		--cov=${PACKAGE_NAME}/slack/rbac \
		--cov=${PACKAGE_NAME}/clients \
		--cov=${PACKAGE_NAME}/netbox \
		--cov=${PACKAGE_NAME}/sentry \
		--cov=${PACKAGE_NAME}/exceptions \
		tests \


.PHONY: run
run:
	poetry run ${PACKAGE_NAME}

kill:
	pgrep -f ${PACKAGE_NAME} | xargs kill -9

clean:
	rm -rf .pytest_cache
	find . -name '__pycache__' | xargs rm -rf

# -----------------------------------------------------------------------------
# Building Docker image
# -----------------------------------------------------------------------------

DOCKER = docker
DOCKER_BUILDDIR = .
DOCKERFILE = $(DOCKER_BUILDDIR)/Dockerfile
DOCKER_IMAGE_NAME = $(PACKAGE_NAME)
DOCKER_TAG = $(PACKAGE_VERSION)
DOCKER_TARGET = $(DOCKER_IMAGE_NAME).$(DOCKER_TAG)
DOCKER_IMAGE = $(DOCKER_IMAGE_NAME):$(DOCKER_TAG)


image: $(DOCKER_TARGET)
	@echo "Build completed: $(DOCKER_TARGET)"

$(DOCKER_TARGET): $(DOCKERFILE)
	$(DOCKER) build \
		--tag $(DOCKER_IMAGE_NAME):$(DOCKER_TAG) \
		--file $(DOCKERFILE) \
		.

	$(DOCKER) tag $(DOCKER_IMAGE) $(DOCKER_IMAGE_NAME):latest

# -----------------------------------------------------------------------------
# SystemD service commands to restart or stop chatops on the NMS server
# -----------------------------------------------------------------------------

restart:
	sudo systemctl restart docker-compose@chatopsv4

shutdown:
	sudo systemctl stop docker-compose@chatopsv4
