# ---------------------------------------------------------
# Misc.
# ---------------------------------------------------------

# Use Bash as the default shell.
SHELL := /bin/bash

# Set the default Make target.
.DEFAULT_GOAL := tests

# Normalize the workspace path and expose it to Docker Compose.
WORKSPACE ?= $(CURDIR)
MCP_SERVER_WORKSPACE := $(abspath $(WORKSPACE))
export MCP_SERVER_WORKSPACE

# Tell Docker Compose to use Bake for builds.
export COMPOSE_BAKE := true

# Set the Docker Compose profile.
DOCKER_COMPOSE_PROFILE ?= all

# Centralize the Docker Compose command.
COMPOSE := docker compose --profile $(DOCKER_COMPOSE_PROFILE)

# Set the Docker Compose service.
MCP_SERVER := {{ cookiecutter.project_slug }}

# Get service configuration from Docker Compose.
BUILD_CONTEXT := $(shell $(COMPOSE) config --format json | \
	yq -r '.services."$(MCP_SERVER)".build.context')
IMAGE_REF := $(shell $(COMPOSE) config --format json | \
	yq -r '.services."$(MCP_SERVER)".image')

# Set artifact paths.
DOCKERFILE_PATH := $(BUILD_CONTEXT)/Dockerfile
SBOM_PATH := $(MCP_SERVER)-sbom.json
VEX_YAML_PATH := $(BUILD_CONTEXT)/vex.yaml
VEX_JSON_PATH := $(BUILD_CONTEXT)/vex.json

# Set VEX metadata.
VEX_AUTHOR ?= {{ cookiecutter.author }}
VEX_ID_BASE ?= {{ cookiecutter.project_slug }}

# Set scanner configuration and thresholds.
SEMGREP_CONFIG ?= auto
HADOLINT_FAILURE_THRESHOLD ?= warning
GRYPE_FAILURE_THRESHOLD ?= medium

# ---------------------------------------------------------
# Validate the workspace directory exists.
# ---------------------------------------------------------

.PHONY: validate-workspace
.SILENT: validate-workspace
validate-workspace:
	if [ ! -d "$(MCP_SERVER_WORKSPACE)" ]; then \
		echo "ERROR: $(MCP_SERVER_WORKSPACE) does not exist" >&2; \
		exit 1; \
	fi

# ---------------------------------------------------------
# Update uv.lock.
# ---------------------------------------------------------

.PHONY: lock
.SILENT: lock
lock:
	echo "[*] Locking $(MCP_SERVER) Python dependencies"
	cd "$(BUILD_CONTEXT)" && uv lock

# ---------------------------------------------------------
# Check the source code for quality.
# ---------------------------------------------------------

.PHONY: check
.SILENT: check
check:
	echo "[*] Checking $(MCP_SERVER) source code quality"
	ruff check --fix "$(BUILD_CONTEXT)"

# ---------------------------------------------------------
# Format the source code.
# ---------------------------------------------------------

.PHONY: format
.SILENT: format
format:
	echo "[*] Formatting $(MCP_SERVER) source code"
	ruff format "$(BUILD_CONTEXT)"

# ---------------------------------------------------------
# Check the repository for secrets.
# ---------------------------------------------------------

.PHONY: secrets
.SILENT: secrets
secrets:
	echo "[*] Scanning the $(MCP_SERVER) source code for secrets"
	trufflehog \
		--no-update \
		--fail \
		--fail-on-scan-errors \
		--results=verified,unknown \
		--log-level=-1 \
		git "file://$(MCP_SERVER_WORKSPACE)"

# ---------------------------------------------------------
# Check the Dockerfile for quality.
# ---------------------------------------------------------

.PHONY: dockerfile-lint
.SILENT: dockerfile-lint
dockerfile-lint:
	echo "[*] Checking the $(MCP_SERVER) Dockerfile for quality"
	hadolint \
		--failure-threshold "$(HADOLINT_FAILURE_THRESHOLD)" \
		"$(DOCKERFILE_PATH)"

# ---------------------------------------------------------
# Check the source code for vulnerabilities.
# ---------------------------------------------------------

.PHONY: sast
.SILENT: sast
sast:
	echo "[*] Checking the $(MCP_SERVER) source code for vulnerabilities"
	semgrep scan --config "$(SEMGREP_CONFIG)" "$(BUILD_CONTEXT)"

# ---------------------------------------------------------
# Build the container image.
# ---------------------------------------------------------

.PHONY: build-containers
.SILENT: build-containers
build-containers: lock check format secrets dockerfile-lint sast
	echo "[*] Building the $(MCP_SERVER) container image"
	$(COMPOSE) build $(MCP_SERVER)

# ---------------------------------------------------------
# Generate a VEX file for the container image.
# ---------------------------------------------------------

define VEX_FILTER
{
  "@context": "https://openvex.dev/ns/v0.2.0",
  "@id": strenv(VEX_ID),
  "author": strenv(VEX_AUTHOR),
  "timestamp": strenv(VEX_TIMESTAMP),
  "version": 1,
  "statements": [
    .advisories[] | {
      "vulnerability": {
        "name": .vulnerability
      },
      "products": [
        .products[] | {
          "@id": .
        }
      ],
      "status": .status,
      "justification": .justification,
      "impact_statement": .impact_statement
    }
  ]
}
endef

export VEX_FILTER

.PHONY: vex
.SILENT: vex
vex:
	echo "[*] Generating VEX for $(MCP_SERVER)"
	VEX_ID="$(VEX_ID_BASE)" \
	VEX_AUTHOR="$(VEX_AUTHOR)" \
	VEX_TIMESTAMP="$$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
	yq -o=json "$$VEX_FILTER" "$(VEX_YAML_PATH)" > "$(VEX_JSON_PATH)"

# ---------------------------------------------------------
# Generate an SBOM for the container image.
# ---------------------------------------------------------

.PHONY: sbom
.SILENT: sbom
sbom: build-containers
	echo "[*] Generating SBOM for $(MCP_SERVER)"
	syft "$(IMAGE_REF)" -o cyclonedx-json="$(SBOM_PATH)"

# ---------------------------------------------------------
# Scan the container image's dependencies for CVEs.
# ---------------------------------------------------------

.PHONY: dependency-scan
.SILENT: dependency-scan
dependency-scan: sbom vex
	echo "[*] Updating the Grype vulnerability database"
	grype db update
	echo "[*] Scanning dependencies for $(MCP_SERVER)"
	grype sbom:"$(SBOM_PATH)" \
		--vex "$(VEX_JSON_PATH)" \
		--fail-on "$(GRYPE_FAILURE_THRESHOLD)"

# ---------------------------------------------------------
# Start the containers.
# ---------------------------------------------------------

.PHONY: start-containers
.SILENT: start-containers
start-containers: validate-workspace dependency-scan
	echo "[*] Using workspace: $(MCP_SERVER_WORKSPACE)"
	$(COMPOSE) up -d

# ---------------------------------------------------------
# Stop the containers.
# ---------------------------------------------------------

.PHONY: stop-containers
.SILENT: stop-containers
stop-containers:
	$(COMPOSE) down

# ---------------------------------------------------------
# Check the status of the containers.
# ---------------------------------------------------------

.PHONY: status
.SILENT: status
status:
	$(COMPOSE) ps --format "table {% raw %}{{.Name}}\t{{.Ports}}\t{{.Status}}{% endraw %}"

# ---------------------------------------------------------
# Test the containers.
# ---------------------------------------------------------

.PHONY: tests
.SILENT: tests
tests: start-containers
	echo "[*] Running tests for $(MCP_SERVER)"
	cd tests && uv run python main.py
