"""
detect Git local repo modifications. Crazy fast by not invoking remote.
"""
import asyncio
from pathlib import Path
from typing import Tuple, AsyncGenerator

from .git import gitdirs, GITEXE

C0 = ['rev-parse', '--abbrev-ref', 'HEAD']  # get branch name
C1 = ['status', '--porcelain']  # uncommitted or changed files


async def git_modified(rdir: Path) -> AsyncGenerator[Tuple[str, str], None]:
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
        proc = await asyncio.create_subprocess_exec(*[GITEXE, '-C', str(d)] + C1,
                                                    stdout=asyncio.subprocess.PIPE)
        stdout, _ = await proc.communicate()
        ret = stdout.decode('utf8').rstrip()
# %% detect uncommitted changes
        if ret:
            yield d.name, ret
            continue
# %% detect committed, but not pushed
        proc = await asyncio.create_subprocess_exec(*[GITEXE, '-C', str(d)] + C0,
                                                    stdout=asyncio.subprocess.PIPE)
        stdout, _ = await proc.communicate()
        branch = stdout.decode('utf8').rstrip()

        C2 = [GITEXE, '-C', str(d), 'diff', '--stat', f'origin/{branch}..']
        proc = await asyncio.create_subprocess_exec(*C2, stdout=asyncio.subprocess.PIPE)
        stdout, _ = await proc.communicate()
        ret = stdout.decode('utf8').rstrip()

        if ret:
            yield d.name, ret
