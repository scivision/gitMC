"""
Git fetch / pull functions
"""
import asyncio
import subprocess
import logging
from pathlib import Path
from typing import AsyncGenerator, Tuple, List

from .git import GITEXE, gitdirs, MAGENTA, BLACK


async def fetchpull(mode: List[str], rdir: Path) -> AsyncGenerator[Tuple[str, str], None]:
    """
    handles recursive "git pull" and "git fetch"

    Parameters
    ----------

    mode : str
        fetch or pull
    rdir : pathlib.Path
        top-level path over Git repos
    verbose: bool
        print repo being checked

    Yields
    ------
    failed : Path
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

    for d in gitdirs(rdir):
        logging.info(f'{mode} {d.name}')
        cmd = [GITEXE, '-C', str(d)] + mode

        proc = await asyncio.create_subprocess_exec(*cmd,
                                                    stdout=subprocess.DEVNULL,
                                                    stderr=asyncio.subprocess.PIPE)
        _, stderr = await proc.communicate()
        err = stderr.decode('utf8').rstrip()

        if proc.returncode:
            yield d.name, err


async def find_remote(mode: List[str], path: Path):

    async for d, v in fetchpull(mode, path):
        print(MAGENTA + str(d))
        print(BLACK + v)
