#!/usr/bin/env python
"""
for a root directory, assumes all subdirectories are Git repos
and "git pull" each of them.
"""
from gitutils.pull import fetchpull
from argparse import ArgumentParser
from gitutils.git import MAGENTA, BLACK


def main():
    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    p.add_argument('-v', '--verbose', action='store_true')
    P = p.parse_args()

    failed = []
    for d, v in fetchpull('pull', P.codepath):
        print(MAGENTA + str(d))
        print(BLACK + v)
        failed.append(d)

    print('\n'.join(map(str, failed)))  # map(str,) needed for Windows


if __name__ == '__main__':
    main()
