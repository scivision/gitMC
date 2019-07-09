#!/usr/bin/env python
import pytest
import os
import subprocess
from pathlib import Path
import gitutils.push as gup

R = Path(__file__).parent


def test_script():
    subprocess.check_call(['gitmodified', str(R.parent)])


@pytest.mark.asyncio
@pytest.mark.skipif(os.name == 'nt', reason='Pytest-asyncio not setup for Windows yet')
async def test_mod():

    repos = [r async for r in gup.git_modified(R.parent)]
    assert len(repos) in {0, 1}
