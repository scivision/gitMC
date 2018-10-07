#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest
import gitutils as pgu

R = Path(__file__).parent


def test_findfile():
    missdir = pgu.find_dir_missing_file('blahblah', '..')
    assert len(missdir) > 0
    subprocess.check_call(['find_missing_file', 'blahblah', '..'], cwd=R)


def test_actonchanged():
    subprocess.check_call(['ActOnChanged', '.'], cwd=R)


if __name__ == '__main__':
    pytest.main(['-x', __file__])
