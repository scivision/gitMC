"""
Git fetch / pull functions
"""

from __future__ import annotations
import argparse
import asyncio
import subprocess
import logging
from pathlib import Path

from . import _log
from .git import GITEXE, gitdirs


async def fetchpull(mode: str, path: Path) -> Path:
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
        Git repo that failed to fetch/pull


    Reference:
    ----------
    format mini-language:
    https://docs.python.org/3/library/string.html#format-specification-mini-language


    Note: Don't use git pull --quiet because you get no output at all when remote change
    occured. Leave it as is with stdout=DEVNULL and no --quiet.
    """

    cmd = [GITEXE, "-C", str(path), mode]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    stdout, stderr = await proc.communicate()
    out = stdout.decode("utf8", errors="ignore").rstrip()
    if out and out != "Already up to date.":
        print(path.name, out)

    if mode == "fetch" and proc.returncode == 0:
        cmd = [GITEXE, "-C", str(path), "diff", "--stat", "HEAD..FETCH_HEAD"]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.DEVNULL,
        )
        stdout, stderr = await proc.communicate()
        out = stdout.decode("utf8", errors="ignore").rstrip()
        if out:
            print(path.name, out)
    err = stderr.decode("utf8", errors="ignore").rstrip()
    if proc.returncode:
        if "Permission denied" in err or "fatal: could not read Password" in err:
            logging.info(f"SKIP: credentials needed: {path.name}")
            return None

        logging.error(f"{path.name}  {err}")
        return path

    logging.info(f"{mode} {path.name}")
    return None


async def git_pullfetch(mode: str, path: Path) -> list[Path]:

    failed = []
    for r in asyncio.as_completed([fetchpull(mode, d) for d in gitdirs(path)]):
        fail = await r
        if fail:
            failed.append(fail)
            print(fail.name)

    return failed


def git_fetch_cli():
    p = argparse.ArgumentParser()
    p.add_argument("path", help="path to look under", nargs="?", default="~/code")
    p.add_argument("-v", "--verbose", action="store_true")
    P = p.parse_args()

    _log(P.verbose)

    asyncio.run(git_pullfetch("fetch", P.path))


def git_pull_cli():
    p = argparse.ArgumentParser()
    p.add_argument("path", help="path to look under", nargs="?", default="~/code")
    p.add_argument("-v", "--verbose", action="store_true")
    P = p.parse_args()

    _log(P.verbose)

    asyncio.run(git_pullfetch("pull", P.path))


if __name__ == "__main__":
    git_pull_cli()
