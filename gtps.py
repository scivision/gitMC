#!/usr/bin/env python
"""
detects uncommitted work/files in all git repos under a directory
"""
from pathlib import Path
from sys import stderr
import subprocess
from colorama import init,Fore,Back
#
from pygitutils import codepath

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

def detectchange(d,verbose=False):
    c1 = ['git','status','--porcelain'] # uncommitted or changed files
    
    try:
# %% detect uncommitted changes
        ret = subprocess.check_output(c1, cwd=d) 
        dpath = _print_change(ret,d,verbose)
        if dpath is not None: 
            return dpath

# %% detect committed, but not pushed
        c0 = ['git','rev-parse','--abbrev-ref','HEAD'] # get branch name
        branch = subprocess.check_output(c0, cwd=d).decode('utf8')[:-1]
        
        c2 = ['git','diff','--stat',f'origin/{branch}..'] 
        ret = subprocess.check_output(c2, cwd=d)
        dpath = _print_change(ret,d,verbose)
    except subprocess.CalledProcessError as e:
        print('Error in',d,e.output, file=stderr)

    return dpath
    
def _print_change(ret,d,verbose=False):
    dpath = None # in case error
    if ret:
        dpath = d
        if verbose:
            print(Back.MAGENTA + str(d))
            print(Back.BLACK + ret.decode('utf8'))
            
    return dpath

# replaced by git status --porcelain
#['git','ls-files','-o','-d','--exclude-standard']): # check for uncommitted files
#['git','--no-pager','diff','HEAD'], # check for uncommitted work
# DOES NOT WORK ['git','log','--branches','--not','--remotes'],     # check for uncommitted branches

if __name__ == '__main__':
    rdir = codepath()
    dir_topush = gitpushall(rdir,True)
