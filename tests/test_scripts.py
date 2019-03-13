#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest

R = Path(__file__).parent


@pytest.mark.parametrize('op', ['gitmodified', 'gitbranch', 'gitemail'])
def test_git(op):
    subprocess.check_call([op, '..'], cwd=R)


if __name__ == '__main__':
    pytest.main(['-x', __file__])
