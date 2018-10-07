#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest

R = Path(__file__).parent


def test_git_push():
    subprocess.check_call(['gitmodified', '.'], cwd=R)


def test_gitbranch():
    subprocess.check_call(['gitbranch', '.'], cwd=R)


def test_email():
    subprocess.check_call(['gitemail', '.'], cwd=R)


if __name__ == '__main__':
    pytest.main(['-x', __file__])
