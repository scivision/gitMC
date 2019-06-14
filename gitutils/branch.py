"""
Operations for Git branches

git branch get name methods:
https://stackoverflow.com/a/45028375
"""

from typing import AsyncGenerator, Tuple
from pathlib import Path
import asyncio

from .git import GITEXE, gitdirs

BRANCH_REV = ['rev-parse', '--abbrev-ref', 'HEAD']
BRANCH_SYM = ['symbolic-ref', '--short', 'HEAD']
BRANCH_NAME = ['name-rev', '--name-only', 'HEAD']
BRANCH_SIMPLE = ['branch', '--show-current']  # Git >= 2.22


async def findbranch(mainbranch: str, rdir: Path) -> AsyncGenerator[Tuple[str, str], None]:
    """
    find all branches in tree not matching "mainbranch"

    Parameters
    ----------

    mainbranch : str
        branch name that's "normal" e.g. master
    rdir : pathlib.Path
        top-level directory to work under e.g. ~/code/

    Yields
    ------

    branch : tuple of pathlib.Path, str
        repo path and branch name

    asyncio.get_child_watcher() must be instantiated by calling function:
    https://docs.python.org/3/library/asyncio-subprocess.html#subprocess-and-threads
    """

    rdir = Path(rdir).expanduser()

    for d in gitdirs(rdir):
        proc = await asyncio.create_subprocess_exec(*[GITEXE, '-C', str(d)] + BRANCH_REV,
                                                    stdout=asyncio.subprocess.PIPE)
        stdout, _ = await proc.communicate()

        branchname = stdout.decode('utf8').rstrip()

        if mainbranch in branchname:
            continue

        yield d.name, branchname
