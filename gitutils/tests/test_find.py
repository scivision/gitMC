#!/usr/bin/env python
from pathlib import Path
import subprocess
import sys
import pytest
import gitutils.find as pgf

R = Path(__file__).parent
T = Path(__file__).resolve().parents[2]


def test_findfile():
    missdir = pgf.find_dir_missing_file("blahblah", "..")
    assert len(list(missdir)) > 0


def test_findfile_baddir(tmp_path):
    with pytest.raises(NotADirectoryError):
        next(pgf.find_dir_missing_file("blahblah", "asdfasfdfoo"))

    assert len(list(pgf.find_dir_missing_file("blahblah", tmp_path))) == 0

    assert len(list(pgf.find_dir_missing_file("test_find.py", R))) == 1


def test_findfile_script():
    subprocess.check_call([sys.executable, "find_missing_file.py", "blahblah", str(T)], cwd=T)


def test_actonchanged():
    subprocess.check_call([sys.executable, "ActOnChanged.py", str(R)], cwd=T)


if __name__ == "__main__":
    pytest.main([__file__])
