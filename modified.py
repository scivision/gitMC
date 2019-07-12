#!/usr/bin/env python
"""
detects uncommitted work/files in all git repos under a directory
"""
import logging
from argparse import ArgumentParser
from gitutils.push import coro_local
from gitutils.runner import runner
from gitutils.git import MAGENTA, BLACK


def main():
    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    p.add_argument('-v', '--verbose', action='store_true')
    P = p.parse_args()

    if P.verbose:
        logging.basicConfig(level=logging.DEBUG)

    changes = runner(coro_local, P.codepath)

    c = MAGENTA if P.verbose else ''

    for d, v in changes:
        print(c + str(d))
        if P.verbose:
            print(BLACK + v)


if __name__ == '__main__':
    main()
