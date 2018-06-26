#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest
from pygitutils import fetchpull

rdir = Path(__file__).parent


def atest_gitpushpullfetch():
    fetchpull('pull', rdir.parent)
    fetchpull('fetch', rdir.parent)


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
