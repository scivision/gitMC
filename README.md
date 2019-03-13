[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2592584.svg)](https://doi.org/10.5281/zenodo.2592584)
[![Build Status](https://travis-ci.org/scivision/gitutils.svg?branch=master)](https://travis-ci.org/scivision/gitutils)
[![Coverage Status](https://coveralls.io/repos/github/scivision/gitutils/badge.svg?branch=master)](https://coveralls.io/github/scivision/gitutils?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/99omgmbo508bwrib?svg=true)](https://ci.appveyor.com/project/scivision/gitutils)
[![pypi versions](https://img.shields.io/pypi/pyversions/gitutils.svg)](https://pypi.python.org/pypi/gitutils)
[![PyPi Download stats](http://pepy.tech/badge/gitutils)](http://pepy.tech/project/gitutils)

# Git Utilities

Platform-independent (Linux/Mac/Windows) Git utilities, useful for managing large (100+) numbers of Git repos.
Speed is an emphasis throughout, with concurrency `asyncio` and pipelining enabled in much of the program.

This uses command-line `git` because PyGit also requires command-line Git installed, and we don't need the advanced functionality.

An important feature in
```sh
ListAllGithubRepos
```
is showing which forks of your repos have had changes "ahead of" your code.
This shows your code is being improved, even if the forked repo didn't make a pull request.
I don't know of any other easy way out there to find this.

Also see Git [utilities](https://github.com/scivision/gitedu) for managing large (100+) numbers of users / teams, particularly for education and institutions.

## Install

Install Git in a way accessible from the command line line

-   Mac: `brew install git`
-   Linux: `apt install git`
-   Windows: command line [Git](https://git-scm.com/download/win).

```sh
python -m pip install -e .
```


## Usage

I didn't know of any other easy ways to do these Git tasks:

* `gitbranch` Tells of any non-master branches under directory ~/code
* `git_filemode_windows`  Sets all git repos to don't care permissions under directory ~/code
* `gitemail` list all contributor email addresses. Optionally, amend email addresses for prior Git commits

### Sync large number of git repos

These assume numerous subdirectories under `~/code` or `c:\code`. 
They work very quickly for large numbers (100+) repos.


* `gitmodified` check if any local repos have pending changes
* `gitcheck` check if any remote repos are ahead of local
* `gitpull` Git pulls all repos
* `gitfetch` Git fetches all repos

You can place an empty file `.nogit` in a subdirectory to skip it.


#### [optional] speedup with https pull
For public repos, to make the Git remote checking go at least twice as fast, and significantly reduce the computational burden when SSH is used for `git push` (as is recommended), consider the "pushInsteadOf" global Git config.
To do this, when cloning a public repo (including ones you're a collaborator on), use `git clone https://`. 
This global SSH push config one-time does SSH push for HTTPS-cloned repos:
```sh
git config --global url."ssh://github.com/".pushInsteadOf https://github.com/
```
The pattern matching can be made for all sites by omitting `github.com` from the command above, or you can refine it for each site, or even for specific usernames by editing the command above.
For private repos, simply clone with SSH as usual


### Preview all changed Jekyll files

This is for a website made using
[Jekyll](https://www.scivision.co/create-jekyll-github-pages-website):
```sh
ActOnChanged -j
```

## Github
Python GitHub [API](https://pypi.org/project/PyGithub/)

Most users will need a GitHub API token, as the unauthenticated API access is severly limited.

1. [Generate](https://github.com/settings/tokens) GitHub API token with ONLY the `user:email` permission.
2. Copy that text string to a secure location on your computer.

### GitHub user stats

`ListAllGithubRepos username OauthKey`
Gives stats on GitHub repos for a particular user.
It requires extra prereqs via:
```sh
pip install -e .[github]
```

