"""
detect Git local repo modifications. Crazy fast by not invoking remote.
"""
from pathlib import Path
from typing import Tuple, Iterator
import subprocess
from .git import gitdirs, GITEXE, TIMEOUT

C0 = [GITEXE, 'rev-parse', '--abbrev-ref', 'HEAD']  # get branch name
C1 = [GITEXE, 'status', '--porcelain']  # uncommitted or changed files


def gitpushall(rdir: Path) -> Iterator[Tuple[Path, str]]:
    """
    Notes which Git repos have local changes that haven't been pushed to remote

    Parameters
    ----------
    rdir : pathlib.Path
        top-level directory Git repos are under

    Yields
    -------
    changes : tuple of pathlib.Path, str
        Git repos that have local changes
    """
    for d in gitdirs(rdir):
        try:
            # %% detect uncommitted changes
            ret = subprocess.check_output(C1, cwd=d, universal_newlines=True,
                                          timeout=TIMEOUT)
            if ret:
                yield d, ret
                continue
    # %% detect committed, but not pushed
            branch = subprocess.check_output(C0, cwd=d, universal_newlines=True,
                                             timeout=TIMEOUT)[:-1]

            C2 = [GITEXE, 'diff', '--stat', f'origin/{branch}..']
            ret = subprocess.check_output(C2, cwd=d, universal_newlines=True,
                                          timeout=TIMEOUT)
            if ret:
                yield d, ret
        except subprocess.CalledProcessError as e:
            yield d, e.output
