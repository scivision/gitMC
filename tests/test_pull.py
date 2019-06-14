#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest
import gitutils
import os

R = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('op', ['gitpull', 'gitfetch', 'gitcheck'])
def test_script(op):
    subprocess.check_call([op, str(R)])


@pytest.mark.asyncio
@pytest.mark.skipif(os.name == 'nt', reason='Pytest-asyncio not setup for Windows yet')
@pytest.mark.parametrize('mode', ['fetch', 'pull'])
async def test_nonGit_dir(tmp_path, mode):

    dirs = [d async for d in gitutils.fetchpull(mode, tmp_path)]
    assert len(dirs) == 0


@pytest.mark.asyncio
@pytest.mark.skipif(os.name == 'nt', reason='Pytest-asyncio not setup for Windows yet')
@pytest.mark.parametrize('mode', ['fetch', 'pull'])
async def test_fakeGit_dir(tmp_path, mode):
    fake = (tmp_path / '.git')
    fake.mkdir()
    fake.touch('HEAD')

    dirs = [d async for d in gitutils.fetchpull(mode, fake)]
    assert len(dirs) == 0


if __name__ == '__main__':
    pytest.main(['-x', __file__])
