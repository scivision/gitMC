#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest

import gitutils.find as pgf

R = Path(__file__).parent
T = Path(__file__).resolve().parents[2]


def test_findfile():
    missdir = pgf.find_dir_missing_file(R, "blahblah")
    assert len(list(missdir)) > 0


def test_findfile_baddir():
    with pytest.raises(NotADirectoryError):
        next(pgf.find_dir_missing_file("asdfasfdfoo", "blahblah"))


def test_missing(tmp_path):
    assert len(list(pgf.find_dir_missing_file(tmp_path, "blahblah"))) == 0

    assert len(list(pgf.find_dir_missing_file(R, "test_find.py"))) == 1


def test_findfile_script():
    subprocess.check_call(["find_missing_file", str(T), "blahblah"])


def test_actonchanged():
    subprocess.check_call(["ActOnChanged", str(R)])


if __name__ == "__main__":
    pytest.main([__file__])
