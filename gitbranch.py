#!/usr/bin/env python
"""
report on git repos not on the expected branch e.g. 'master'
"""
import subprocess as S
#
from pygitutils import codepath

def findbranch(ok='master'):

    rdir = codepath()

    cmd=['git','rev-parse','--abbrev-ref','HEAD']

    dlist = [x for x in rdir.iterdir() if x.is_dir()]

    branch=[]
    for d in dlist:
        try:
            ret = S.check_output(cmd,  cwd=str(d)).decode('utf8').rstrip() #stderr=S.DEVNULL,

            if not ok in ret:
                branch.append((d,ret))
        except S.CalledProcessError as e:
            print('{}  {}'.format(d,e))

    return branch

if __name__ == '__main__':

    branch = findbranch()

    for b in branch:
        print('{} => {}'.format(b[0],b[1]))