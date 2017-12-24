#!/usr/bin/env python
"""
list changed files and run program on them.
Optionally chop off (fixed width) first part of filename--useful for previewing 
all changed files in a static rendered web preview (Jekyll, Hugo)
"""
import subprocess
from pathlib import Path

def listchanged(path:Path) -> list:
    ret = subprocess.check_output(['git','ls-files','--modified'],
                                  cwd=path)

    ret = ret.decode('utf8')
    ret = ret.split('\n')
    
    return ret

    
if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('path',help='git directory to operate on')
    p.add_argument('program',help='program to run on modified files',nargs='?')
    p.add_argument('--jekyll',help='enact Firefox preview of local Jekyll preview',action='store_true')
    p = p.parse_args()
    
    path = Path(p.path).expanduser().resolve()
    program = p.program
    
    flist = listchanged(path)
# %%        
    if p.jekyll and not program:
        program='firefox'

    if program:
        if p.jekyll:
            prefix='http://localhost:4000/'
            if path.name == '_posts':
                cut = 11
            else:
                cut = 0
            flist = [prefix + f[cut:].split('.')[0] for f in flist]
        else:
            flist = [path / f for f in flist]
            
        subprocess.run([program] + flist)
    else:
        print('\n'.join(flist))
