#!/usr/bin/env python
import pytest
import gitutils.branch as gub
import subprocess
from pathlib import Path
import os

R = Path(__file__).parent


def test_script():
    subprocess.check_call(['gitbranch', str(R.parent)])


@pytest.mark.asyncio
@pytest.mark.skipif(os.name == 'nt', reason='Pytest-asyncio not setup for Windows yet')
@pytest.mark.parametrize('path, N', [(R, 0), (R.parent, 1)])
async def test_branch(path, N):

    branches = [b async for b in gub.findbranch('fake_branchname', path)]
    assert len(branches) == N


if __name__ == '__main__':
    pytest.main(['-x', __file__])
