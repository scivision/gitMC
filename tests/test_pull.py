#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest
import gitutils

R = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('op', ['gitpull', 'gitfetch', 'gitcheck'])
def test_git(op):
    subprocess.check_call([op, '.'], cwd=R)


@pytest.mark.parametrize('mode', ['fetch', 'pull'])
def test_nonGit_dir(tmp_path, mode):

    dirs = list(gitutils.fetchpull(mode, tmp_path))
    assert len(dirs) == 0


@pytest.mark.parametrize('mode', ['fetch', 'pull'])
def test_fakeGit_dir(tmp_path, mode):
    fake = (tmp_path / '.git')
    fake.mkdir()
    fake.touch('HEAD')

    dirs = list(gitutils.fetchpull(mode, fake))
    assert len(dirs) == 0


if __name__ == '__main__':
    pytest.main(['-x', __file__])
