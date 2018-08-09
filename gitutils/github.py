from typing import Tuple, List
from time import sleep
from datetime import datetime
import numpy as np
from pathlib import Path
import github
import logging
import pandas as pd


def repo_prober(user: str, oauth: Path=None, branch: str=None, verbose: bool=False) -> Tuple[pd.DataFrame, List[Tuple[str, int]]]:
    # %% authenication
    sess = github_session(oauth)

    if not check_api_limit(sess):
        raise RuntimeError('GitHub API limit exceeded')
# %% prepare to loop over repos
    repos = _get_repos(sess, user)

    dat = pd.DataFrame(np.empty((len(repos), 2), int),
                       index=[r.name for r in repos],
                       columns=['forks', 'stars'])

    ahead: List[Tuple[str, int]] = []

    for repo in repos:
        ahead = fork_prober(repo, ahead, branch)

        dat.loc[repo.name, :] = (repo.forks_count, repo.stargazers_count)

        if not check_api_limit(sess):
            raise RuntimeError('GitHub API limit exceeded')

        sleep(1.)

    return dat, ahead


def fork_prober(repo, ahead: List[Tuple[str, int]], branch: str=None,
                verbose: bool=False) -> List[Tuple[str, int]]:

    b = repo.default_branch if not branch else branch

    try:
        master = repo.get_branch(b)
    except github.GithubException as e:
        logging.error(f'{repo.full_name}  {e}')
        return ahead

    forks = repo.get_forks()
    for fork in forks:
        sleep(0.2)  # don't hammer the API, avoiding 502 errors

        try:
            fmaster = fork.get_branch(b)
        except github.GithubException as e:
            if e.data['message'] == 'Not Found':  # repo/branch that they deleted  FIXME: should we check their default branch?
                continue

            logging.error(f'{repo.full_name} {fork.full_name}  {e}')
            continue

        try:
            comp = repo.compare(master.commit.sha, fmaster.commit.sha)
        except github.GithubException as e:
            if e.data['message'].startswith('No common ancestor'):
                continue

            logging.error(f'{repo.full_name} {fork.full_name}  {e}')
            continue

        if comp.ahead_by:
            ahead.append((fork.full_name, comp.ahead_by))
            print(f'{fork.full_name} ahead by {comp.ahead_by}', end="")
            if verbose and comp.behind_by:
                print(f'behind by {comp.behind_by}', end="")
            print()

    return ahead


def _get_repos(g: github.Github, user: str) -> list:
    repo = user.split('/')

    if len(repo) == 2:  # assuming a single repo is specified
        repos = [g.get_user(repo[0]).get_repo(repo[1])]
    elif len(repo) == 1:
        repos = list(g.get_user(repo[0]).get_repos())

    return repos


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
        logging.critical(f'GitHub rate limit exceeded: {api_remaining} / {api_max}. Try again after {treset} UTC.')
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
