"""
detect Git local repo modifications. Crazy fast by not invoking remote.
"""
import asyncio
import logging
from pathlib import Path
import typing

from .git import gitdirs, GITEXE

C0 = ["rev-parse", "--abbrev-ref", "HEAD"]  # get branch name
C1 = ["status", "--porcelain"]  # uncommitted or changed files


async def git_modified(path: Path) -> typing.Tuple[str, str]:
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
    proc = await asyncio.create_subprocess_exec(*[GITEXE, "-C", str(path)] + C1, stdout=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    if proc.returncode != 0:
        logging.error(f"{path.name} return code {proc.returncode}  {C1}")
    out = stdout.decode("utf8", errors="ignore").rstrip()
    logging.info(path.name)
    # %% detect uncommitted changes
    if out:
        return path.name, out
    # %% detect committed, but not pushed
    proc = await asyncio.create_subprocess_exec(*[GITEXE, "-C", str(path)] + C0, stdout=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    if proc.returncode != 0:
        logging.error(f"{path.name} return code {proc.returncode}  {C0}")
    branch = stdout.decode("utf8", errors="ignore").rstrip()

    C2 = [GITEXE, "-C", str(path), "diff", "--stat", f"origin/{branch}.."]
    proc = await asyncio.create_subprocess_exec(*C2, stdout=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    if proc.returncode != 0:
        logging.error(f"{path.name} return code {proc.returncode}  {branch}")
    out = stdout.decode("utf8", errors="ignore").rstrip()

    if out:
        return path.name, out
    return None


async def coro_local(path: Path) -> typing.List[Path]:
    futures = [git_modified(d) for d in gitdirs(path)]
    return list(filter(None, await asyncio.gather(*futures)))
