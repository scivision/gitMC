#!/usr/bin/env python
"""
detects uncommitted work/files in all git repos under a directory
"""
from pathlib import Path
from typing import List
from argparse import ArgumentParser
from pygitutils import gitpushall


def main() -> List[Path]:
    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    P = p.parse_args()

    return gitpushall(P.codepath, True)


if __name__ == '__main__':
    main()
