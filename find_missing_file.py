#!/usr/bin/env python
"""
Finds directories without .gitattributes
can also be used to find directories missing other specific files.
"""
from pathlib import Path
from sys import stderr
from gitutils import find_dir_missing_file
from argparse import ArgumentParser


def main():
    p = ArgumentParser()
    p.add_argument('fn', help='filename to look for')
    p.add_argument('path', help='root path to search under', nargs='?', default='.')
    p.add_argument('-c', '--copy', help='filepath to copy in if missing')
    P = p.parse_args()

    filedest = Path(P.copy).expanduser() if P.copy else None

    missing = find_dir_missing_file(P.fn, P.path, filedest)

    if missing:
        print(f'these directories were missing file   {P.fn}')
        print(f'{[str(m) for m in missing]}', file=stderr)


if __name__ == '__main__':
    main()
