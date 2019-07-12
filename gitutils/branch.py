"""
Operations for Git branches

git branch get name methods:
https://stackoverflow.com/a/45028375
"""

import typing
from pathlib import Path
import asyncio
import logging

from .git import GITEXE, gitdirs

BRANCH_REV = ['rev-parse', '--abbrev-ref', 'HEAD']
BRANCH_SYM = ['symbolic-ref', '--short', 'HEAD']
BRANCH_NAME = ['name-rev', '--name-only', 'HEAD']
BRANCH_SIMPLE = ['branch', '--show-current']  # Git >= 2.22


async def different_branch(mainbranch: str, path: Path) -> typing.Tuple[str, str]:
    """
    does branch not match "mainbranch"

    Parameters
    ----------

    mainbranch : str
        branch name that's "normal" e.g. master
    path : pathlib.Path
        Git repo to check

    Returns
    -------

    branch : tuple of pathlib.Path, str
        repo path and branch name

    asyncio.get_child_watcher() must be instantiated by calling function:
    https://docs.python.org/3/library/asyncio-subprocess.html#subprocess-and-threads
    """

    proc = await asyncio.create_subprocess_exec(*[GITEXE, '-C', str(path)] + BRANCH_REV,
                                                stdout=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    logging.info(str(path))

    branchname = stdout.decode('utf8').rstrip()

    if mainbranch != branchname:
        return path.name, branchname
    return None


async def coro_local(branch: str, path: Path) -> typing.List[Path]:
    futures = [different_branch(branch, d) for d in gitdirs(path)]
    return list(filter(None, await asyncio.gather(*futures)))
