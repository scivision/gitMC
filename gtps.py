#!/usr/bin/env python
"""
detects uncommitted work/files in all git repos under a directory
"""
from __future__ import print_function
from sys import stderr
import subprocess as S
from colorama import init,Fore,Back
#
from pygitutils import codepath

def gitpushall(rdir,verbose=False):
    dlist = [x for x in rdir.iterdir() if x.is_dir()]

    dir_topush = []
    for d in dlist:
        if (d/'.nogit').is_file(): #user requesting this directory not to be synced
            continue

        dpath = detectchange(d,verbose)
        if dpath:
            dir_topush.append(dpath)

    return dir_topush

def detectchange(d,verbose=False):
    dpath = None # in case error
    c= ['git','status','--porcelain'] # uncommitted or changed files
    try:
        ret = S.check_output(c, cwd=str(d)) #stderr=S.DEVNULL,
        if ret:
            dpath = d
            if verbose:
                print(Back.MAGENTA + str(d))
                print(Back.BLACK + ret.decode('utf8'))
    except S.CalledProcessError as e:
        print('Error in',d,e.output, file=stderr)

    return dpath

# replaced by git status --porcelain
#['git','ls-files','-o','-d','--exclude-standard']): # check for uncommitted files
#['git','--no-pager','diff','HEAD'], # check for uncommitted work
# DOES NOT WORK ['git','log','--branches','--not','--remotes'],     # check for uncommitted branches

if __name__ == '__main__':
    rdir = codepath()
    dir_topush = gitpushall(rdir,True)
