#!/usr/bin/env python3
#
#   Copyright (c) 2026 Jack Bennett.
#   All Rights Reserved.
#
#   See the LICENCE file for more information.

# this script isn't meant to be run on its own
if __name__ == "__main__":
    exit(0)

from __rstparse import get_rst_title

import os
import glob

class Article:
    """Class representation of an individual article."""

    def __init__(self):
        # The article's title (first RST heading)
        self.title = ""
        # The article's index (preceeding number in filename)
        self.index = -1
        # Absolute URL to the article
        self.href = ""

def find_articles(dir: str) -> list[Article]:
    """Enumerate all RST articles in `dir` and represent them as Article objects in the returned list."""

    # Note that article filenames must end in .rst (case-sensitive)
    art_filenames = glob.glob("*.rst", root_dir=dir) # each article (relative) filename
    art_filepaths = [os.path.join(dir, n) for n in art_filenames] # path to each article RST file

    ret = []

    indices = []

    for filename, path in zip(art_filenames, art_filepaths):
        a = Article()

        a.title = get_rst_title(path)

        # index is the number before the first underscore
        index_str = filename.split("_", 1)
        try:
            a.index = int(index_str[0])
            # must be positive and 1-indexed
            if a.index <= 0:
                raise Exception
        except:
            raise Exception(f"Invalid article at {path}: filename must start with a integer (> 0) followed by an underscore.")

        # check for duplicate indices - there must be a better way of doing this
        if a.index in indices:
            raise Exception(f"Multiple articles with the same index found (index is {a.index}).")
        indices.append(a.index)

        filename_html = filename.replace(".rst", ".html", 1)
        a.href = f"/articles/{filename_html}"

        ret.append(a)

    ret.sort(key=lambda a: a.index)

    return ret

def render_articles_ul_html(arts: list[Article]) -> str:
    """Render the given list of articles as a HTML ul element for the sidebar."""

    ret = "<ul>"

    for art in arts:
        ret += f"<li style='list-style-type:\"{art.index}   \"'><a href=\"{art.href}\">{art.title}</a></li>"

    ret += "</ul>"

    return ret
