#!/usr/bin/env python
"""
report on git repos not on the expected branch e.g. 'master'
"""
import subprocess
#
from pygitutils import findbranch

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('codepath',help='path to code root', nargs='?', default='~/code')
    p.add_argument('mainbranch',nargs='?',
                   default='master',help='name of your main branch')
    p = p.parse_args()

    branch = findbranch(p.mainbranch, p.codepath)

    for b in branch:
        print(b[0],' => ',b[1])
