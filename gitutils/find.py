from pathlib import Path
import typing
import shutil


def find_dir_missing_file(fn: str, path: Path, copyfile: Path = None) -> typing.List[Path]:
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

    Results
    -------
    missing : list of pathlib.Path
        directories that were missing the file and it wasn't copied there.
    """
    path = Path(path).expanduser()
    if not path.is_dir():
        raise NotADirectoryError(path)

    dlist = (x for x in path.iterdir() if x.is_dir())

    missing = []  # type: typing.List[Path]
    for d in dlist:
        if not (d / fn).is_file():
            if isinstance(copyfile, Path):
                shutil.copy(copyfile, d)
                print('copied', copyfile, 'to', d)
            else:
                missing.append(d)

    return missing
