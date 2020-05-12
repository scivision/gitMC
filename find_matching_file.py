#!/usr/bin/env python
"""
Finds directories matching specific files.
"""

import argparse

from gitutils.find import find_matching_file


def main():
    p = argparse.ArgumentParser()
    p.add_argument("fn", help="filename to look for")
    p.add_argument("path", help="root path to search under", nargs="?", default=".")
    P = p.parse_args()

    for f in find_matching_file(P.fn, P.path):
        print(f)


if __name__ == "__main__":
    main()
