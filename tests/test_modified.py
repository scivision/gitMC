#!/usr/bin/env python
import subprocess
import pytest
import sys
from pathlib import Path
from gitutils.push import coro_local
from gitutils.runner import runner

R = Path(__file__).parent


def test_script():
    subprocess.check_call([sys.executable, "modified.py", str(R.parent)], cwd=R.parent)


def test_mod():
    repos = runner(coro_local, R.parent)
    assert len(repos) in {0, 1}


if __name__ == "__main__":
    pytest.main([__file__])
