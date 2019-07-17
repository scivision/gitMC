#!/usr/bin/env python
"""
Set all collaborator permission to "read" for a user/organization with repo names matching pattern.

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
import logging
import webbrowser


def main():
    p = ArgumentParser(description='Set all collaborator permission to "read"')
    p.add_argument('user', help='GitHub username / organizations')
    p.add_argument('oauth', help='Oauth filename')
    p.add_argument('pattern', help='modify repos with name starting with this string')
    p.add_argument('--omit', help='dont consider these admins', nargs='+')
    P = p.parse_args()

# %% authentication
    sess = gb.github_session(P.oauth)
    gb.check_api_limit(sess)
# %% get user / organization handle
    userorg = gb.user_or_org(sess, P.user)
# %% prepare to loop over repos
    repos = gb.get_repos(userorg)

    to_modify = [repo for repo in repos if repo.name.startswith(P.pattern)]
    if not to_modify:
        raise SystemExit(f'no repos to modify under {P.user}/{P.pattern}')

    print('\ntype affirmative to remove all collaborators from\n', '\n'.join([repo.full_name for repo in to_modify]))
    modify = input() == 'affirmative'

    for repo in to_modify:
        collabs = repo.get_collaborators()

        admins = [c.login for c in collabs if c.login not in P.omit]
        if not admins:
            continue

        print('admins', repo.full_name, ' '.join(admins))
        if modify:
            if repo.archived:
                logging.error(f'could not remove collabs from archived {repo.full_name}')
                webbrowser.open_new_tab('https://github.com/' + repo.full_name + '/settings')
                continue

            for admin in admins:
                repo.remove_from_collaborators(admin)


if __name__ == '__main__':
    main()
