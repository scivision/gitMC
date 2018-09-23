import github
from pathlib import Path
from datetime import datetime
import logging
from typing import Union, Optional
import pandas


def check_api_limit(g: github.Github=None) -> bool:
    """
    https://developer.github.com/v3/#rate-limiting
    don't hammer the API, avoiding 502 errors

    No penalty for checking rate limits
    """
    if g is None:
        g = github_session()

    ok = True

    api_limits = g.rate_limiting   # remaining, limit
    api_remaining, api_max = api_limits
    treset = datetime.utcfromtimestamp(g.rate_limiting_resettime)  # local time

    if api_remaining == 0:
        raise RuntimeError(f'GitHub rate limit exceeded: {api_remaining} / {api_max}. Try again after {treset} UTC.')
        ok = False
    elif api_remaining < 10:
        logging.warning(f'approaching GitHub API limit, {api_remaining} / {api_max} remaining until {treset} UTC.')
    else:
        logging.debug(f'GitHub API limit: {api_remaining} / {api_max} remaining until {treset} UTC.')

    return ok


def github_session(oauth: Path=None) -> github.Github:
    if oauth:
        oauth = Path(oauth).expanduser()
        g = github.Github(oauth.read_text().strip())  # no trailing \n allowed
    else:  # unauthenticated
        g = github.Github()

    return g


def repo_exists(user: Union[github.AuthenticatedUser.AuthenticatedUser,
                            github.Organization.Organization],
                reponame: str) -> bool:
    """
    user: GitHub user session
    reponame: reponame under user e.g. pymap3d
    """
    exists = False
    try:
        repo = user.get_repo(reponame)
        if repo.name:
            exists = True
    except github.GithubException as e:
        pass

    return exists


def last_commit_date(sess: github.Github, name: str) -> Optional[datetime]:
    """
    git show -s --format=%cI HEAD
    """
    time = None

    try:
        repo = sess.get_repo(name)
        if not repo_isempty(repo):
            time = repo.pushed_at
    except github.GithubException as e:
        logging.error(f'{name} not found \n')

    return time


def repo_isempty(repo: github.Repository) -> bool:
    try:
        repo.get_contents('/')
        empty = False
    except github.GithubException as e:
        logging.error(f'{repo.name} is empty. \n')
        empty = True

    return empty


def read_repos(fn: Path, sheet: str) -> pandas.Series:
    """
    make pandas.Series of email/id, Git url from spreadsheet
    """

    # %% get list of repos to duplicate
    fn = Path(fn).expanduser()
    repos = pandas.read_excel(fn, sheet_name=sheet, index_col=0, usecols="A, D")
    repos.dropna(how='any', inplace=True)

    return repos
