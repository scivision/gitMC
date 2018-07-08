#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest

rdir = Path(__file__).resolve().parents[1]


def test_git_push():
    subprocess.check_call(['gtps', '..'], cwd=rdir)


def test_gitbranch():
    subprocess.check_call(['gitbranch', '..'], cwd=rdir)


def test_email():
    subprocess.check_call(['gitemail'], cwd=rdir)


if __name__ == '__main__':
    pytest.main()
