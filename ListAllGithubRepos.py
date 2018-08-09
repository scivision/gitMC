#!/usr/bin/env python
"""
lists all repos for a Github user.
Requires Oauth login because otherwise API is very limited for unauthenticated users.

The Oauth file should be in a secure place, NOT in a Git repo!
Maybe encrypted and with permissions 600.
The Oauth key should have no checkboxes, so that it's read only for public repos.
"""
import pandas as pd
import numpy as np
from pathlib import Path
import github
import logging
from argparse import ArgumentParser
from typing import Tuple, List
from time import sleep


def listall(user: str, oauth: Path, branch: str=None, verbose: bool=False) -> Tuple[pd.DataFrame, List[Tuple[str, int]]]:
    oauth = Path(oauth).expanduser()
    g = github.Github(oauth.read_text().strip())  # no trailing \n allowed

    repos = list(g.get_user().get_repos())
    dat = pd.DataFrame(np.empty((len(repos), 2), int),
                       index=[r.name for r in repos],
                       columns=['forks', 'stars'])

    ahead: List[Tuple[str, int]] = []

    for repo in repos:
        ahead = fork_prober(repo, ahead, branch)

        dat.loc[repo.name, :] = (repo.forks_count, repo.stargazers_count)
        sleep(0.1)  # don't hammer the API, avoiding 502 errors

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
        try:
            fmaster = fork.get_branch(b)
        except github.GithubException as e:
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

        sleep(0.1)  # don't hammer the API, avoiding 502 errors

    return ahead


def main():
    p = ArgumentParser(description='list all Github repos for a particular user')
    p.add_argument('user', help='Github username')
    p.add_argument('oauth', help='Oauth filename')

    P = p.parse_args()
    dat, ahead = listall(P.user, P.oauth)

    datnz = dat[~(dat == 0).all(axis=1)]
# %%
    pd.set_option('display.max_rows', 500)

    print(datnz.sort_values(['stars', 'forks'], ascending=False))

    print(ahead)


if __name__ == '__main__':
    main()
