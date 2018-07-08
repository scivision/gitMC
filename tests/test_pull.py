#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest

rdir = Path(__file__).resolve().parents[1]


def test_gitpull():
    subprocess.check_call(['gtpl', '..'], cwd=rdir)


def test_gitfetch():
    subprocess.check_call(['gtft', '..'], cwd=rdir)


if __name__ == '__main__':
    pytest.main()
