#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest

rdir = Path(__file__).parent


def atest_gitpull():
    subprocess.check_call(['gtpl', '..'], cwd=rdir)


def atest_gitfetch():
    subprocess.check_call(['gtft', '..'], cwd=rdir)


def test_git_push():
    subprocess.check_call(['gtps', '..'], cwd=rdir)


def test_gitbranch():
    subprocess.check_call(['gitbranch', '..'], cwd=rdir)


def test_actonchanged():
    subprocess.check_call(['ActOnChanged', '.'], cwd=rdir)


def test_email():
    subprocess.check_call(['gitemail'], cwd=rdir)


if __name__ == '__main__':
    pytest.main()
