from pathlib import Path
import typing
import shutil


def find_dir_missing_file(fn: str, path: Path, copyfile: Path = None) -> typing.Iterator[Path]:
    """
    if directory is missing a file, copy the file to that directory

    Parameters
    ----------
    fn : str
        filename to look for
    path : pathlib.Path
        top-level directory to check directories under
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
    if copyfile and not isinstance(copyfile, Path):
        raise TypeError("copyfile must be Path or None")

    dlist = (x for x in path.iterdir() if x.is_dir())

    for d in dlist:
        if not (d / fn).is_file():
            if isinstance(copyfile, Path):
                shutil.copy2(copyfile, d)
                print(f"copied {copyfile} to {d}")

            yield d
