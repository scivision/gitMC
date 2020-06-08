#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest

R = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("op", ["gitemail"])
def test_git(op):
    subprocess.check_call([op, str(R)])


if __name__ == "__main__":
    pytest.main([__file__])
