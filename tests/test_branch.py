#!/usr/bin/env python
import pytest
from gitutils.branch import coro_local
from gitutils.runner import runner
import subprocess
import sys
from pathlib import Path

R = Path(__file__).parent


def test_script():
    subprocess.check_call([sys.executable, "branch.py", str(R.parent)], cwd=R.parent)


@pytest.mark.parametrize("path, N", [(R, 0), (R.parent, 1)])
def test_branch(path, N):

    branches = runner(coro_local, "fake_branchname", path)
    assert len(branches) == N


if __name__ == "__main__":
    pytest.main([__file__])
