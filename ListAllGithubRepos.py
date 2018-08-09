#!/usr/bin/env python
"""
lists all repos for a Github user.
Can use Oauth login.
GitHub API is otherwise very limited for unauthenticated users.

The Oauth file should be in a secure place, NOT in a Git repo!
Maybe encrypted and with permissions 600.
The Oauth key should have no checkboxes, so that it's read only for public repos.
"""
import pandas as pd
from argparse import ArgumentParser
import gitutils.github as gu


def main():
    p = ArgumentParser(description='list all Github repos for a particular user')
    p.add_argument('user', help='Github username')
    p.add_argument('oauth', help='Oauth filename', nargs='?')

    P = p.parse_args()
    dat, ahead = gu.repo_prober(P.user, P.oauth)

    datnz = dat[~(dat == 0).all(axis=1)]
# %%
    pd.set_option('display.max_rows', 500)

    print(datnz.sort_values(['stars', 'forks'], ascending=False))

    print(ahead)


if __name__ == '__main__':
    main()
