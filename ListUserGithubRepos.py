#!/usr/bin/env python
"""
List all GitHub repos of a user / organization

Without Oauth, you will only see public repos
"""
from argparse import ArgumentParser
import gitutils.github_base as gb


def main():
    p = ArgumentParser(description='List user/organization repos')
    p.add_argument('user', help='GitHub username / organizations')
    p.add_argument('oauth', help='Oauth filename', nargs='?')
    P = p.parse_args()

# %% authentication
    sess = gb.github_session(P.oauth)

    gb.check_api_limit(sess)
# %% prepare to loop over repos
    repos = gb.get_repos(sess, P.user)
    if not repos:
        raise SystemExit(f'no repos for {P.user}')

    for repo in repos:
        print(repo.name)


if __name__ == '__main__':
    main()
