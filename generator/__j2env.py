#!/usr/bin/env python3
#
#   Copyright (c) 2026 Jack Bennett.
#   All Rights Reserved.
#
#   See the LICENCE file for more information.

# this script isn't meant to be run on its own
if __name__ == "__main__":
    exit(0)

from __artget import Article, render_articles_ul_html

import jinja2 as j2
import os

def setup_jinja2_env(fsdir: str, staticdir: str, articles: list[Article]):
    env = j2.Environment(loader=j2.FileSystemLoader(fsdir))

    # used in some custom functions
    global STATICDIR
    STATICDIR = os.path.realpath(staticdir)

    env.globals["readstatic"] = __j2func_readstatic

    env.globals["articlesul"] = render_articles_ul_html(articles)
    env.globals["articlesamt"] = len(articles)

    return env

def __j2func_readstatic(filename):
    f = open(STATICDIR + os.path.sep + filename, "r")
    contents = f.read()
    f.close()

    return contents
