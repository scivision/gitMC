import subprocess
import asyncio

import gitutils.status_cmd
import gitutils.status
from gitutils.git import TIMEOUT, MAX_CONCURRENT


def test_script_modified(git_init):
    p = git_init
    ret = subprocess.check_output(["gitstat", str(p)], text=True)
    assert not ret

    test_new = p / "foo.txt"
    test_new.touch()
    ret = subprocess.check_output(["gitstat", str(p), "-v"], text=True)
    assert ret, f"didn't find {test_new} in {ret}"


def test_modified_libgit2(git_init):
    p = git_init
    repos = gitutils.status.git_status(p)
    assert len(list(repos)) == 0

    test_new = p / "foo.txt"
    test_new.touch()
    repos = gitutils.status.git_status(p)
    r = list(repos)
    assert len(r) == 1
    print(r)


def test_modified_async(git_init):
    p = git_init
    repos = asyncio.run(
        gitutils.status_cmd.git_status_async(
            p, False, timeout=TIMEOUT["local"], max_concurrent=MAX_CONCURRENT
        )
    )
    assert len(repos) == 0

    (p / "foo.txt").touch()
    repos = asyncio.run(
        gitutils.status_cmd.git_status_async(
            p, False, timeout=TIMEOUT["local"], max_concurrent=MAX_CONCURRENT
        )
    )
    r = list(repos)
    assert len(r) == 1
