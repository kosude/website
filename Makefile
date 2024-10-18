OUT_DIR := dist
SRC_DIR := .

PAGES_DIR := $(SRC_DIR)/pages
PAGES_RST_DIR := $(SRC_DIR)/pages/rst
STYLES_DIR := $(SRC_DIR)/style
TPL_DIR := $(SRC_DIR)/tpl

PYTHON := python3

# this ensures `all` is run by default despite not being the first target in the Makefile
.DEFAULT_GOAL := all

# rules to check for dependencies

validate_python:
	$(if \
		$(shell which $(PYTHON)),\
		$(info Python located at $(shell command -v $(PYTHON))),\
		$(error Python not found in PATH!))

# create list of templated HTML pages and other copied files
GEN_HTML := $(subst pages,dist,$(shell find $(PAGES_DIR) -name "*.html"))
GEN_RST := $(subst .rst,.html,$(subst pages/rst,dist/articles,$(shell find $(PAGES_RST_DIR) -name "*.rst")))
GEN_CSS := $(subst style,dist,$(shell find $(STYLES_DIR) -name "*.css"))

all: $(GEN_HTML) $(GEN_RST) $(GEN_CSS)

$(OUT_DIR):
	mkdir -p $(OUT_DIR)/articles

# copy the base article.html for each RST document and expand it
$(OUT_DIR)/articles/%.html: $(PAGES_RST_DIR)/%.rst $(TPL_DIR)/*.j2 | $(OUT_DIR) validate_python
	$(PYTHON) $(SRC_DIR)/gen/translate.py -r -b="$(TPL_DIR)/article.j2" "$<" > "$@"
	$(PYTHON) $(SRC_DIR)/gen/translate.py -i -t="$(TPL_DIR)" "$@"

# template each HTML file
$(OUT_DIR)/%.html: $(PAGES_DIR)/%.html $(PAGES_RST_DIR)/*.rst $(TPL_DIR)/*.j2 | $(OUT_DIR) validate_python
	$(PYTHON) $(SRC_DIR)/gen/translate.py -t="$(TPL_DIR)" "$<" > "$@"

# copy CSS
$(OUT_DIR)/%.css: $(STYLES_DIR)/%.css | $(OUT_DIR)
	cp "$<" "$@"
