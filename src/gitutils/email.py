"""
operations for Git author attributions
"""

from __future__ import annotations
from pathlib import Path
import typing as T
import collections
import logging
import subprocess

from .git import gitdirs, GITEXE, TIMEOUT


def gitemail(path: Path, exclude: str = None) -> T.Iterator[tuple[Path, list[tuple[str, int]]]]:
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
                [GITEXE, "-C", str(d), "log", '--pretty="%ce"'], text=True, timeout=TIMEOUT
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
