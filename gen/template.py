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
    parser.add_argument("pagedir",
                        type=str,
                        help="path to HTML page directory")
    parser.add_argument("tpldir",
                        type=str,
                        help="path to templates directory")

    return parser.parse_args()

ARGS = get_args()
INFILE = os.path.basename(ARGS.infile)
OUTFILE = os.path.realpath(ARGS.outfile)
PAGES_DIR = os.path.realpath(ARGS.pagedir)
TPL_DIR = os.path.realpath(ARGS.tpldir)

# directory must exist for the output file
if not os.path.exists(os.path.dirname(OUTFILE)):
    print(f"Error: non-existent parent directory of output file '{OUTFILE}'")
    exit(1)

pages_env = j2.Environment(loader=j2.FileSystemLoader(PAGES_DIR))
tpl_loader = j2.FileSystemLoader(TPL_DIR)

# get template for INFILE to be rendered into OUTFILE
tpl = pages_env.get_template(INFILE)
tpl.environment.loader = tpl_loader # {%include%}'d templates sourced via tpl_loader

res = tpl.render()
with open(OUTFILE, "w", encoding="utf-8") as f:
    f.write(res)
