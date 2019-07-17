#!/usr/bin/env python
"""
List all GitHub repos of a user / organization.
Optionally, open the settings or laerts page for each repo.

For organization private repos, you will need "repo" Oauth permission.
Restricted "Third-party application access policy"
from organization oauth_application_policy settings is OK.

Without Oauth, you will only see public repos
"""
from argparse import ArgumentParser
import webbrowser
import gitutils.github_base as gb


def main():
    p = ArgumentParser(description='List user/organization repos')
    p.add_argument('user', help='GitHub username / organization name')
    p.add_argument('oauth', help='Oauth filename', nargs='?')
    p.add_argument('-p', '--pattern', help='only repos with name starting with this string')
    p.add_argument('-settings', help='open settings page for each repo', action='store_true')
    p.add_argument('-alerts', help='open alerts page for each repo', action='store_true')
    P = p.parse_args()

# %% authentication
    sess = gb.github_session(P.oauth)
    gb.check_api_limit(sess)
# %% get user / organization handle
    userorg = gb.user_or_org(sess, P.user)
# %% prepare to loop over repos
    repos = gb.get_repos(userorg)
    if not repos:
        raise SystemExit(f'no repos for {P.user}')

    if P.pattern:
        repos = [repo for repo in repos if repo.name.startswith(P.pattern)]

    for repo in repos:
        print(repo.full_name)
        if P.settings:
            webbrowser.open_new_tab('https://github.com/' + repo.full_name + '/settings')
        if P.alerts:
            webbrowser.open_new_tab('https://github.com/' + repo.full_name + '/network/alerts')


if __name__ == '__main__':
    main()
