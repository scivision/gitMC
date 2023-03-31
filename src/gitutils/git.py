"""
Git utilities: focused on speed for very large numbers of Git repos
"""

from __future__ import annotations
from pathlib import Path
import subprocess
import typing
import shutil
import functools

# from colorama.
MAGENTA = "\x1b[45m"
BLACK = "\x1b[40m"

TIMEOUT = {
    "remote": 30.0,  # [seconds] arbitrary delay for network operations
    "local": 5.0,  # [seconds] local operations should be fast
}


@functools.cache
def git_exe() -> str:
    """
    find Git executable

    Returns
    -------
    exe : str
        path to Git executable
    """

    if not (exe := shutil.which("git")):
        raise EnvironmentError("Git not found")

    try:
        subprocess.check_call(
            [exe, "-C", ".", "--version"], stdout=subprocess.DEVNULL, timeout=TIMEOUT["local"]
        )
        # stdout>NULL to avoid leaking version into pipe
    except subprocess.CalledProcessError:
        raise EnvironmentError("Git version is too old.")

    return exe


def gitdirs(path: Path) -> typing.Iterator[Path]:
    """
    Generator for Git directories

    Parameters
    ----------
    path: pathlib.Path
        top-level Git directory

    Yields
    ------
    dirs : generator
        generator for Git repo paths
    """

    path = Path(path).expanduser().resolve(strict=True)

    if baddir(path):  # assume top-level dir under which Git repos live
        for x in path.iterdir():
            if not baddir(x):
                yield x
    else:
        yield path


def baddir(path: Path) -> bool:
    """
    tells if a directory is not a Git repo or excluded.
    A directory with top-level file ".nogit" is excluded.
    Treats PermissionError as bad -- happens on Windows.

    Parameters
    ----------

    path : pathlib.Path
        path to check if it's a Git repo

    Results
    -------

    bad : bool
        True if an excluded Git repo or not a Git repo
    """

    path = path.expanduser()

    try:
        if not path.is_dir():
            return True
    except PermissionError:
        return True

    try:
        bad = (path / ".nogit").is_file() or not (path / ".git" / "HEAD").is_file()
    except PermissionError:
        bad = True

    return bad


def list_changed(path: Path) -> list[str]:
    """very quick check if any files were modified in this Git repo

    Parameters
    ----------
    path : pathlib.Path
        path to Git repo

    Results
    -------

    changes : list of str
        filenames changed in this Git repo
    """

    if not path.is_dir():
        raise NotADirectoryError(path)

    cmd = [git_exe(), "-C", str(path), "ls-files", "--modified"]
    # .strip() avoids returning a blank last element
    if ret := subprocess.check_output(
        cmd, text=True, errors="ignore", timeout=TIMEOUT["local"]
    ).strip():
        return ret.split("\n")

    return []
