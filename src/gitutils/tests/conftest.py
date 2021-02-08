import pytest
import subprocess


@pytest.fixture(scope="function")
def git_init(tmp_path):
    subprocess.check_call(["git", "-C", str(tmp_path), "init", "-b", "main"])
    return tmp_path


@pytest.fixture(scope="function")
def git_commit(git_init):
    p = git_init
    (p / "foo.txt").touch()
    subprocess.check_call(["git", "-C", str(p), "add", "."])

    subprocess.check_call(["git", "-C", str(p), "config", "user.email", "you@example.invalid"])
    subprocess.check_call(["git", "-C", str(p), "config", "user.name", "Your Name"])

    subprocess.check_call(["git", "-C", str(p), "commit", "-am", "test", "--no-verify"])
    return p
