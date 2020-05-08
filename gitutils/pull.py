"""
Git fetch / pull functions
"""
import asyncio
import subprocess
import logging
import sys
from pathlib import Path
import typing

from .git import GITEXE, gitdirs


async def fetchpull(mode: typing.List[str], path: Path) -> Path:
    """
    handles recursive "git pull" and "git fetch"

    Parameters
    ----------

    mode : str, list of str
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

    cmd = [GITEXE, "-C", str(path)] + mode
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
    _, stderr = await proc.communicate()
    if proc.returncode == 0:
        logging.info(f"{mode} {path.name}")
    else:
        logging.info(f"{mode} {path.name} return code {proc.returncode}")

    err = stderr.decode("utf8", errors="ignore").rstrip()
    if proc.returncode:
        if "Permission denied" in err:
            print("SKIP: credentials needed:", path.name, file=sys.stderr)
        else:
            print(path.name, err, file=sys.stderr)
        return path
    return None


async def coro_remote(mode: typing.List[str], path: Path) -> typing.List[Path]:
    futures = [fetchpull(mode, d) for d in gitdirs(path)]
    return list(filter(None, await asyncio.gather(*futures)))
