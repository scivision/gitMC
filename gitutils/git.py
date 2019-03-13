"""
Git utilities: focused on speed for very large numbers of Git repos
"""
from pathlib import Path
import subprocess
from typing import List, Iterator, Any
import shutil

try:
    import colorama
    MAGENTA = colorama.Back.MAGENTA
    BLACK = colorama.Back.BLACK
    colorama.init()
except ImportError:
    MAGENTA = BLACK = ''

TIMEOUT = 30.  # arbitrary, seconds
GITEXE: Any = shutil.which('git')  # type: ignore
if not GITEXE:
    raise FileNotFoundError('Could not find executable for Git')

"""
replaced by git status --porcelain:
  ['git','ls-files','-o','-d','--exclude-standard']): # check for uncommitted files
  ['git','--no-pager','diff','HEAD'], # check for uncommitted work

DOES NOT WORK ['git','log','--branches','--not','--remotes'],     # check for uncommitted branches
"""


def gitdirs(path: Path) -> Iterator[Path]:
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

    path = Path(path).expanduser().resolve()

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
        bad = (path / '.nogit').is_file() or not (path / '.git' / 'HEAD').is_file()
    except PermissionError:
        bad = True

    return bad


def listchanged(path: Path) -> List[str]:
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
    ret = subprocess.check_output(['git', 'ls-files', '--modified'],
                                  universal_newlines=True,
                                  cwd=path)

    changes = ret.split('\n')

    return changes
