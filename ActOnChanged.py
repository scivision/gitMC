#!/usr/bin/env python
"""
list changed files and run program on them.
Optionally chop off (fixed width) first part of filename--useful for previewing
all changed files in a static rendered web preview (Jekyll, Hugo)
"""
import webbrowser
from pathlib import Path
from pygitutils import listchanged

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('path', help='git directory to operate on')
    p.add_argument('-j', '--jekyll', help='web browser preview of localhost', action='store_true')
    p = p.parse_args()

    path = Path(p.path).expanduser().resolve()
    flist = listchanged(path)
# %%
    if p.jekyll:
        prefix = 'http://localhost:4000/'

        if path.name == '_posts':
            cut = 11
        else:
            cut = 0
        flist = [prefix + f[cut:].split('.')[0] for f in flist]

        for f in flist:
            webbrowser.open_new_tab(f)
    else:
        flist = (str(path / f) for f in flist)
        print('\n'.join(flist))
