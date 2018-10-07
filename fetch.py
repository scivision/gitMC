#!/usr/bin/env python
"""
for a root directory, assumes all subdirectories are Git repos
and "git fetch" each
"""
from gitutils import fetchpull
from argparse import ArgumentParser


def main():
    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    P = p.parse_args()

    fetchpull('fetch', P.codepath)


if __name__ == '__main__':
    main()
