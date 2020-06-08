#!/usr/bin/env python
import subprocess
import pytest
from pathlib import Path

from gitutils.push import coro_modified
from gitutils.runner import runner

R = Path(__file__).parent
T = Path(__file__).resolve().parents[2]


def test_script():
    subprocess.check_call(["gitmodified", str(T)], cwd=T)


def test_mod():
    repos = runner(coro_modified, T)
    assert len(repos) in {0, 1}


if __name__ == "__main__":
    pytest.main([__file__])
