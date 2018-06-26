#!/usr/bin/env python
"""
sets core.fileMode=false for git repos
mostly for Windows, particularly Cygwin
"""
from pathlib import Path
from subprocess import call
from argparse import ArgumentParser, Namespace


def cmdparse() -> Namespace:

    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    return p.parse_args()


def main(p: Namespace):
    rdir = Path(p.codepath).expanduser()

    dlist = [x for x in rdir.iterdir() if x.is_dir()]

    print('setting fileMode=false for', len(dlist), 'directories under', rdir)

    for d in dlist:
        call(['git', 'config', 'core.filemode', 'false'], cwd=d)


if __name__ == '__main__':
    main(cmdparse())
