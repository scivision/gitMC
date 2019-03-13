from pathlib import Path
from typing import Tuple, List, Optional
import collections
import logging
import subprocess

from .git import baddir, GITEXE


def gitemail(path: Path, exclude: str = None) -> Optional[List[Tuple[str, int]]]:
    """
    returns email addresses of everyone who ever made a Git commit in this repo.

    Parameters
    ----------

    path : pathlib.Path
        path to Git repo
    exclude : list of str or tuple of str
        email addresses to exclude

    Results
    -------

    emails : list of tuple of str, int
        email addresses with how many times they committed
    """
    path = Path(path).expanduser().resolve()

    if baddir(path):
        raise FileNotFoundError(f'no Git repos found under {path}')

    assert isinstance(GITEXE, str)
    cmd = [GITEXE, 'log', '--pretty="%ce"']

    try:
        ret = subprocess.check_output(cmd, cwd=path, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        logging.error(f'{path}  {e}')
        return None

    ret = ret.replace('"', '')
    ret = filter(None, ret.split('\n'))  # remove blanks
    if exclude:
        ret = (n for n in ret if not n.startswith(exclude))

    emails = collections.Counter(ret).most_common()

    return emails
