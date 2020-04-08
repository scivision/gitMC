#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest
import sys

from gitutils.runner import runner
from gitutils.pull import coro_remote

R = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("op", ["pull.py", "fetch.py", "check.py"])
def test_script(op):
    subprocess.check_call([sys.executable, op, str(R)], cwd=R)


@pytest.mark.parametrize("mode", ["fetch", "pull"])
def test_nonGit_dir(tmp_path, mode):

    dirs = runner(coro_remote, mode, tmp_path)
    assert len(dirs) == 0


@pytest.mark.parametrize("mode", ["fetch", "pull"])
def test_fakeGit_dir(tmp_path, mode):
    fake = tmp_path / ".git"
    fake.mkdir()
    fake.touch("HEAD")

    dirs = runner(coro_remote, mode, fake)
    assert len(dirs) == 0


if __name__ == "__main__":
    pytest.main([__file__])
