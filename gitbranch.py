#!/usr/bin/env python
"""
report on git repos not on the expected branch e.g. 'master'
"""
import subprocess as S
#
from pygitutils import codepath

def findbranch(ok):

    rdir = codepath()

    cmd=['git','rev-parse','--abbrev-ref','HEAD']

    dlist = [x for x in rdir.iterdir() if x.is_dir()]

    branch=[]
    for d in dlist:
        try:
            ret = S.check_output(cmd,  cwd=d).decode('utf8').rstrip() #stderr=S.DEVNULL,

            if not ok in ret:
                branch.append((d,ret))
        except S.CalledProcessError as e:
            print(d,e)

    return branch

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('mainbranch',nargs='?',
                   default='master',help='name of your main branch')
    p = p.parse_args()

    branch = findbranch(p.mainbranch)

    for b in branch:
        print(f'{b[0]} => {b[1]}')
