#!/usr/bin/env python3
#
#   Copyright (c) 2024 Jack Bennett.
#   All Rights Reserved.
#
#   See the LICENCE file for more information.

import argparse
import jinja2 as j2
import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile",
                        type=str,
                        help="path to file to be templated")
    parser.add_argument("outfile",
                        type=str,
                        help="path to output file")

    return parser.parse_args()

ARGS = get_args()
INFILE = os.path.basename(ARGS.infile)
OUTFILE = os.path.realpath(ARGS.outfile)

# directory must exist for the output file
if not os.path.exists(os.path.dirname(OUTFILE)):
    print(f"Error: non-existent parent directory of output file '{OUTFILE}'")
    exit(1)

PAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "pages")
TPL_DIR = os.path.dirname(os.path.realpath(__file__))

pages_env = j2.Environment(loader=j2.FileSystemLoader(PAGES_DIR))
tpl_loader = j2.FileSystemLoader(TPL_DIR)

# get template for INFILE to be rendered into OUTFILE
tpl = pages_env.get_template(INFILE)
tpl.environment.loader = tpl_loader # {%include%}'d templates sourced via tpl_loader

res = tpl.render()
with open(OUTFILE, "w", encoding="utf-8") as f:
    f.write(res)
