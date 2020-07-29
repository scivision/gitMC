import subprocess
import pytest


@pytest.mark.parametrize("op", ["gitemail"])
def test_email(op, git_commit):
    p = git_commit
    ret = subprocess.check_output([op, str(p)], text=True)
    assert ret
