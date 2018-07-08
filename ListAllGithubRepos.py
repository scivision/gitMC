#!/usr/bin/env python
"""
lists all repos for a Github user.
Requires Oauth login because otherwise API is very limited for unauthenticated users.

The Oauth file should be in a secure place, NOT in a Git repo!
Maybe encrypted and with permissions 600.
The Oauth key should have no checkboxes, so that it's read only for public repos.
I'll leave it to you if you trust PyGithub with private repos.
"""
from tabulate import tabulate
import pandas
import numpy as np
from pathlib import Path
from github import Github
from argparse import ArgumentParser


def listall(user: str, oauth: Path) -> pandas.DataFrame:
    oauth = Path(oauth).expanduser()
    g = Github(oauth.read_text().strip())  # no trailing \n allowed

    repos = list(g.get_user().get_repos())
    dat = pandas.DataFrame(np.empty((len(repos), 2), int),
                           index=[r.name for r in repos],
                           columns=['forks', 'stars'])

    for r in repos:
        dat.loc[r.name, :] = (r.forks_count, r.stargazers_count)

    return dat


def main():
    p = ArgumentParser(description='list all Github repos for a particular user')
    p.add_argument('user', help='Github username')
    p.add_argument('oauth', help='Oauth filename')

    P = p.parse_args()
    dat = listall(P.user, P.oauth)

    datnz = dat[~(dat == 0).all(axis=1)]

    print(tabulate(datnz.sort_values(['stars', 'forks'], ascending=False), headers='keys'))


if __name__ == '__main__':
    main()
