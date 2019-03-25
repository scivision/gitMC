"""
These Git utilities use nothing beyond pure Python and command-line Git.
Speed is emphasized throughout, with pipelining and concurrent `asyncio` routines throughout
for fastest operation on large numbers of repos.
"""
from pathlib import Path
from typing import List
import shutil

from .git import listchanged  # noqa: F401
from .branch import findbranch  # noqa: F401
from .email import gitemail  # noqa: F401
from .pull import fetchpull  # noqa: F401
from .push import gitpushall  # noqa: F401


def find_dir_missing_file(fn: str, path: Path, copyfile: Path = None) -> List[Path]:
    """
    if directory is missing a file, copy the file to that directory

    Parameters
    ----------
    fn : pathlib.Path
        filename to look for
    path : pathlib.Path
        top-level directory to check directories under
    copyfile : pathlib.Path, optional
        if present, copy this file into the directory that doesn't have it

    Results
    -------
    missing : list of pathlib.Path
        directories that were missing the file and it wasn't copied there.
    """
    path = Path(path).expanduser()

    dlist = (x for x in path.iterdir() if x.is_dir())

    missing = []
    for d in dlist:
        if not (d / fn).is_file():
            if isinstance(copyfile, Path):
                shutil.copy(copyfile, d)
                print('copied', copyfile, 'to', d)
            else:
                missing.append(d)

    return missing
