#!/usr/bin/env python
from pathlib import Path
import subprocess
import os
import pytest
from pygitutils import fetchpull

rdir = Path(__file__).parents[1]

cmd = 'python ' if os.name == 'nt' else ''


def test_gitpushpullfetch():
    fetchpull('pull', rdir.parent)
    fetchpull('fetch', rdir.parent)


def test_gitbranch():
    subprocess.check_call((cmd + 'gitbranch.py ..').split(), cwd=rdir)


def test_actonchanged():
    subprocess.check_call((cmd + 'ActOnChanged.py .').split(), cwd=rdir)


def test_email():
    subprocess.check_call((cmd + 'gitemail.py').split(), cwd=rdir)


if __name__ == '__main__':
    pytest.main()
