import subprocess

from gitutils.push import coro_modified
from gitutils.runner import runner


def test_script_modified(git_init):
    p = git_init
    ret = subprocess.check_output(["gitmodified", str(p)])
    assert not ret

    (p / "foo.txt").touch()
    ret = subprocess.check_output(["gitmodified", str(p)])
    assert ret


def test_modified(git_init):
    p = git_init
    repos = runner(coro_modified, p)
    assert len(repos) == 0

    (p / "foo.txt").touch()
    repos = runner(coro_modified, p)
    assert len(repos) == 1
