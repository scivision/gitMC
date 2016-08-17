==========
pygitutils
==========

Platform-independent (Linux/Mac/Windows) (Python 2.7 / Python 3.5) Git utilities, 
useful for managing large (100+) numbers of Git repos.
I use command-line git because PyGit requires command-line Git to be installed, 
and I don't need the advanced functionality.

Prereq
======
::

   git


====================    ========
Program                 Function
====================    ========
gtpl                    Pulls all git repos under directory  [~/code]
gtps                    Pushes  "     "     "     "     "          "
gitbranch               Tells of any non-master branches under directory [~/code]
git_filemode_windows    Sets all git repos to don't care permissions under directory  [~/code]
====================    ========
