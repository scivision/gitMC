"""
detect Git local repo modifications. Crazy fast by not invoking remote.
"""
from pathlib import Path
from typing import Iterator
import subprocess
import logging

from .git import gitdirs, MAGENTA, BLACK, GITEXE, TIMEOUT

C0 = [GITEXE, 'rev-parse', '--abbrev-ref', 'HEAD']  # get branch name
C1 = [GITEXE, 'status', '--porcelain']  # uncommitted or changed files


def gitpushall(rdir: Path, verbose: bool = False) -> Iterator[Path]:
    """
    Notes which Git repos have local changes that haven't been pushed to remote

    Parameters
    ----------
    rdir : pathlib.Path
        top-level directory Git repos are under
    verbose : bool
        verbosity

    Yields
    ------
    dir_topush : generator of pathlib.Path
        Git repos that have local changes
    """

    for d in gitdirs(rdir):
        if detectchange(d, verbose):
            yield d


def detectchange(d: Path, verbose: bool = False) -> bool:
    """
    in depth check for local Git repo changes

    Parameters
    ----------
    d : pathlib.Path
        Git repo to check
    verbose : bool
        verbosity

    Results
    -------
    changed : bool
        has Git repo had local changes
    """

    try:
        # %% detect uncommitted changes
        ret = subprocess.check_output(C1, cwd=d, universal_newlines=True,
                                      timeout=TIMEOUT)
        changed = bool(ret)
        _print_change(ret, d, verbose)
        if changed:
            return changed
# %% detect committed, but not pushed
        branch = subprocess.check_output(C0, cwd=d, universal_newlines=True,
                                         timeout=TIMEOUT)[:-1]

        C2 = [GITEXE, 'diff', '--stat', f'origin/{branch}..']
        ret = subprocess.check_output(C2, cwd=d, universal_newlines=True,
                                      timeout=TIMEOUT)

        changed = bool(ret)
        _print_change(ret, d, verbose)
    except subprocess.CalledProcessError as e:
        logging.error(f'{d} {e.output}')

    return changed


def _print_change(ret: str, d: Path, verbose: bool = False):
    if verbose and ret:
        print(MAGENTA + str(d))
        print(BLACK + ret)
