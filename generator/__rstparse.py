#   Copyright (c) 2026 Jack Bennett.
#   All Rights Reserved.
#
#   See the LICENCE file for more information.

# this script isn't meant to be run on its own
if __name__ == "__main__":
    exit(0)

from docutils import frontend
from docutils import nodes
from docutils import utils
from docutils.core import publish_parts
from docutils.parsers import rst
from docutils.writers import html4css1

import re

class HTMLTranslator(html4css1.HTMLTranslator):
    """A lot of methods are provided in this class which can be overriden for hacking docutils:
       see https://github.com/docutils/docutils/blob/master/docutils/docutils/writers/_html_base.py"""

    ...

class HTMLWriter(html4css1.Writer):
    """HTML writer class that uses the customised translator type."""

    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = HTMLTranslator

# global reused docutils state objects
parser = rst.Parser()
parser_settings = frontend.OptionParser((rst.Parser,)).get_default_values()
writer = HTMLWriter()
writer_setting_overrides = {"initial_header_level": 2}

def _parse_rst(path: str) -> nodes.document:
    """Parse the given RST file into a docutils tree (document) object."""

    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    document = utils.new_document("<>", parser_settings)
    parser.parse(src, document) # populates document with parsed nodes
    return document

# regex statements to match toplevel document tags
# (to be removed as they are not necessary here)
DOCDIV_OPEN_RE = re.compile(r"<div class=\"document\"(?: id=\".*\")?>\n")
DOCDIV_CLOSE_RE = re.compile(r"</div>\n$")

def render_rst_file_html(path: str) -> str:
    """Render the provided RST file into a HTML string."""

    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    parts = publish_parts(src, writer=writer, settings_overrides=writer_setting_overrides)
    body = parts["html_body"]

    # we remove the surrounding <div> element that docutils creates, since it is redundant.
    # doing this by overriding a function in the writer class seems really (unnecessarily) complicated
    # so this hack is the next best thing
    ret = re.sub(DOCDIV_OPEN_RE, "", body)
    ret = re.sub(DOCDIV_CLOSE_RE, "", ret)

    return ret

def get_rst_title(path: str) -> str:
    """Get the first top-most heading in the specified RST file - taken to be the article's title."""

    doc = _parse_rst(path)

    # enumerate all section headings in the document
    # TODO: currently getting all then discarding - could this be optimised?
    sect_titles = [s.next_node(nodes.title).astext() for s in doc.findall(nodes.section)]

    if len(sect_titles) < 1:
        raise Exception(f"RST article at {path} missing a top-level heading")

    return sect_titles[0]
