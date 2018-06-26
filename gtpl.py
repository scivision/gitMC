#!/usr/bin/env python
"""
for a root directory $rdir, assumes all subdirectories are Git repos
and pulls to the current branch
"""
from pygitutils import fetchpull
from argparse import ArgumentParser


def main():
    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    P = p.parse_args()

    fetchpull('pull', P.codepath)


if __name__ == '__main__':
    main()
