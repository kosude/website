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
    parser.add_argument("outdir",
                        type=str,
                        help="path to output/dist directory")

    return parser.parse_args()

def abort():
    print("Stopping")
    exit(1)

ARGS = get_args()
OUTDIR = ARGS.outdir

# output directory must exist
if not os.path.exists(OUTDIR):
    print(f"Error: outdir '{OUTDIR}' does not exist on the fs")
    abort()

PAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "pages")
TPL_DIR = os.path.dirname(os.path.realpath(__file__))

print(f"Loading templates from: {TPL_DIR}")
print(f"Rendering pages from: {PAGES_DIR}")

pages_env = j2.Environment(loader=j2.FileSystemLoader(PAGES_DIR))
tpl_loader = j2.FileSystemLoader(TPL_DIR)

for page in pages_env.list_templates():
    outfile = os.path.join(OUTDIR, page)

    pagetpl = pages_env.get_template(page)
    pagetpl.environment.loader = tpl_loader

    res = pagetpl.render()
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(res)

    print(f"\t{page} -> {outfile}")
