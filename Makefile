OUT_DIR := dist
SRC_DIR := .

PAGES_DIR := $(SRC_DIR)/pages
PAGES_RST_DIR := $(SRC_DIR)/pages/rst
STYLES_DIR := $(SRC_DIR)/style
JS_DIR := $(SRC_DIR)/src
TPL_DIR := $(SRC_DIR)/tpl
GENERATOR_DIR := $(SRC_DIR)/generator

PYTHON := python3

# this ensures `all` is run by default despite not being the first target in the Makefile
.DEFAULT_GOAL := all

# rule to check for python dependency
validate_python:
	$(if \
		$(shell which $(PYTHON)),\
		$(info Python located at $(shell command -v $(PYTHON))),\
		$(error Python not found in PATH!))

# source files
SRCS_HTML := $(shell find $(PAGES_DIR) -name "*.html")
SRCS_RST := $(shell find $(PAGES_RST_DIR) -name "*.rst")
SRCS_CSS := $(shell find $(STYLES_DIR) -name "*.css")
SRCS_JS := $(shell find $(JS_DIR) -name "*.js")

# create lists of transpiled files
GEN_HTML := $(SRCS_HTML:$(PAGES_DIR)/%=$(OUT_DIR)/%)
GEN_RST := $(SRCS_RST:$(PAGES_RST_DIR)/%.rst=$(OUT_DIR)/articles/%.html)
GEN_CSS := $(SRCS_CSS:$(STYLES_DIR)/%=$(OUT_DIR)/css/%)
GEN_JS := $(SRCS_JS:$(JS_DIR)/%=$(OUT_DIR)/js/%)

# build everything by default
all: $(GEN_HTML) $(GEN_RST) $(GEN_CSS) $(GEN_JS) $(OUT_DIR)/robots.txt

# copy the base article.html for each RST document and expand it
$(OUT_DIR)/articles/%.html: $(PAGES_RST_DIR)/%.rst $(TPL_DIR)/*.j2 | $(OUT_DIR) validate_python
	$(PYTHON) $(GENERATOR_DIR)/translate.py -r -b="$(TPL_DIR)/article.j2" "$<" > "$@"
	$(PYTHON) $(GENERATOR_DIR)/translate.py -i -t="$(TPL_DIR)" "$@"

# template each HTML file
$(OUT_DIR)/%.html: $(PAGES_DIR)/%.html $(PAGES_RST_DIR)/*.rst $(TPL_DIR)/*.j2 | $(OUT_DIR) validate_python
	$(PYTHON) $(GENERATOR_DIR)/translate.py -t="$(TPL_DIR)" "$<" > "$@"

# copy CSS
$(OUT_DIR)/css/%.css: $(STYLES_DIR)/%.css | $(OUT_DIR)
	cp "$<" "$@"

# copy JS
$(OUT_DIR)/js/%.js: $(JS_DIR)/%.js | $(OUT_DIR)
	cp "$<" "$@"

# copy robots.txt
$(OUT_DIR)/robots.txt: robots.txt
	cp "$<" "$@"

# directories
$(OUT_DIR): $(OUT_DIR)/articles $(OUT_DIR)/css $(OUT_DIR)/js

$(OUT_DIR)/articles:
	mkdir -p $@
$(OUT_DIR)/css:
	mkdir -p $@
$(OUT_DIR)/js:
	mkdir -p $@
