from typing import List, Tuple
from pathlib import Path
import subprocess

from .git import baddir


def findbranch(ok: str, rdir: Path) -> List[Tuple[Path, str]]:
    """find all branches in tree not matching ok

    Parameters
    ----------

    ok : str
        branch name that's "normal" e.g. master
    rdir : pathlib.Path
        top-level directory to work under e.g. ~/code/

    Results
    -------

    branch : list of tuple of pathlib.Path, str
        repo paths and branch names
    """

    rdir = Path(rdir).expanduser()

    cmd = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']

    dlist = [x for x in rdir.iterdir() if not baddir(x)]

    if not dlist:
        if not baddir(rdir):
            dlist = [rdir]
        else:
            raise FileNotFoundError(f'no Git repos found under {rdir}')

    branch = []
    for d in dlist:
        try:
            ret = subprocess.check_output(cmd, cwd=d,
                                          universal_newlines=True).rstrip()

            if ok not in ret:
                branch.append((d, ret))
        except subprocess.CalledProcessError as e:
            print(d, e)

    return branch
