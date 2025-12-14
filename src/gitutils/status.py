"""
detect Git local repo modifications
"""

import argparse
from collections.abc import Iterator
from pathlib import Path
import asyncio
from pprint import pprint

import pygit2

from . import _log
from .git import gitdirs, MAX_CONCURRENT
from .status_cmd import git_status_serial, git_status_async


def git_status(path: Path, verbose: bool) -> Iterator[tuple[Path, dict]]:

    for d in gitdirs(path):
        repo = pygit2.Repository(d)
        if status := repo.status():
            yield d, status


def cli():
    p = argparse.ArgumentParser(description="get status of many Git repos")
    p.add_argument("path", help="path to look under", nargs="?", default="~/code")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("-t", "--timeout", type=float)
    p.add_argument(
        "-method",
        help="use Git command line serial execution",
        choices=["pygit2", "serial", "async"],
        default="pygit2",
    )
    p.add_argument(
        "-m",
        "--max-concurrent",
        type=int,
        default=MAX_CONCURRENT,
        help="maximum concurrent Git commands",
    )
    P = p.parse_args()

    _log(P.verbose)

    if P.method == "pygit2":
        for d, s in git_status(P.path, P.verbose):
            print(str(d))
            pprint(s)
    elif P.method == "serial":
        for d in gitdirs(P.path):
            if changes := git_status_serial(d, P.timeout):
                print(changes[0])
                if P.verbose:
                    print(changes[1])
    elif P.method == "async":
        asyncio.run(
            git_status_async(P.path, P.verbose, timeout=P.timeout, max_concurrent=P.max_concurrent)
        )


if __name__ == "__main__":
    cli()
