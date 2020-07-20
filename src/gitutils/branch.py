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

BRANCH_REV = ["rev-parse", "--abbrev-ref", "HEAD"]
BRANCH_SYM = ["symbolic-ref", "--short", "HEAD"]
BRANCH_NAME = ["name-rev", "--name-only", "HEAD"]
BRANCH_SIMPLE = ["branch", "--show-current"]  # Git >= 2.22


async def different_branch(main: str, path: Path) -> typing.Tuple[str, str]:
    """
    does branch not match "main"

    Parameters
    ----------

    main : str
        desired default branch name
    path : pathlib.Path
        Git repo to check

    Returns
    -------

    branch : tuple of pathlib.Path, str
        repo path and branch name

    asyncio.get_child_watcher() must be instantiated by calling function:
    https://docs.python.org/3/library/asyncio-subprocess.html#subprocess-and-threads
    """

    proc = await asyncio.create_subprocess_exec(*[GITEXE, "-C", str(path)] + BRANCH_SIMPLE, stdout=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    if proc.returncode != 0:
        logging.error(f"{path.name} return code {proc.returncode}  {BRANCH_SIMPLE}")
    logging.info(str(path))

    branch_name = stdout.decode("utf8").strip()

    if main != branch_name:
        return path.name, branch_name
    return None


async def coro_branch(branch: str, path: Path) -> typing.List[Path]:
    futures = [different_branch(branch, d) for d in gitdirs(path)]
    return list(filter(None, await asyncio.gather(*futures)))
