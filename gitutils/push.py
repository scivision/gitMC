from pathlib import Path
from typing import List
import subprocess
import logging

from .git import baddir, MAGENTA, BLACK, GITEXE


def gitpushall(rdir: Path, verbose: bool = False) -> List[Path]:
    """
    Notes which Git repos have local changes that haven't been pushed to remote

    Parameters
    ----------
    rdir : pathlib.Path
        top-level directory Git repos are under
    verbose : bool
        verbosity

    Results
    -------
    dir_topush : list of pathlib.Path
        list of Git repos that have local changes
    """
    rdir = Path(rdir).expanduser()
    dlist = [x for x in rdir.iterdir() if not baddir(x)]

    if not dlist:
        if not baddir(rdir):
            dlist = [rdir]
        else:
            raise FileNotFoundError(f'no Git repos found under {rdir}')

    dir_topush = []
    for d in dlist:
        if detectchange(d, verbose):
            dir_topush.append(d)

    return dir_topush


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
    c1 = ['git', 'status', '--porcelain']  # uncommitted or changed files
    assert isinstance(GITEXE, str)

    try:
        # %% detect uncommitted changes
        ret = subprocess.check_output(c1, cwd=d, universal_newlines=True)
        changed = _print_change(ret, d, verbose)
        if changed:
            return changed

# %% detect committed, but not pushed
        c0 = [GITEXE, 'rev-parse', '--abbrev-ref', 'HEAD']  # get branch name
        branch = subprocess.check_output(c0, cwd=d, universal_newlines=True)[:-1]

        c2 = [GITEXE, 'diff', '--stat', f'origin/{branch}..']
        ret = subprocess.check_output(c2, cwd=d, universal_newlines=True)
        changed = _print_change(ret, d, verbose)
    except subprocess.CalledProcessError as e:
        logging.error(f'{d} {e.output}')

    return changed


def _print_change(ret: str, d: Path, verbose: bool = False) -> bool:
    changed = False

    if ret:
        changed = True
        if verbose:
            print(MAGENTA + str(d))
            print(BLACK + ret)

    return changed
