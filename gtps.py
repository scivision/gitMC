#!/usr/bin/env python
"""
detects uncommitted work/files in all git repos under a directory
"""
from pathlib import Path
#
from pygitutils import codepath,detectchange

def gitpushall(rdir:Path, verbose:bool=False):
    dlist = [x for x in rdir.iterdir() if x.is_dir()]

    dir_topush = []
    for d in dlist:
        if (d/'.nogit').is_file(): #user requesting this directory not to be synced
            continue

        dpath = detectchange(d,verbose)
        if dpath:
            dir_topush.append(dpath)

    return dir_topush

# replaced by git status --porcelain
#['git','ls-files','-o','-d','--exclude-standard']): # check for uncommitted files
#['git','--no-pager','diff','HEAD'], # check for uncommitted work
# DOES NOT WORK ['git','log','--branches','--not','--remotes'],     # check for uncommitted branches

if __name__ == '__main__':
    rdir = codepath()
    dir_topush = gitpushall(rdir,True)
