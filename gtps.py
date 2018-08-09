#!/usr/bin/env python
"""
detects uncommitted work/files in all git repos under a directory
"""
from argparse import ArgumentParser
from gitutils import gitpushall


def main():
    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    P = p.parse_args()

    gitpushall(P.codepath, True)


if __name__ == '__main__':
    main()
