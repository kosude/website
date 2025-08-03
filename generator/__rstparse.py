#   Copyright (c) 2024 Jack Bennett.
#   All Rights Reserved.
#
#   See the LICENCE file for more information.

# this script isn't meant to be run on its own
if __name__ == "__main__":
    exit(0)

from docutils import frontend, nodes
from docutils.parsers.rst import Parser
from docutils.writers import html4css1
from docutils.core import publish_parts

import re

class HTMLTranslator(html4css1.HTMLTranslator):
    def should_be_compact_paragraph(self, node):
        if isinstance(node.parent, nodes.block_quote):
            return 0

        return html4css1.HTMLTranslator.should_be_compact_paragraph(self, node)

    # the original visit_section puts divs everywhere which aren't necessary
    def visit_section(self, node):
        self.section_level += 1

    # same deal for depart_section
    def depart_section(self, node):
        self.section_level -= 1

class HTMLWriter(html4css1.Writer):
    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = HTMLTranslator

settings = frontend.get_default_settings(Parser)

DOCDIV_OPEN_RE = re.compile(r"<div class=\"document\"(?: id=\".*\")?>\n")
DOCDIV_CLOSE_RE = re.compile(r"</div>\n$")

def parse_rst_file(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    parts = publish_parts(src, writer=HTMLWriter())
    body = parts["html_body"]

    # we remove the surrounding <div> element that docutils creates, since it is redundant.
    # doing this by overriding a function in the writer class seems really (unnecessarily) complicated
    # so this hack is the next best thing
    ret = re.sub(DOCDIV_OPEN_RE, "", body)
    ret = re.sub(DOCDIV_CLOSE_RE, "", ret)

    return ret
