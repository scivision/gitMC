#!/usr/bin/env python
"""
mass create repos for teams
"""
import pandas
from gitutils.github_base import connect_github, repo_exists, check_api_limit
from pathlib import Path
from argparse import ArgumentParser


def main():
    p = ArgumentParser()
    p.add_argument('fn', help='.xlsx with group info')
    p.add_argument('oauth', help='Oauth file')
    p.add_argument('-stem', help='beginning of repo names', default='')
    p.add_argument('-orgname', help='Github Organization')
    p = p.parse_args()

    fn = Path(p.fn).expanduser()

    teams = pandas.read_excel(fn, index_col=0, usecols="C, D").squeeze().drop_duplicates().dropna().astype(int).to_dict()
# %%
    op, sess = connect_github(p.oauth, p.orgname)

    for teamname, teamnum in teams.items():
        if not check_api_limit(sess):
            raise RuntimeError('GitHub API limit exceeded')

        reponame = f'{p.stem}{teamnum:02d}-{teamname}'

        if repo_exists(op, reponame):
            continue

        print('creating', reponame)
        op.create_repo(name=reponame, private=True)


if __name__ == '__main__':
    main()
