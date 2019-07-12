#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest
import gitutils.find as pgf

R = Path(__file__).parent


def test_findfile():
    missdir = pgf.find_dir_missing_file('blahblah', '..')
    assert len(missdir) > 0


def test_findfile_baddir(tmp_path):
    with pytest.raises(NotADirectoryError):
        pgf.find_dir_missing_file('blahblah', 'asdfasfdfoo')

    assert len(pgf.find_dir_missing_file('blahblah', tmp_path)) == 0

    assert len(pgf.find_dir_missing_file('test_find.py', R)) == 1


def test_findfile_script():
    subprocess.check_call(['find_missing_file', 'blahblah', str(R.parent)])


def test_actonchanged():
    subprocess.check_call(['ActOnChanged', str(R)])


if __name__ == '__main__':
    pytest.main(['-x', __file__])
