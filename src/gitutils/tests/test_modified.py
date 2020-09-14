import subprocess
import asyncio

from gitutils.status import git_status


def test_script_modified(git_init):
    p = git_init
    ret = subprocess.check_output(["gitstat", str(p)], text=True)
    assert not ret

    (p / "foo.txt").touch()
    ret = subprocess.check_output(["gitstat", str(p)], text=True)
    assert ret


def test_modified(git_init):
    p = git_init
    repos = asyncio.run(git_status(p))
    assert len(repos) == 0

    (p / "foo.txt").touch()
    repos = asyncio.run(git_status(p))
    assert len(repos) == 1
