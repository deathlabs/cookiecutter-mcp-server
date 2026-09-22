# ---------------------------------------------------------
# Misc.
# ---------------------------------------------------------

.DEFAULT_GOAL := build
TEMPLATE_DIR := .
BUILD_DIR := build
TEMP_DIR := test

# ---------------------------------------------------------
# Build a new project.
# ---------------------------------------------------------

.PHONY: build
.SILENT: build
build: clean
	cookiecutter $(TEMPLATE_DIR) --no-input -o $(BUILD_DIR)
	TARGET_DIR=$$(ls -d $(BUILD_DIR)/* | head -n 1) &&\
	$(MAKE) --no-print-directory -C "$$TARGET_DIR" &&\
	$(MAKE) --no-print-directory -C "$$TARGET_DIR" stop-container &&\
	$(MAKE) --no-print-directory -C "$$TARGET_DIR" remove-container &&\
	$(MAKE) --no-print-directory -C "$$TARGET_DIR" remove-container-image 

# ---------------------------------------------------------
# Test the cookiecutter template.
# ---------------------------------------------------------

.PHONY: test
.SILENT: test
test: 
	cookiecutter $(TEMPLATE_DIR) --no-input -o $(TEMP_DIR)
	TARGET_DIR=$$(ls -d $(TEMP_DIR)/* | head -n 1) &&\
	$(MAKE) --no-print-directory -C "$$TARGET_DIR" &&\
	$(MAKE) --no-print-directory -C "$$TARGET_DIR" stop-container &&\
	$(MAKE) --no-print-directory -C "$$TARGET_DIR" remove-container &&\
	$(MAKE) --no-print-directory -C "$$TARGET_DIR" remove-container-image &&\
	$(MAKE) --no-print-directory clean

# ---------------------------------------------------------
# Clean the build directory.
# ---------------------------------------------------------

.PHONY: clean
.SILENT: clean
clean:
	rm -rf $(TEMP_DIR)
