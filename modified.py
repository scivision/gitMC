#!/usr/bin/env python
"""
detects uncommitted work/files in all git repos under a directory
"""
from argparse import ArgumentParser
from gitutils import gitpushall
from gitutils.git import MAGENTA, BLACK


def main():
    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    p.add_argument('-v', '--verbose', action='store_true')
    P = p.parse_args()

    c = MAGENTA if P.verbose else ''
    for d, v in gitpushall(P.codepath):
        print(c + str(d))
        if P.verbose:
            print(BLACK + v)


if __name__ == '__main__':
    main()
