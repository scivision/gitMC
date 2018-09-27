#!/usr/bin/env python
"""
mass create repos for teams
"""
import pandas
from gitutils.github_base import repo_exists, check_api_limit, connect_github
from pathlib import Path
import warnings
from argparse import ArgumentParser


def main():
    p = ArgumentParser()
    p.add_argument('fn', help='.xlsx with group info')
    p.add_argument('oauth', help='Oauth file')
    p.add_argument('-stem', help='beginning of repo names', default='')
    p.add_argument('-orgname', help='Github Organization')
    p = p.parse_args()

    fn = Path(p.fn).expanduser()

    teams = pandas.read_excel(fn, index_col=0, usecols="C, D, F").dropna()
    teams['TEAM #'] = teams['TEAM #'].astype(int)
# %%
    op, sess = connect_github(p.oauth, p.orgname)

    for teamname, row in teams.iterrows():
        if not check_api_limit(sess):
            raise RuntimeError('GitHub API limit exceeded')

        reponame = f'{p.stem}{row["TEAM #"]:02d}-{teamname}'

        exists = repo_exists(op, reponame)
        if not exists:
            print('creating', reponame)
            op.create_repo(name=reponame, private=True)

        repo = op.get_repo(reponame)
        username = row['Github']

        if not repo.has_in_collaborators(username):
            try:
                repo.add_to_collaborators(username)
                print(f'{username} invited to {reponame}')
            except Exception:
                warnings.warn(f'failed to invite {username} to {reponame}')


if __name__ == '__main__':
    main()
