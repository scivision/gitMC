#!/usr/bin/env python
"""
detects uncommitted work/files in all git repos under a directory
"""
from argparse import ArgumentParser
from gitutils import gitpushall


def main():
    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    p.add_argument('-v', '--verbose', action='store_true')
    P = p.parse_args()

    print('\n'.join(map(str, gitpushall(P.codepath, P.verbose))))


if __name__ == '__main__':
    main()
