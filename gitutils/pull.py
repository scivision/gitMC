"""
Git fetch / pull functions
"""
from pathlib import Path
from typing import Iterator, Tuple
import subprocess
from .git import GITEXE, gitdirs, TIMEOUT


def fetchpull(mode: str, rdir: Path) -> Iterator[Tuple[Path, str]]:
    """
    handles recursive "git pull" and "git fetch"

    Parameters
    ----------

    mode : str
        fetch or pull
    rdir : pathlib.Path
        top-level path over Git repos

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
        try:
            # don't use timeout as it doesn't work right when waiting for user input (password)
            ret = subprocess.run([GITEXE] + mode.split(), cwd=d,
                                 universal_newlines=True,
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.PIPE,
                                 timeout=TIMEOUT)

            if ret.stderr:
                yield d, ret.stderr
        except subprocess.CalledProcessError as e:
            yield d, e.output
