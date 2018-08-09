[![Build Status](https://travis-ci.org/scivision/gitutils.svg?branch=master)](https://travis-ci.org/scivision/gitutils)
[![Coverage Status](https://coveralls.io/repos/github/scivision/gitutils/badge.svg?branch=master)](https://coveralls.io/github/scivision/gitutils?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/99omgmbo508bwrib?svg=true)](https://ci.appveyor.com/project/scivision/gitutils)
[![pypi versions](https://img.shields.io/pypi/pyversions/gitutils.svg)](https://pypi.python.org/pypi/gitutils)
[![pypi format](https://img.shields.io/pypi/format/gitutils.svg)](https://pypi.python.org/pypi/gitutils)
[![PyPi Download stats](http://pepy.tech/badge/gitutils)](http://pepy.tech/project/gitutils)

# Git Utilities

Platform-independent (Linux/Mac/Windows) Git utilities, useful for managing large (100+) numbers of Git repos. 
I use command-line `git` because PyGit also requires command-line Git installed, and I don't need the advanced functionality.

A very important feature in 
```sh
ListAllGithubRepos
``` 
is showing which forks of your repos have had changes "ahead of" your code.
This shows your code is being improved, even if the forked repo didn't make a pull request.
I don't know of any other easy way out there to find this.

## Install

Install Git in a way accessible from the command line line

-   Mac: `brew install git`
-   Linux: `apt install git`
-   Windows: command line [Git](https://git-scm.com/download/win).
-   BSD: `pkg install git`

```sh
python -m pip install -e . 
```


## Usage

I didn't know of any other easy ways to do these Git tasks:

* `gitbranch` Tells of any non-master branches under directory ~/code
* `git_filemode_windows`  Sets all git repos to don't care permissions under directory ~/code
* `gitemail` list all contributor email addresses. Optionally, amend email addresses for prior Git commits

### GitHub

`ListAllGithubRepos`  
Gives stats on GitHub repos for a particular user.
It requires extra prereqs via: 
```sh
pip install -e .[github]
```

### Sync large number of git repos

These assume numerous subdirectories under `~/code` or `c:\code`. They
work very quickly for large numbers (100+) repos

* `gtps` check if any repos have pending changes
* `gtpl` Git pulls all repos
* `gtft` Git fetches all repos

You can place an empty file `.nogit` in a subdirectory to skip `pull` or `push`. 


### Preview all changed Jekyll files

This is for a website made using
[Jekyll](https://www.scivision.co/create-jekyll-github-pages-website):
```sh
ActOnChanged -j
```

