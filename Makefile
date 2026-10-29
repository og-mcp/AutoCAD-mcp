# ==============================================================================
# architect-cad-mcp — Build, Test & Docker Publish Makefile
# ==============================================================================
# Usage:
#   make help                         # list targets
#   make version                      # print version from pyproject.toml
#   make test                         # run pytest suite
#   make build                        # build local Docker image
#   make publish DOCKER_USERNAME=me   # build multi-arch image & push to Docker Hub
# ==============================================================================

PYTHON          ?= python
DOCKER_USERNAME ?= ogmcp
IMAGE_NAME      ?= architect-cad-mcp
IMAGE           ?= $(DOCKER_USERNAME)/$(IMAGE_NAME)
PLATFORMS       ?= linux/amd64,linux/arm64

# Single source of truth for the version: [project].version in pyproject.toml
VERSION := $(shell $(PYTHON) -c "import tomllib;print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])")

.DEFAULT_GOAL := help
.PHONY: help version install test health demo build run run-sse tag push publish clean

help: ## Show available targets
	@echo "architect-cad-mcp v$(VERSION) - image: $(IMAGE)"
	@echo "Targets: version install test health demo build run run-sse tag push publish clean"

version: ## Print the package version (used by CI to detect releases)
	@echo $(VERSION)

install: ## Install package with dev dependencies (editable)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"

test: ## Run the pytest suite
	$(PYTHON) -m pytest -v

health: ## Run the built-in diagnostic health probe
	$(PYTHON) -m architect_cad_mcp.health

demo: ## Run the headless ezdxf demo (DXF + audit + PNG)
	$(PYTHON) examples/headless_demo.py

build: ## Build the local Docker image (single-arch)
	docker build --build-arg VERSION=$(VERSION) -t $(IMAGE_NAME):latest -t $(IMAGE):$(VERSION) -t $(IMAGE):latest .

run: ## Run the container in stdio mode (for MCP clients)
	docker run -i --rm -v "$(CURDIR)/cad_output:/app/cad_output" $(IMAGE_NAME):latest

run-sse: ## Run the container as an SSE network service on :8000
	docker run --rm -p 8000:8000 -v "$(CURDIR)/cad_output:/app/cad_output" $(IMAGE_NAME):latest --transport sse --host 0.0.0.0 --port 8000

tag: ## Tag the local image for Docker Hub
	docker tag $(IMAGE_NAME):latest $(IMAGE):$(VERSION)
	docker tag $(IMAGE_NAME):latest $(IMAGE):latest

push: tag ## Push the local single-arch image to Docker Hub
	docker push $(IMAGE):$(VERSION)
	docker push $(IMAGE):latest

publish: ## Build multi-arch image (amd64+arm64) and push :VERSION and :latest
	docker buildx build \
		--platform $(PLATFORMS) \
		--build-arg VERSION=$(VERSION) \
		--tag $(IMAGE):$(VERSION) \
		--tag $(IMAGE):latest \
		--push .

clean: ## Remove caches and generated output
	$(PYTHON) -c "import shutil;[shutil.rmtree(p,ignore_errors=True) for p in ('cad_output','demo-output','.pytest_cache','build','dist')]"
