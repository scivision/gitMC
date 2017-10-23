#!/usr/bin/env python
"""
sets core.fileMode=false for git repos
mostly for Windows, particularly Cygwin
"""
from subprocess import call
#
from pygitutils import codepath

rdir = codepath()

dlist = [x for x in rdir.iterdir() if x.is_dir()]

print(f'setting fileMode=false for {len(dlist)} directories under {rdir}')

for d in dlist:
    call(['git','config','core.filemode','false'], cwd=d)
