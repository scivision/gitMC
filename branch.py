#!/usr/bin/env python
"""
report on git repos not on the expected branch e.g. 'master'
"""
from argparse import ArgumentParser
import logging
from gitutils.branch import coro_local
from gitutils.runner import runner


def main():
    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    p.add_argument('mainbranch', nargs='?',
                   default='master', help='name of your main branch')
    p.add_argument('-v', '--verbose', action='store_true')
    P = p.parse_args()

    if P.verbose:
        logging.basicConfig(level=logging.DEBUG)

    branches = runner(coro_local, P.mainbranch, P.codepath)
    for b in branches:
        print(b[0], ' => ', b[1])


if __name__ == '__main__':
    main()
