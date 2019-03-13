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
from typing import Sequence
from argparse import ArgumentParser

from gitutils import gitemail
from gitutils.git import MAGENTA, BLACK

cwd = Path(__file__).parent
github = '@users.noreply.github.com'


def amend(path: Path, emails: Sequence[str], user: str):
    assert isinstance(user, str)

    for email in emails:
        if email != user + github:
            cmd = [str(cwd / 'amender.sh'), email, user]
            subprocess.check_call(cmd, cwd=path)


def main():
    p = ArgumentParser()
    p.add_argument('path', help='path to Git repo', nargs='?', default='.')
    p.add_argument('-e', '--exclude', help='user to ignore (keep)')
    p.add_argument('-a', '--amend', help='change all non-exclused commits to username')
    p = p.parse_args()

    for d, emails in gitemail(p.path, p.exclude):

        if p.amend:
            amend(d, emails, p.amend)

        print(MAGENTA + d.stem + BLACK)
        for email in emails:
            print(*email)


if __name__ == '__main__':
    main()
