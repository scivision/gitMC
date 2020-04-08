#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest
import sys

R = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("op", ["gitemail.py"])
def test_git(op):
    subprocess.check_call([sys.executable, op, "."], cwd=R)


if __name__ == "__main__":
    pytest.main([__file__])
