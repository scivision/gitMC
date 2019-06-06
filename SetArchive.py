#!/usr/bin/env python
"""
Archive GitHub repos for a user/organization with repo names matching pattern

Requires GitHub Oauth login with sufficient permissions "repo:public_repo".
(admin:org Oauth does not work)
It's suggested you create an Oauth key for this, and then disable/delete this key permissions when done
to avoid a security issue.

if you get error

    github.GithubException.UnknownObjectException: 404 {'message': 'Not Found',
    'documentation_url': 'https://developer.github.com/v3/repos/#edit'}

that typically means your Oauth key doesn't have adequte permissions.
"""
from argparse import ArgumentParser
import gitutils.github_base as gb


def main():
    p = ArgumentParser(description='Set GitHub repos to Archive matching pattern')
    p.add_argument('user', help='GitHub username / organizations')
    p.add_argument('oauth', help='Oauth filename')
    p.add_argument('pattern', help='archive repos with name starting with this string')
    P = p.parse_args()

# %% authentication
    sess = gb.github_session(P.oauth)

    gb.check_api_limit(sess)
# %% prepare to loop over repos
    repos = gb.get_repos(sess, P.user)
    if not repos:
        raise SystemExit(f'no repos for {P.user}')

    to_archive = [repo for repo in repos if repo.name.startswith(P.pattern) and not repo.archived]
    if not to_archive:
        raise SystemExit(f'no repos left to archive under {P.user}/{P.pattern}')

    print('NOTE: presently, you can only UNarchive through the website manually.')
    print('\ntype affirmative to ARCHIVE (make read-only)', '\n'.join([repo.full_name for repo in to_archive]))
    if input() != 'affirmative':
        raise SystemExit('Aborted')

    for repo in to_archive:
        repo.edit(archived=True)
        print('archived', repo.full_name)


if __name__ == '__main__':
    main()
