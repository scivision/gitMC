from pathlib import Path
from typing import Sequence, Tuple, List
import collections
import subprocess

from .git import baddir, MAGENTA, BLACK, GITEXE


def gitemail(path: Path, exclude: Sequence[str] = None) -> List[Tuple[str, int]]:
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

    ret = subprocess.check_output(cmd, cwd=path, universal_newlines=True)
    ret = ret.replace('"', '')
    ret = filter(None, ret.split('\n'))  # remove blanks

    # rset = set(ret)
    # emails = list(rset.difference(set(exclude))) if exclude else list(rset)

    emails = collections.Counter(ret).most_common()
# %% output
    print(MAGENTA + path.stem + BLACK)

    for email in emails:
        print(email[0], email[1])

    return emails
