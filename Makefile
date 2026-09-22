TEMPLATE_DIR := .
BUILD_DIR := .test_output

.PHONY: all test clean

all: test

test: clean
	@cookiecutter $(TEMPLATE_DIR) --no-input -o $(BUILD_DIR)
	@TARGET_DIR=$$(ls -d $(BUILD_DIR)/* | head -n 1); \
	$(MAKE) --no-print-directory -C "$$TARGET_DIR"
	@$(MAKE) --no-print-directory clean
	@echo "[+] Test completed and cleaned up."

clean:
	@rm -rf $(BUILD_DIR)
