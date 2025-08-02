OUT_DIR := dist
SRC_DIR := .

PAGES_DIR := $(SRC_DIR)/pages
PAGES_RST_DIR := $(SRC_DIR)/pages/rst
STYLES_DIR := $(SRC_DIR)/style
MEDIA_DIR := $(SRC_DIR)/media
TPL_DIR := $(SRC_DIR)/tpl
GENERATOR_DIR := $(SRC_DIR)/generator

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
GEN_HTML := $(subst pages,$(OUT_DIR),$(shell find $(PAGES_DIR) -name "*.html"))
GEN_RST := $(subst .rst,.html,$(subst pages/rst,$(OUT_DIR)/articles,$(shell find $(PAGES_RST_DIR) -name "*.rst")))
GEN_CSS := $(subst style,$(OUT_DIR),$(shell find $(STYLES_DIR) -name "*.css"))
# GEN_MEDIA := $(subst media,$(OUT_DIR)/media,$(shell find $(MEDIA_DIR) -name "*.png"))

all: $(GEN_HTML) $(GEN_RST) $(GEN_CSS) $(GEN_MEDIA)

$(OUT_DIR):
	mkdir -p $(OUT_DIR)/articles
#	mkdir -p $(OUT_DIR)/media

# copy the base article.html for each RST document and expand it
$(OUT_DIR)/articles/%.html: $(PAGES_RST_DIR)/%.rst $(TPL_DIR)/*.j2 | $(OUT_DIR) validate_python
	$(PYTHON) $(GENERATOR_DIR)/translate.py -r -b="$(TPL_DIR)/article.j2" "$<" > "$@"
	$(PYTHON) $(GENERATOR_DIR)/translate.py -i -t="$(TPL_DIR)" "$@"

# template each HTML file
$(OUT_DIR)/%.html: $(PAGES_DIR)/%.html $(PAGES_RST_DIR)/*.rst $(TPL_DIR)/*.j2 | $(OUT_DIR) validate_python
	$(PYTHON) $(GENERATOR_DIR)/translate.py -t="$(TPL_DIR)" "$<" > "$@"

# copy CSS
$(OUT_DIR)/%.css: $(STYLES_DIR)/%.css | $(OUT_DIR)
	cp "$<" "$@"

# copy media
# $(GEN_MEDIA): $(OUT_DIR)/media/%: $(MEDIA_DIR)/% | $(OUT_DIR)
# 	cp "$<" "$@"
