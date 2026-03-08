#!/usr/bin/env python3
#
#   Copyright (c) 2026 Jack Bennett.
#   All Rights Reserved.
#
#   See the LICENCE file for more information.

import jinja2 as j2
import os

def setup_jinja2_env(fsdir, staticdir):
    env = j2.Environment(loader=j2.FileSystemLoader(fsdir))

    # used in some custom functions
    global STATICDIR
    STATICDIR = os.path.abspath(staticdir)

    env.globals["readstatic"] = __j2func_readstatic

    return env

def __j2func_readstatic(filename):
    f = open(STATICDIR + os.path.sep + filename, "r")
    contents = f.read()
    f.close()

    return contents
