import pytest
import subprocess
import asyncio

from gitutils.branch import coro_branch


@pytest.mark.parametrize("name, N", [("master", False), ("fake", True)])
def test_script_branch(name, N, git_init):
    p = git_init
    ret = subprocess.check_output(["gitbranch", str(p), name], text=True)
    if N:
        assert ret
    else:
        assert not ret


@pytest.mark.parametrize("name,N", [("master", 0), ("fake", 1)])
def test_branch(name, N, git_init):
    p = git_init
    branches = asyncio.run(coro_branch(name, p))
    assert len(branches) == N
