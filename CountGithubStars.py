#!/usr/bin/env python
"""
Totals up stars and fork count for all repos of a Github user.
Can use Oauth login if desired.
"""
import pandas
from argparse import ArgumentParser
import gitutils.github_repo_stats as gu


def main():
    p = ArgumentParser(description='Totals up stars and fork count for all repos of a Github user.')
    p.add_argument('user', help='Github username / organization name', nargs='+')
    p.add_argument('-i', '--oauth', help='Oauth filename', nargs='?')
    p = p.parse_args()

    dat = pandas.DataFrame(None)

    for u in p.user:
        counts = gu.repo_prober(u, p.oauth, None, True)[0]

        d = pandas.DataFrame([c[1:] for c in counts],
                             index=[c[0] for c in counts],
                             columns=['forks', 'stars'])
        dat = pandas.concat((dat, d))

    datnz = dat[~(dat == 0).all(axis=1)]
# %%  Stars and Forks
    pandas.set_option('display.max_rows', 500)

    print(f'\n{" ".join(p.user)} total stars received {dat["stars"].sum()}')
    print(f'{" ".join(p.user)} total other users forked {dat["forks"].sum()}\n')

    print(datnz.sort_values(['stars', 'forks'], ascending=False))


if __name__ == '__main__':
    main()
