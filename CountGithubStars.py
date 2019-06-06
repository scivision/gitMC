#!/usr/bin/env python
"""
Totals up stars and fork count for all repos of a Github user.
Can use Oauth login if desired.
"""
import pandas as pd
from argparse import ArgumentParser
import gitutils.github_repo_stats as gu
import pandas


def main():
    p = ArgumentParser(description='Totals up stars and fork count for all repos of a Github user.')
    p.add_argument('user', help='Github username')
    p.add_argument('oauth', help='Oauth filename', nargs='?')
    p = p.parse_args()

    counts = gu.repo_prober(p.user, p.oauth, None, True)[0]

    dat = pd.DataFrame([c[1:] for c in counts],
                       index=[c[0] for c in counts],
                       columns=['forks', 'stars'])

    datnz = dat[~(dat == 0).all(axis=1)]
# %%  Stars and Forks
    pd.set_option('display.max_rows', 500)

    print(f'\n{p.user} total stars received {dat["stars"].sum()}')
    print(f'{p.user} total other users forked {dat["forks"].sum()}\n')

    print(datnz.sort_values(['stars', 'forks'], ascending=False))


if __name__ == '__main__':
    main()
