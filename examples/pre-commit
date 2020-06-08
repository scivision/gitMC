#!/usr/bin/env python
"""
To check your Git commits locally for:
* no trailing whitespace
* PEP8 (python only)
* mypy type hint (python only)

1. set Git to look for pre-commit hook by in Terminal:
    git config --global core.hooksPath ~/.git/hooks
2. put this script at ~/.git/hooks/pre-commit (no .py extension)

Works on Python 3.x

* https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
* https://www.scivision.dev/git-commit-precheck-pep8/
"""

import shutil
import subprocess
import sys
import os

try:
    import yaml
except ImportError:
    yaml = None
    print("yaml checks not available", file=sys.stderr)

flake8 = shutil.which("flake8")
if not flake8:
    print("flake8 checks not available", file=sys.stderr)
mypy = shutil.which("mypy")
if not mypy:
    print("mypy checks not available", file=sys.stderr)

# %% Python checking
stdout = subprocess.check_output(["git", "diff", "--staged", "--name-only"], universal_newlines=True)

pystaged = [f for f in stdout.split("\n") if f.endswith(".py") and os.path.isfile(f)]

for f in pystaged:
    txt = open(f).read()
    if "breakpoint(" in txt:
        raise SystemExit("Remove breakpoint in {} before commit".format(f))

if pystaged:
    if flake8:
        if subprocess.call([flake8] + pystaged):
            raise SystemExit("fix PEP8 issues before commit")

    if mypy:
        if subprocess.call([mypy] + pystaged):
            raise SystemExit("fix type hinting issues before commit")

if yaml is not None:
    ymlstaged = (f for f in stdout.split("\n") if f.endswith((".yml", ".yaml")) and os.path.isfile(f))
    for f in ymlstaged:
        yaml.safe_load(open(f).read())

# %% general checks
if subprocess.call(["git", "diff-index", "--check", "--cached", "HEAD", "--"]):
    raise SystemExit("Fix whitespace issues before commit")
