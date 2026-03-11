#!/usr/bin/env python3
#
#   Copyright (c) 2024 Jack Bennett.
#   All Rights Reserved.
#
#   See the LICENCE file for more information.

from __artget import find_articles
from __j2env import setup_jinja2_env
from __rstparse import render_rst_file_html, get_rst_title

import argparse
import jinja2 as j2
import os

# configure and parse CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("input",
                    type=str,
                    help="path to input template (or RST if -r specified)")
parser.add_argument("-r",
                    dest="rst",
                    help="specify the input file to be RST",
                    action="store_true")
parser.add_argument("-i",
                    dest="in_place",
                    help="edit the input file in-place",
                    action="store_true")
parser.add_argument("-t",
                    dest="tpldir",
                    type=str,
                    help="path to templates directory for import resolutions")
parser.add_argument("-s",
                    dest="staticdir",
                    type=str,
                    help="path to static files directory")
parser.add_argument("-a",
                    dest="artdir",
                    type=str,
                    help="path to article RST directory")
parser.add_argument("-b",
                    dest="base",
                    type=str,
                    help="path to base HTML to populate with RST - required if -r is specified")
args = parser.parse_args()

# validate conditionally required arguments
if args.rst == True and args.base == None:
    parser.error("When -r is specified, -b is required")
    exit(1)

# TODO: validate required (if not rst) -a and -s flags

INFILE = os.path.realpath(args.input)

# function to output the final value depending on presence of the -i flag
def write_and_exit(ret):
    if not args.in_place:
        print(ret)
        exit(0)

    # in-place editing is enabled
    with open(INFILE, "w", encoding="utf-8") as f:
        f.write(ret)
        exit(0)

if args.rst:
    # if --rst is specified then we interpret INFILE as reStructuredText and translate it into HTML based on base (-b)

    BASEFILE = os.path.realpath(args.base)

    rst_html = render_rst_file_html(INFILE)
    rst_title = get_rst_title(INFILE)

    # get the base file contents and insert the RST-HTML translation
    f = open(BASEFILE, "r")
    datasrc = f.read()
    f.close()

    datasrc = datasrc.replace("{@{RST_PUT}@}", rst_html)
    datasrc = datasrc.replace("{@{RST_TITLE}@}", rst_title)

    write_and_exit(datasrc)
else:
    # if --rst is not specified we interpret INFILE as jinja2 and expand it

    FS_DIR = os.path.dirname(INFILE)
    TPL_NAME = os.path.basename(INFILE)

    # TODO: articles and env don't change between invocations, and are expensive to get - can they be cached?
    articles = find_articles(os.path.realpath(args.artdir))
    env = setup_jinja2_env(FS_DIR, args.staticdir, articles)

    tpl = env.get_template(TPL_NAME)

    # enable other template loading if -t was specified
    if args.tpldir != None:
        tpldir = os.path.realpath(args.tpldir)
        tpl.environment.loader = j2.FileSystemLoader(tpldir)

    ret = tpl.render()

    write_and_exit(ret)
