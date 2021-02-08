"""
detect Git local repo modifications. Crazy fast by not invoking remote.

replaced by git status --porcelain:
  git ls-files -o -d --exclude-standard: # check for uncommitted files
  git --no-pager diff HEAD , # check for uncommitted work

DOES NOT WORK git log --branches --not --remotes     # check for uncommitted branches
"""

from __future__ import annotations
import argparse
import asyncio
import subprocess
import logging
from pathlib import Path

from . import _log
from .git import gitdirs, GITEXE, MAGENTA, BLACK, TIMEOUT

C0 = ["rev-parse", "--abbrev-ref", "HEAD"]  # get branch name
C1 = ["status", "--porcelain"]  # uncommitted or changed files

__all__ = ["git_porcelain"]


def git_porcelain(path: Path) -> bool:
    """
    detects if single Git repo is porcelain i.e. clean.
    May not have been pushed or fetched.

    Parameters
    ----------

    path: pathlib.Path
        path to Git repo

    Returns
    -------

    is_porcelain: bool
        true if local Git is clean
    """

    if not path.is_dir():
        raise NotADirectoryError(path)

    ret = subprocess.run(
        [GITEXE, "-C", str(path)] + C1, stdout=subprocess.PIPE, text=True, timeout=TIMEOUT
    )
    if ret.returncode != 0:
        logging.error(f"{path.name} return code {ret.returncode}  {C1}")
        return False
    return not ret.stdout


async def _git_status(path: Path) -> tuple[str, str]:
    """
    Notes which Git repos have local changes that haven't been pushed to remote

    Parameters
    ----------
    path : pathlib.Path
        Git repo directory

    Returns
    -------
    changes : tuple of pathlib.Path, str
        Git repo local changes
    """

    proc = await asyncio.create_subprocess_exec(
        *[GITEXE, "-C", str(path)] + C1, stdout=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    if proc.returncode != 0:
        logging.error(f"{path.name} return code {proc.returncode}  {C1}")
        return None
    out = stdout.decode("utf8", errors="ignore").rstrip()
    logging.info(path.name)
    # %% detect uncommitted changes
    if out:
        return path.name, out
    # %% detect committed, but not pushed
    proc = await asyncio.create_subprocess_exec(
        *[GITEXE, "-C", str(path)] + C0, stdout=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    if proc.returncode != 0:
        logging.error(f"{path.name} return code {proc.returncode}  {C0}")
        return None
    branch = stdout.decode("utf8", errors="ignore").rstrip()

    C2 = [GITEXE, "-C", str(path), "diff", "--stat", f"origin/{branch}.."]
    proc = await asyncio.create_subprocess_exec(*C2, stdout=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    if proc.returncode != 0:
        logging.error(f"{path.name} return code {proc.returncode}  {branch}")
        return None
    out = stdout.decode("utf8", errors="ignore").rstrip()
    if out:
        return path.name, out
    return None


async def git_status(path: Path, verbose: bool = False) -> list[str]:

    c = MAGENTA if verbose else ""

    changed = []
    for r in asyncio.as_completed([_git_status(d) for d in gitdirs(path)]):
        changes = await r
        if changes:
            changed.append(changes[0])
            print(c + changes[0])
            if verbose:
                print(BLACK + changes[1])

    return changed


def cli():
    p = argparse.ArgumentParser(description="get status of many Git repos")
    p.add_argument("path", help="path to look under", nargs="?", default="~/code")
    p.add_argument("-v", "--verbose", action="store_true")
    P = p.parse_args()

    _log(P.verbose)

    asyncio.run(git_status(P.path))


if __name__ == "__main__":
    cli()
