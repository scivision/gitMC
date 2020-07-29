import subprocess
import pytest

import gitutils.find as pgf
import gitutils.git as pg


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
    ret = subprocess.check_output(["find_missing_file", str(tmp_path), "blahblah"], text=True)
    assert not ret


def test_actonchanged(git_init):
    p = git_init
    ch = pg.listchanged(p)
    assert not ch
    ret = subprocess.check_output(["ActOnChanged", str(p)], text=True)
    assert not ret

    fn = p / "foo.txt"
    fn.touch()
    subprocess.check_call(["git", "-C", str(p), "add", fn])
    fn.write_text("hello")
    ch = pg.listchanged(p)
    assert ch
    ret = subprocess.check_output(["ActOnChanged", str(p)], text=True)
    assert ret
