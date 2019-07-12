"""
Git fetch / pull functions
"""
import asyncio
import subprocess
import logging
from pathlib import Path
import typing

from .git import GITEXE, gitdirs


async def fetchpull(mode: typing.List[str], path: Path) -> Path:
    """
    handles recursive "git pull" and "git fetch"

    Parameters
    ----------

    mode : str
        fetch or pull
    path : pathlib.Path
        Git repo path

    Returns
    -------
    failed : pathlib.Path
        Git repos with failures


    Reference:
    ----------
    format mini-language:
    https://docs.python.org/3/library/string.html#format-specification-mini-language


    Note: Don't use git pull --quiet because you get no output at all when remote change
    occured. Leave it as is with stdout=DEVNULL and no --quiet.
    """
    if isinstance(mode, str):
        mode = [mode]

    cmd = [GITEXE, '-C', str(path)] + mode
    proc = await asyncio.create_subprocess_exec(*cmd,
                                                stdout=subprocess.DEVNULL,
                                                stderr=asyncio.subprocess.PIPE)
    _, stderr = await proc.communicate()
    logging.info(f'{mode} {path.name}')

    err = stderr.decode('utf8').rstrip()
    if proc.returncode:
        print(path.name, err)
        return path
    return None


async def coro_remote(mode: typing.List[str], path: Path) -> typing.List[Path]:
    futures = [fetchpull(mode, d) for d in gitdirs(path)]
    return list(filter(None, await asyncio.gather(*futures)))
