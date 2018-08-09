#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest

R = Path(__file__).parent


def test_gitpull():
    subprocess.check_call(['gtpl', '.'], cwd=R)


def test_gitfetch():
    subprocess.check_call(['gtft', '.'], cwd=R)


if __name__ == '__main__':
    pytest.main(['-x', __file__])
