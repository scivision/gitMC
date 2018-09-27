#!/usr/bin/env python
"""
mass create repos for teams
"""
import pandas
from gitutils.github_base import github_session, repo_exists, check_api_limit
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
    sess = github_session(p.oauth)
    guser = sess.get_user()

    org = None
    if p.orgname:
        orgs = list(guser.get_orgs())
        for o in orgs:
            if o.login == p.orgname:
                org = o
                break

        assert org is not None
        op = org
    else:
        op = guser

    for teamname, teamnum in teams.items():
        if not check_api_limit(sess):
            raise RuntimeError('GitHub API limit exceeded')

        reponame = f'{p.stem}{teamnum:02d}-{teamname}'

        exists = repo_exists(op, reponame)
        if exists:
            continue

        print('creating', reponame)
        op.create_repo(name=reponame, private=True)


if __name__ == '__main__':
    main()
