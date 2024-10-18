#!/usr/bin/env python3
#
#   Copyright (c) 2024 Jack Bennett.
#   All Rights Reserved.
#
#   See the LICENCE file for more information.

import argparse
import os
from __rstparse import parse_rst_file

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("base",
                        type=str,
                        help="base file to copy and insert the RST tree into")
    parser.add_argument("rst",
                        type=str,
                        help="path to RST file")
    parser.add_argument("outfile",
                        type=str,
                        help="path to output HTML file")

    return parser.parse_args()

ARGS = get_args()
BASEFILE = os.path.realpath(ARGS.base)
RSTFILE = os.path.realpath(ARGS.rst)
OUTFILE = os.path.realpath(ARGS.outfile)

# directory must exist for the output file
if not os.path.exists(os.path.dirname(OUTFILE)):
    print(f"Error: non-existent parent directory of output file '{OUTFILE}'")
    exit(1)

(rst_title, rst_html) = parse_rst_file(RSTFILE)

# copy the base file to the output location with inserted RST function call
f = open(BASEFILE, "r")
datasrc = f.read()
f.close()
datadst = datasrc.replace("{@{RST_PUT}@}", rst_html)
datadst = datadst.replace("{@{RST_TITLE}@}", f"{rst_title} - Jack Bennett")
f = open(OUTFILE, "w")
f.write(datadst)
f.close()
