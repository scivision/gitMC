==========
pygitutils
==========

Platform-independent (Linux/Mac/Windows) Git utilities, 
useful for managing large (100+) numbers of Git repos.
I use command-line git because PyGit requires command-line Git to be installed, 
and I don't need the advanced functionality.

Prereq
======
::

   git

Sync large number of git repos in subdirectories
================================================
These assume numerous subdirectories under `~/code` or `c:\code`. They work very quickly for large numbers (100+) repos::

gtps.py     check if any repos have pending changes
gtpl.py     `git pull` all repos
gtft.py     `git fetch` all repos

You can place an empty file `.nogit` in a subdirectory if you don't want it to be checked for `pull` or `push`.
For `gtps.py`, the changed files are noted--you have to `cd` to that directory and commit/push as usual.

Program listing
===============

====================    ========
Program                 Function
====================    ========
gtpl                    Pulls all git repos under directory  [~/code]
gtps                    Pushes  "     "     "     "     "          "
gtft                    Fetches "     " 
gitbranch               Tells of any non-master branches under directory [~/code]
git_filemode_windows    Sets all git repos to don't care permissions under directory  [~/code]
gitemail                list all contributor email addresses
====================    ========
