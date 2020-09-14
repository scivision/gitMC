"""
Operations for Git branches

git branch get name methods:
https://stackoverflow.com/a/45028375
"""

import argparse
import typing as T
from pathlib import Path
import asyncio
import logging

from . import _log
from .git import GITEXE, gitdirs

BRANCH_REV = ["rev-parse", "--abbrev-ref", "HEAD"]
BRANCH_SYM = ["symbolic-ref", "--short", "HEAD"]
BRANCH_NAME = ["name-rev", "--name-only", "HEAD"]
BRANCH_SIMPLE = ["branch", "--show-current"]  # Git >= 2.22


async def different_branch(main: str, path: Path) -> T.Tuple[str, str]:
    """
    does branch not match specified name

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


async def git_branch(branch: str, path: Path) -> T.List[T.Tuple[str, str]]:

    different = []
    for r in asyncio.as_completed([different_branch(branch, d) for d in gitdirs(path)]):
        diff = await r
        if diff:
            different.append(diff)
            print(diff)

    return different


def cli():
    """
    report on git repos not on the expected branch e.g. 'master'
    """

    p = argparse.ArgumentParser()
    p.add_argument("path", help="path to look under", nargs="?", default="~/code")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("mainbranch", nargs="?", default="master", help="name of your main branch")
    P = p.parse_args()

    _log(P.verbose)

    asyncio.run(git_branch(P.mainbranch, P.path))


if __name__ == "__main__":
    cli()
