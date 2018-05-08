#!/usr/bin/env python
"""
detects uncommitted work/files in all git repos under a directory
"""
from pygitutils import gitpushall

if __name__ == '__main__':
    from argparse import ArgumentParser

    p = ArgumentParser()
    p.add_argument('codepath',help='path to code root', nargs='?', default='~/code')
    p = p.parse_args()

    dir_topush = gitpushall(p.codepath,True)
