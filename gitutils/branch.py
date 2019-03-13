"""
Operations for Git branches
"""

from typing import List, Tuple
from pathlib import Path
import asyncio
import logging
import shutil

from .git import baddir

GITEXE = shutil.which('git')
if not GITEXE:
    raise FileNotFoundError('Could not find executable for Git')

CMD = [GITEXE, 'rev-parse', '--abbrev-ref', 'HEAD']


async def findbranch(mainbranch: str, rdir: Path) -> List[Tuple[Path, str]]:
    """
    find all branches in tree not matching "mainbranch"

    Parameters
    ----------

    mainbranch : str
        branch name that's "normal" e.g. master
    rdir : pathlib.Path
        top-level directory to work under e.g. ~/code/

    Results
    -------

    branch : list of tuple of pathlib.Path, str
        repo paths and branch names

    asyncio.get_child_watcher() must be instantiated by calling function:
    https://docs.python.org/3/library/asyncio-subprocess.html#subprocess-and-threads
    """

    rdir = Path(rdir).expanduser()

    dirs = (x for x in rdir.iterdir() if not baddir(x))

    futures = [_arbiter(mainbranch, d) for d in dirs]

    branch = await asyncio.gather(*futures)

    non_mainbranch = []
    for r, b in branch:
        if b:
            non_mainbranch.append((r, b))

    return non_mainbranch


async def _arbiter(mainbranch: str, path: Path) -> Tuple[Path, str]:

    try:
        tup = await asyncio.wait_for(_worker(mainbranch, path), timeout=5.0)
    except (asyncio.TimeoutError, FileNotFoundError, PermissionError) as e:
        logging.error(f'{path}   {e}')
        tup = (path, '')

    return tup


async def _worker(mainbranch: str, path: Path) -> Tuple[Path, str]:

    proc = await asyncio.create_subprocess_exec(*CMD, cwd=path,
                                                stdout=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()

    branchname = stdout.decode('utf8').rstrip()

    tup = (path, '') if mainbranch in branchname else (path, branchname)

    return tup
