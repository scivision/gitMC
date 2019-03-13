#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest

R = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('op', ['gitpull', 'gitfetch', 'gitcheck'])
def test_git(op):
    subprocess.check_call([op, '.'], cwd=R)


if __name__ == '__main__':
    pytest.main(['-x', __file__])
