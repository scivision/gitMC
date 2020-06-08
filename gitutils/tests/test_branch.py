#!/usr/bin/env python
import pytest
import subprocess
from pathlib import Path

from gitutils.branch import coro_branch
from gitutils.runner import runner

R = Path(__file__).parent
T = Path(__file__).resolve().parents[2]


def test_script():
    subprocess.check_call(["gitbranch", str(T)], cwd=T)


@pytest.mark.parametrize("path, N", [(R, 0), (T, 1)])
def test_branch(path, N):

    branches = runner(coro_branch, "fake_branchname", path)
    assert len(branches) == N


if __name__ == "__main__":
    pytest.main([__file__])
