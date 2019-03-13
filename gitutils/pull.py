"""
Git fetch / pull functions
"""
from pathlib import Path
from typing import Iterator
import subprocess

from .git import GITEXE, gitdirs, TIMEOUT


def fetchpull(mode: str, rdir: Path, verbose: bool = False) -> Iterator[Path]:
    """
    handles recursive "git pull" and "git fetch"

    Parameters
    ----------

    mode : str
        fetch or pull
    rdir : pathlib.Path
        top-level path over Git repos
    verbose : bool
        verbosity

    Yields
    ------
    failed : Path
        Git repos with failures


    Reference:
    ----------
    format mini-language:
    https://docs.python.org/3/library/string.html#format-specification-mini-language
    """
    # Lmax = len(max(map(attrgetter('name'), dlist), key=len))

    for d in gitdirs(rdir):
        # assumes console is at least 80 characters wide
        if verbose:
            print(f' --> {d.name:<80}', end="", flush=True)
        try:
            # don't use timeout as it doesn't work right when waiting for user input (password)
            ret = subprocess.run([GITEXE] + mode.split(), cwd=d,
                                 universal_newlines=True,
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.PIPE,
                                 timeout=TIMEOUT)

            if ret.stderr:
                print(d.name)
                print(ret.stderr)
                yield d
            elif verbose:
                print(end="\r")

        except subprocess.CalledProcessError as e:
            print(f'{d.name}  {e}')
            yield d
