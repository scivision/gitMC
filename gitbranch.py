#!/usr/bin/env python
"""
report on git repos not on the expected branch e.g. 'master'
"""
import subprocess
#
from pygitutils import codepath

def findbranch(ok):
    """find all branches in tree not matching ok"""

    rdir = codepath()

    cmd=['git','rev-parse','--abbrev-ref','HEAD']

    dlist = [x for x in rdir.iterdir() if x.is_dir()]

    branch=[]
    for d in dlist:
        try:
            ret = subprocess.check_output(cmd, cwd=d,
                                          universal_newlines=True).rstrip()

            if not ok in ret:
                branch.append((d,ret))
        except subprocess.CalledProcessError as e:
            print(d,e)

    return branch

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('mainbranch',nargs='?',
                   default='master',help='name of your main branch')
    p = p.parse_args()

    branch = findbranch(p.mainbranch)

    for b in branch:
        print(f'{b[0]} => {b[1]}')
