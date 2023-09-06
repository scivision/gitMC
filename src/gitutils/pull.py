"""
Git fetch / pull functions
"""

from __future__ import annotations
import argparse
import asyncio
import logging
from pathlib import Path
import urllib.request
import socket
import os
import functools

from . import _log
from .git import git_exe, gitdirs, TIMEOUT


def check_internet() -> bool:
    """
    check that Internet connection is working
    """

    url = "https://connectivitycheck.gstatic.com/generate_204"

    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            if resp.getcode() == 204:
                return True
    except (socket.gaierror, urllib.error.URLError):
        raise ConnectionError(f"No internet connection to {url}")

    return False


@functools.cache
def set_env(prompt: bool) -> dict:
    env = None
    if not prompt:
        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = "0"
        env["GIT_SSH_COMMAND"] = "ssh -o BatchMode=yes"


async def execute_process(
    cmd: list[str], prompt: bool = False, timeout: float = TIMEOUT["remote"]
) -> tuple[int, str, str]:
    """
    GIT_TERMINAL_PROMPT=0 disallows spurious Git https password prompts
    https://github.blog/2015-02-06-git-2-3-has-been-released/#the-credential-subsystem-is-now-friendlier-to-scripting
    GIT_SSH_COMMAND handles the Git SSH calls
    """

    env = set_env(prompt)

    proc = await asyncio.wait_for(
        asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, env=env
        ),
        timeout=timeout,
    )
    stdout, stderr = await proc.communicate()
    code = proc.returncode
    if code is None:
        code = 1

    return (
        code,
        stdout.decode("utf8", errors="ignore").rstrip(),
        stderr.decode("utf8", errors="ignore").rstrip(),
    )


async def fetchpull(mode: str, path: Path, prompt: bool, timeout: float) -> Path | None:
    """
    handles recursive "git pull" and "git fetch"

    Parameters
    ----------

    mode : str
        fetch or pull
    path : pathlib.Path
        Git repo path
    prompt : bool
        if True, skip directories that require credentials

    Returns
    -------
    failed : pathlib.Path
        Git repo that failed to fetch/pull
    """

    """
    Don't use "git pull --quiet" since no output at all if remote change occured.
    """

    # %% pull or fetch
    try:
        code, out, err = await execute_process([git_exe(), "-C", str(path), mode], prompt, timeout)
    except TimeoutError:
        logging.error(f"Timeout: {path.name}")
        return path

    if code != 0:
        # fetch or pull failed
        if "Permission denied" in err or "fatal: could not read Password" in err:
            print(f"SKIP: credentials needed: {path.name}")
            return None

        logging.error(f"{path.name} {code} {err}")
        return path
    # %% let user know they have unmerged changes
    if mode == "fetch":
        code, out, err = await execute_process(
            [git_exe(), "-C", str(path), "diff", "--stat", "HEAD..FETCH_HEAD"],
            timeout=timeout,
        )
        if out:
            print(path.name, out)
    else:
        if out != "Already up to date.":
            print(path.name, out)

    logging.info(f"{mode} {path.name}")

    return None


async def git_pullfetch(mode: str, path: Path, prompt: bool, timeout: float) -> list[Path]:
    failed = []
    futures = [fetchpull(mode, d, prompt, timeout) for d in gitdirs(path)]
    for r in asyncio.as_completed(futures):
        if fail := await r:
            failed.append(fail)
            print(fail.name)

    return failed


def git_fetch_cli():
    p = argparse.ArgumentParser()
    p.add_argument("path", help="path to look under", nargs="?", default="~/code")
    p.add_argument(
        "-b",
        "--prompt",
        help="if True, prompt for directories that need remote credentials",
        action="store_true",
    )
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("-t", "--timeout", type=float, default=TIMEOUT["remote"])
    P = p.parse_args()

    _log(P.verbose)

    asyncio.run(git_pullfetch("fetch", P.path, P.prompt, timeout=P.timeout))


def git_pull_cli():
    p = argparse.ArgumentParser()
    p.add_argument("path", help="path to look under", nargs="?", default="~/code")
    p.add_argument(
        "-p",
        "--prompt",
        help="if True, prompt for directories that need remote credentials",
        action="store_true",
    )
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("-t", "--timeout", type=float, default=TIMEOUT["remote"])
    P = p.parse_args()

    _log(P.verbose)

    # if not check_internet():
    #     raise ConnectionError("No internet connection")

    asyncio.run(git_pullfetch("pull", P.path, P.prompt, timeout=P.timeout))


if __name__ == "__main__":
    git_pull_cli()
