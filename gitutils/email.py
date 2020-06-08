"""
operations for Git author attributions
"""
from pathlib import Path
import typing as T
import collections
import logging
import subprocess

from .git import gitdirs, GITEXE, TIMEOUT

R = Path(__file__).parent


def gitemail(path: Path, exclude: str = None) -> T.Iterator[T.Tuple[Path, T.List[T.Tuple[str, int]]]]:
    """
    returns email addresses of everyone who ever made a Git commit in this repo.

    Parameters
    ----------

    path : pathlib.Path
        path to Git repo
    exclude : list of str or tuple of str
        email addresses to exclude

    Yields
    ------
    d : pathlib.Path
        path to the Git repo
    emails : tuple of str, int
        email addresses with how many times they committed
    """

    for d in gitdirs(path):

        try:
            ret = subprocess.check_output([GITEXE, "-C", str(d), "log", '--pretty="%ce"'], universal_newlines=True, timeout=TIMEOUT)
        except subprocess.CalledProcessError as e:
            logging.error(f"{path}  {e}")
            continue

        ret = ret.replace('"', "")
        addrs = filter(None, ret.split("\n"))  # remove blanks
        if exclude:
            addrs = (n for n in addrs if not n.startswith(exclude))

        emails = collections.Counter(addrs).most_common()

        yield d, emails


def amend(path: Path, emails: T.Sequence[str], user: str):
    assert isinstance(user, str)

    github = "@users.noreply.github.com"

    for email in emails:
        if email != user + github:
            cmd = [str(R / "amender.sh"), email, user]
            subprocess.check_call(cmd, cwd=path)
