"""
detect Git local repo modifications
"""

from __future__ import annotations
import argparse
import typing
from pathlib import Path
import asyncio
from pprint import pprint

import pygit2

from . import _log
from .git import gitdirs
from .status_cmd import git_status_serial, git_status_async


def git_status(path: Path, verbose: bool) -> typing.Iterator[dict]:

    for d in gitdirs(path):
        repo = pygit2.Repository(d)
        if status := repo.status():
            yield status


def cli():
    p = argparse.ArgumentParser(description="get status of many Git repos")
    p.add_argument("path", help="path to look under", nargs="?", default="~/code")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("-t", "--timeout", type=float)
    p.add_argument(
        "-method",
        help="use Git command line serial execution",
        choices=["pygit2", "serial", "async"], default="pygit2",
    )
    P = p.parse_args()

    _log(P.verbose)

    if P.method == "pygit2":
        for s in git_status(P.path, P.verbose):
            pprint(s)
    elif P.method == "serial":
        for d in gitdirs(P.path):
            if changes := git_status_serial(d, P.timeout):
                print(changes[0])
                if P.verbose:
                    print(changes[1])
    elif P.method == "async":
        asyncio.run(git_status_async(P.path, P.verbose, P.timeout))


if __name__ == "__main__":
    cli()
