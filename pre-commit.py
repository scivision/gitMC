#!/usr/bin/env python
"""
To check your Git commits locally for:
* no trailing whitespace
* PEP8 (python only)
* mypy type hint (python only)

1. set Git to look for pre-commit hook by in Termina:
    git config --global core.hooksPath ~/.git/hooks
2. put this script at ~/.git/hooks/pre-commit (no .py extension)


Requires Python >= 3.5

* https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
* https://www.scivision.dev/git-commit-precheck-pep8/
"""

import subprocess
from pathlib import Path
import sys
import shutil

# %% pre-flight checks
if sys.version_info < (3, 5):
    raise SystemExit('Python >= 3.5 required for Git pre-commit hooks')

# %% Python checking
ret = subprocess.run(['git', 'diff', '--staged', '--name-only'], stdout=subprocess.PIPE, universal_newlines=True)
if ret.returncode:
    raise SystemExit('failed to run Git diff')

pystaged = [f for f in ret.stdout.split('\n') if f.endswith('.py') and Path(f).is_file()]

for f in pystaged:
    code = Path(f).read_text()
    if "breakpoint(" in code:
        raise SystemExit('Remove breakpoint in {} before commit'.format(f))

if pystaged:
    flake8 = shutil.which('flake8')
    if flake8:
        ret = subprocess.run(['flake8'] + pystaged)
        if ret.returncode:
            raise SystemExit('fix PEP8 issues before commit')
    else:
        print('could not find flake8', file=sys.stderr)

    mypy = shutil.which('mypy')
    if mypy:
        ret = subprocess.run(['mypy'] + pystaged)
        if ret.returncode:
            raise SystemExit('fix type hinting issues before commit')
    else:
        print('could not find mypy', file=sys.stderr)

# %% general checks
ret = subprocess.run(['git', 'diff-index', '--check', '--cached', 'HEAD', '--'])
if ret.returncode:
    raise SystemExit('Fix whitespace issues before commit')
