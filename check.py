#!/usr/bin/env python
"""
for a root directory, assumes all subdirectories are Git repos
and "git fetch --dry-run" each
"""
import logging
from argparse import ArgumentParser

from gitutils.pull import coro_remote
from gitutils.runner import runner

MODE = ['fetch', '--dry-run']


def main():
    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    p.add_argument('-v', '--verbose', action='store_true')
    P = p.parse_args()

    if P.verbose:
        logging.basicConfig(level=logging.DEBUG)

    remotes = runner(coro_remote, MODE, P.codepath)
    print('\n'.join(map(str, remotes)))


if __name__ == '__main__':
    main()
