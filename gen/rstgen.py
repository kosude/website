#!/usr/bin/env python3
#
#   Copyright (c) 2024 Jack Bennett.
#   All Rights Reserved.
#
#   See the LICENCE file for more information.

import argparse
import os

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

# string which will be inserted into the file, to then be evaluated with template.py
funcstr = "{{ " + f"rstfile(\"{RSTFILE}\")" + " }}"

# copy the base file to the output location with inserted RST function call
f = open(BASEFILE, "r")
datasrc = f.read()
f.close()
datadst = datasrc.replace("{@{RST_PUT}@}", funcstr)
f = open(OUTFILE, "w")
f.write(datadst)
f.close()
