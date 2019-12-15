#!/usr/bin/env python
"""
Finds directories missing other specific files.
"""
from pathlib import Path
from sys import stderr
import argparse

from gitutils.find import find_dir_missing_file


def main():
    p = argparse.ArgumentParser()
    p.add_argument("fn", help="filename to look for")
    p.add_argument("path", help="root path to search under", nargs="?", default=".")
    p.add_argument("-c", "--copy", help="filepath to copy in if missing")
    P = p.parse_args()

    filedest = Path(P.copy).expanduser() if P.copy else None

    for f in find_dir_missing_file(P.fn, P.path, filedest):
        print(f, file=stderr)


if __name__ == "__main__":
    main()
