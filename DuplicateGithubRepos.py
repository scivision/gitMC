#!/usr/bin/env python
"""
Duplicate repos specified in spreadsheet.
Requires GitHub Oauth login.

The Oauth file should be in a secure place, NOT in a Git repo!
Maybe encrypted and with permissions 600.
The Oauth key must have "repo" checked, or you'll get 404 error on user.create_repo().

Assumes you have an SSH key loaded for git push --mirror step
"""
from argparse import ArgumentParser
import gitutils.github_duplicator as gu
import gitutils.github_base as gb


def main():
    p = ArgumentParser(description='Duplice Github repos from spreadsheet input')
    p.add_argument('fn', help='spreadsheet filename')
    p.add_argument('oauth', help='Oauth filename')
    p.add_argument('-u', '--username', help='username or organization to create duplicate under')
    p.add_argument('-s', '--stem', help='beginning of duplicated repo names')
    p.add_argument('-w', '--sheet', help='excel sheet to process', required=True)
    p = p.parse_args()

    repos = gb.read_repos(p.fn, p.sheet)

    gu.repo_dupe(repos, p.oauth, p.username, p.stem)


if __name__ == '__main__':
    main()
