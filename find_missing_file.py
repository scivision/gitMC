#!/usr/bin/env python
"""
Finds directories without .gitattributes 
can also be used to find directories missing other specific files.
"""
from sys import stderr
from pygitutils import find_dir_missing_file

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('fn',help='filename to look for')
    p.add_argument('path',help='root path to search under',nargs='?',default='.')
    p.add_argument('-c','--copy',help='filepath to copy in if missing')
    p = p.parse_args()
    
    missing = find_dir_missing_file(p.fn, p.path, p.copy)

    if missing:
        print(f'{[str(m) for m in missing]}',file=stderr)
