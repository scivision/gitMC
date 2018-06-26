#!/usr/bin/env python
"""
report author emails for all repos under root.
Important for being sure your contributions are plotted in Github (non-registered emails do not plot).

To keep email privacy, use githubusername@users.noreply.github.com

%ae author email doesn't matter to github graph

iterates command
git log --pretty="%ce"  | sort | uniq

EXAMPLE:
gitemail.py scivision ~/code -r

"""
from pathlib import Path
import subprocess
from pygitutils import gitemail
from typing import List
from argparse import ArgumentParser, Namespace
#
cwd = Path(__file__).parent
github = '@users.noreply.github.com'


def amend(path: Path, emails: List[str], user: str):
    assert isinstance(user, str)

    for email in emails:
        if email != user + github:
            cmd = [str(cwd / 'amender.sh'), email, user]
            subprocess.check_call(cmd, cwd=path)


def cmdparse() -> Namespace:
    p = ArgumentParser()
    p.add_argument('user', help='desired Github username', nargs='?')
    p.add_argument('path', help='path to Git repo', nargs='?', default='.')
    p.add_argument('-r', '--recurse', help='recurse', action='store_true')
    p.add_argument('-e', '--exclude', help='users to ignore (keep)', nargs='+')
    p.add_argument('-a', '--amend', help='change all non-exclused commits to username', action='store_true')
    return p.parse_args()


def main(p: Namespace):
    path = Path(p.path).expanduser()

    dlist = [d for d in path.iterdir() if (d / '.git').is_dir()] if p.recurse else [path]

    for d in dlist:
        emails = gitemail(d, p.user, p.exclude)
        if p.user and p.amend and emails is not None:
            amend(d, emails, p.user)


if __name__ == '__main__':
    main(cmdparse())
