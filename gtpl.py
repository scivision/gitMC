#!/usr/bin/env python
"""
for a root directory $rdir, assumes all subdirectories are Git repos
and pulls to the current branch
"""
from pygitutils import fetchpull
from argparse import ArgumentParser

p = ArgumentParser()
p.add_argument('codepath',help='path to code root', nargs='?', default='~/code')
p = p.parse_args()

fetchpull('pull', p.codepath)

