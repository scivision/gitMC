import subprocess
import sys


def test_email(git_commit):
    p = git_commit
    ret = subprocess.check_output([sys.executable, "-m", "gitutils.email", p], text=True)
    assert ret
