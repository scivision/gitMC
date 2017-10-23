#!/usr/bin/env python
"""
Finds directories without .gitattributes 
can also be used to find directories missing other specific files.
"""
from sys import stderr
from pathlib import Path
import shutil


def find_dir_missing_file(fn:str,path:Path, copyfile:Path=None) -> list:
    path = Path(path).expanduser()
    
    dlist = [x for x in path.iterdir() if x.is_dir()]
    
    missing = []
    for d in dlist:
        if not (d/fn).is_file():
            if copyfile:
                shutil.copy(copyfile, d)
                print(f'copied {copyfile} to {d}')
            else:
                missing.append(d)
            
    return missing


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('fn',help='filename to look for')
    p.add_argument('path',help='root path to search under',nargs='?',default='.')
    p.add_argument('-c','--copy',help='filepath to copy in if missing')
    p = p.parse_args()
    
    missing = find_dir_missing_file(p.fn, p.path, p.copy)

    if missing:
        print(f'{[str(m) for m in missing]}',file=stderr)
