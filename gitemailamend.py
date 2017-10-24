#!/usr/bin/env python
"""
report author emails for all repos under root.
Important for being sure your contributions are plotted in Github (non-registered emails do not plot).

To keep email privacy, use githubusername@users.noreply.github.com

%ae author email doesn't matter to github graph

iterates command
git log --pretty="%ce"  | sort | uniq
"""
import sys
from pathlib import Path
import subprocess
from pygitutils import gitemail
sys.tracebacklimit=1
#
cwd = Path(__file__).parent
github = '@users.noreply.github.com'

def amend(path:Path, emails:list, user:str):
    assert isinstance(user,str)

    for email in emails:
        if email != user + github:
            cmd = [str(cwd/'gitemailamend.sh'), email, user]
            subprocess.check_call(cmd, cwd=path)


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('user',help='desired Github username',nargs='?')
    p.add_argument('-d','--dir',help='path to Git repo', nargs='?',default='.')
    p.add_argument('-r',help='recurse',action='store_true')
    p = p.parse_args()

    path = Path(p.dir).expanduser()

    dlist = [d for d in path.iterdir() if d.is_dir()] if p.r else [path]

    for d in dlist:
        emails = gitemail(d, p.user)
        if p.user:
            amend(d, emails, p.user)


