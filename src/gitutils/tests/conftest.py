import pytest
import subprocess

from ..git import git_exe, TIMEOUT


@pytest.fixture(scope="function")
def git_init(tmp_path):
    to = TIMEOUT["local"]
    subprocess.check_call([git_exe(), "-C", str(tmp_path), "init", "-b", "main"], timeout=to)
    return tmp_path


@pytest.fixture(scope="function")
def git_commit(git_init):
    p = git_init
    (p / "foo.txt").touch()

    to = TIMEOUT["local"]
    subprocess.check_call([git_exe(), "-C", str(p), "add", "."], timeout=to)

    subprocess.check_call(
        [git_exe(), "-C", str(p), "config", "user.email", "you@example.invalid"], timeout=to
    )
    subprocess.check_call([git_exe(), "-C", str(p), "config", "user.name", "Your Name"], timeout=to)

    subprocess.check_call(
        [git_exe(), "-C", str(p), "commit", "-am", "test", "--no-verify", "--no-gpg-sign"],
        timeout=to,
    )
    return p
