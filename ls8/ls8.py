#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
if len(sys.argv) != 2:
    print("usage: comp.py filename")
    sys.exit(1)
progname = sys.argv[1]
cpu.load(progname)
cpu.run()