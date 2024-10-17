OUT_DIR := dist
SRC_DIR := .

PAGES_DIR := $(SRC_DIR)/pages
STYLES_DIR := $(SRC_DIR)/style
TPL_DIR := $(SRC_DIR)/tpl

PYTHON := python

# create list of templated HTML pages and other copied files
GEN_PAGES := $(subst pages,dist,$(shell find $(PAGES_DIR) -name "*.html"))
GEN_STYLES := $(subst style,dist,$(shell find $(STYLES_DIR) -name "*.css"))

all: $(GEN_PAGES) $(GEN_STYLES)

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

# template each HTML file
$(OUT_DIR)/%.html: $(PAGES_DIR)/%.html $(TPL_DIR)/*.j2 | $(OUT_DIR)
	$(TPL_DIR)/expand.py "$<" "$@"

# copy CSS
$(OUT_DIR)/%.css: $(STYLES_DIR)/%.css | $(OUT_DIR)
	cp "$<" "$@"
