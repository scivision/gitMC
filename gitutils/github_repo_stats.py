"""
How many total GitHub stars do you have?
"""
from typing import Tuple, List
from time import sleep
import numpy as np
from pathlib import Path
import github
import logging
import pandas as pd

from .github_base import check_api_limit, github_session


def repo_prober(user: str, oauth: Path = None, branch: str = None,
                verbose: bool = False) -> Tuple[pd.DataFrame, List[Tuple[str, int]]]:
    """
    probe all GitHub repos for a user to see how much forks of each repo are ahead.
    Discover if there is an actively developed fork of your GitHub repos

    Parameters
    ----------
    user : str
        GitHub username
    oauth : pathlib.Path
        file containing GitHub Oauth hash
    branch : str
        Git branch to examine
    verbose : bool
        verbosity

    Results
    -------
    dat : pandas.DataFrame
        forks and stars for each repo
    ahead : list of tuple of str, int
        forked with repos with number of commits they're ahead of your repo
    """
    # %% authentication
    sess = github_session(oauth)

    check_api_limit(sess)
# %% prepare to loop over repos
    repos = _get_repos(sess, user)

    dat = pd.DataFrame(np.empty((len(repos), 2), int),
                       index=[r.name for r in repos],
                       columns=['forks', 'stars'])

    ahead: List[Tuple[str, int]] = []

    for repo in repos:
        ahead = fork_prober(repo, sess, ahead, branch)

        dat.loc[repo.name, :] = (repo.forks_count, repo.stargazers_count)

        check_api_limit(sess)

        sleep(1.)

    return dat, ahead


def fork_prober(repo, sess,
                ahead: List[Tuple[str, int]],
                branch: str = None,
                verbose: bool = False) -> List[Tuple[str, int]]:
    """
    check a GitHub repo for forks

    Parameters
    ----------
    repo :
        handle to GitHub repo
    sess :
        handle to GitHub session
    ahead : list of tuple of str, int
        forked with repos with number of commits they're ahead of your repo
    branch : str
        Git branch to examine
    verbose : bool
        verbosity

    Results
    -------
    ahead : list of tuple of str, int
        forked with repos with number of commits they're ahead of your repo
    """
    check_api_limit(sess)

    b = repo.default_branch if not branch else branch

    try:
        master = repo.get_branch(b)
    except github.GithubException as e:
        logging.error(f'{repo.full_name}  {e}')
        return ahead

    forks = repo.get_forks()
    for fork in forks:
        sleep(0.2)  # don't hammer the API, avoiding 502 errors

        check_api_limit(sess)

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
