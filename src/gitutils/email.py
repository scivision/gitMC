"""
operations for Git author attributions
"""

from __future__ import annotations
from pathlib import Path
import typing as T
import collections
import logging
import subprocess
import argparse

from .git import gitdirs, git_exe, TIMEOUT, MAGENTA, BLACK
from . import _log


def gitemail(
    path: Path, exclude: str | None = None, timeout=TIMEOUT["local"]
) -> T.Iterator[tuple[Path, list[tuple[str, int]]]]:
    """
    returns email addresses of everyone who ever made a Git commit in this repo.

    Parameters
    ----------

    path : pathlib.Path
        path to Git repo
    exclude : list of str or tuple of str
        email addresses to exclude

    Yields
    ------
    d : pathlib.Path
        path to the Git repo
    emails : tuple of str, int
        email addresses with how many times they committed
    """

    for d in gitdirs(path):
        try:
            ret = subprocess.check_output(
                [git_exe(), "-C", str(d), "log", '--pretty="%ce"'],
                text=True,
                timeout=timeout,
            )
        except subprocess.CalledProcessError as e:
            logging.error(f"{path}  {e}")
            continue

        addrs: T.Iterable[str] = filter(None, ret.replace('"', "").split("\n"))
        # remove blanks
        if exclude:
            addrs = (n for n in addrs if not n.startswith(exclude))

        emails = collections.Counter(addrs).most_common()

        yield d, emails


def cli():
    p = argparse.ArgumentParser()
    p.add_argument("path", help="path to look under", nargs="?", default="~/code")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("-e", "--exclude", help="user to ignore (keep)")
    p.add_argument("-t", "--timeout", help="timeout for git commands", type=float)
    P = p.parse_args()

    _log(P.verbose)

    for d, emails in gitemail(P.path, P.exclude, timeout=P.timeout):
        print(MAGENTA + d.stem + BLACK)
        for email in emails:
            print(*email)


if __name__ == "__main__":
    cli()
