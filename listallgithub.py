#!/usr/bin/env python
"""
lists all repos for a user without needing PyGithub package or login.
Note current limit for unauthenticated Github API is 60 requests/hour.

Specify -f if you already downloaded the file,
or -u user to download tuser.json via unauthenticated Github API (no private repos)
"""
from urllib.request import urlretrieve
from pandas import read_json # more robust than built-in JSON

def listall(user:str,fn):
    if user:
        url = f'https://api.github.com/users/{user}/repos?per_page=1000'
        fn = f'{user}.json'
        print(f'downloading {url} to {fn}')
        urlretrieve(url,fn)
        
    return read_json(fn)


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='list all Github repos for a particular user')
    p.add_argument('-u','--user',help='Github username')
    p.add_argument('-f','--fn',help='Github JSON file to read')
    
    p = p.parse_args()

    dat = listall(p.user,p.fn)

    names = dat['full_name'].tolist()
    urls = dat['html_url'].tolist()