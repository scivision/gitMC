from pathlib import Path
import subprocess
import pytest
import asyncio

from gitutils.pull import coro_remote


@pytest.mark.skipif(__file__ is None, reason="can't find own directory")
@pytest.mark.parametrize("op", ["gitpull", "gitfetch", "gitcheck"])
def test_script_pull(op):
    R = Path(__file__).resolve().parent
    ret = subprocess.check_output([op, str(R)], text=True).strip()
    assert not ret


@pytest.mark.parametrize("mode", ["fetch", "pull"])
def test_nonGit_dir_pull(tmp_path, mode):

    dirs = asyncio.run(coro_remote(mode, tmp_path))
    assert len(dirs) == 0
