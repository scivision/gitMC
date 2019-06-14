"""
Git fetch / pull functions
"""
import asyncio
import subprocess
from pathlib import Path
from typing import AsyncGenerator, Tuple

from .git import GITEXE, gitdirs


async def fetchpull(mode: str, rdir: Path,
                    verbose: bool = False) -> AsyncGenerator[Tuple[str, str], None]:
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
    """

    for d in gitdirs(rdir):
        if verbose:
            print(mode, d.name)
        proc = await asyncio.create_subprocess_exec(*[GITEXE, '-C', str(d), mode],
                                                    stdout=subprocess.DEVNULL,
                                                    stderr=asyncio.subprocess.PIPE)
        _, stderr = await proc.communicate()
        err = stderr.decode('utf8').rstrip()

        if proc.returncode:
            yield d.name, err
