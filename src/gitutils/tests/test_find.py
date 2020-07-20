import subprocess
import pytest

import gitutils.find as pgf


def test_findfile(tmp_path):
    sub1 = tmp_path / "sub1"
    sub1.mkdir()
    missdir = list(pgf.find_dir_missing_file(tmp_path, "blahblah"))
    assert len(missdir) == 1
    assert missdir[0].samefile(sub1)


def test_findfile_baddir():
    with pytest.raises(NotADirectoryError):
        next(pgf.find_dir_missing_file("asdfasfdfoo", "blahblah"))


def test_missing(tmp_path):
    sub1 = tmp_path / "sub1"
    sub1.mkdir()
    miss = list(pgf.find_dir_missing_file(tmp_path, "blahblah"))
    assert len(miss) == 1
    assert miss[0].samefile(sub1)

    (sub1 / "foo").touch()
    assert len(list(pgf.find_dir_missing_file(tmp_path, "foo"))) == 0


def test_findfile_script(tmp_path):
    subprocess.check_call(["find_missing_file", str(tmp_path), "blahblah"])


def test_actonchanged(tmp_path):
    subprocess.check_call(["ActOnChanged", str(tmp_path)])
