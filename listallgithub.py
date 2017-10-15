#!/usr/bin/env python
"""
lists all repos for a Github user. 
Requires Oauth login because otherwise API is very limited for unauthenticated users.

The Oauth file should be in a secure place, NOT in a Git repo! 
Maybe encrypted and with permissions 600.
The Oauth key should have no checkboxes, so that it's read only for public repos.
I'll leave it to you if you trust PyGithub with private repos.
"""
from tabulate import tabulate
from pandas import DataFrame
from pathlib import Path
from github import Github


def listall(user:str, oauth:Path):
    oauth = Path(oauth).expanduser()
    g = Github(oauth.read_text().strip())  # no trailing \n allowed
    
    repos = g.get_user().get_repos()
    dat = DataFrame(columns=['repos','Nforks'])
    for repo in repos:
        dat=dat.append({'repos':repo.name,'Nforks':repo.forks_count},ignore_index=True)

    return dat

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='list all Github repos for a particular user')
    p.add_argument('user',help='Github username')
    p.add_argument('oauth',help='Oauth filename')
    
    p = p.parse_args()

    dat = listall(p.user, p.oauth)
    
    print(tabulate(dat,headers='keys'))