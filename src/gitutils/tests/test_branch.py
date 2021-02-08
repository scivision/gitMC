import pytest
import subprocess
import asyncio

from gitutils.branch import git_branch


@pytest.mark.parametrize("name, N", [("main", False), ("fake", True)])
def test_script_branch(name, N, git_commit):
    p = git_commit

    ret = subprocess.check_output(["gitbranch", str(p), "-main", name], text=True)

    if N:
        assert ret
    else:
        assert not ret


@pytest.mark.parametrize("name,N", [("main", 0), ("fake", 1)])
def test_branch(name, N, git_commit):
    p = git_commit
    branches = asyncio.run(git_branch(name, p))
    assert len(branches) == N, f"{branches}"
