import pytest
import subprocess

from gitutils.branch import coro_branch
from gitutils.runner import runner


@pytest.mark.parametrize("name, N", [("master", False), ("fake", True)])
def test_script_branch(name, N, git_init):
    p = git_init
    ret = subprocess.check_output(["gitbranch", str(p), name], universal_newlines=True)
    if N:
        assert ret
    else:
        assert not ret


@pytest.mark.parametrize("name,N", [("master", 0), ("fake", 1)])
def test_branch(name, N, git_init):
    p = git_init
    branches = runner(coro_branch, name, p)
    assert len(branches) == N
