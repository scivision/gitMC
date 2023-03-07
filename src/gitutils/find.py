from __future__ import annotations
from pathlib import Path
import typing as T
import shutil


def find_matching_file(path: Path, fn: str) -> T.Iterator[Path]:
    """
    if full path file is found, return that filename

    Parameters
    ----------
    path : pathlib.Path
        top-level directory to check directories under
    fn : str
        filename to look for

    Yields
    -------
    matched : pathlib.Path
        full path to matching file
    """

    path = Path(path).expanduser().resolve()
    if not path.is_dir():
        raise NotADirectoryError(path)

    for d in (x for x in path.iterdir() if x.is_dir()):
        if (d / fn).is_file():
            yield d


def find_dir_missing_file(path: Path, fn: str, copyfile: Path | None = None) -> T.Iterator[Path]:
    """
    if directory is missing a file, copy the file to that directory

    Parameters
    ----------
    path : pathlib.Path
        top-level directory to check directories under
    fn : str
        filename to look for
    copyfile : pathlib.Path, optional
        if present, copy this file into the directory that doesn't have it

    Yields
    -------
    missing : pathlib.Path
        directories missing the file
    """

    path = Path(path).expanduser().resolve()
    if not path.is_dir():
        raise NotADirectoryError(path)

    for d in (x for x in path.iterdir() if x.is_dir()):
        if not (d / fn).is_file():
            if copyfile:
                shutil.copy2(copyfile, d)
                print(f"copied {copyfile} to {d}")

            yield d
