from operator import attrgetter
from pathlib import Path
from typing import List
import subprocess
import logging
from time import sleep
from sys import stderr

from .git import baddir, GITEXE


def fetchpull(mode: str, rdir: Path) -> List[str]:
    """
    handles recursive "git pull" and "git fetch"

    Parameters
    ----------

    mode : str
        fetch or pull
    rdir : pathlib.Path
        top-level path over Git repos

    Results
    -------

    failed : list of str
        names of Git repos with failures


    Reference:
    ----------
    format mini-language:
    https://docs.python.org/3/library/string.html#format-specification-mini-language
    """
    # leave .resolve() for useful error messages
    rdir = Path(rdir).expanduser().resolve()

    dlist = [x for x in rdir.iterdir() if not baddir(x)]

    if not dlist:
        if not baddir(rdir):
            dlist = [rdir]
        else:
            raise FileNotFoundError(f'no Git repos found under {rdir}')

    Lmax = len(max(map(attrgetter('name'), dlist), key=len))
    print('git', mode, len(dlist), 'paths under', rdir)

    failed = []
    assert isinstance(GITEXE, str)

    for d in dlist:

        print(f' --> {d.name:<{Lmax}}', end="", flush=True)
        try:
            # don't use timeout as it doesn't work right when waiting for user input (password)
            subprocess.check_output([GITEXE] + mode.split(), cwd=d,
                                    universal_newlines=True)
            print(end="\r")
        except subprocess.CalledProcessError:
            failed.append(d.name)

        sleep(.1)  # don't hammer the remote server

    print()
    if failed:
        logging.error(f'git {mode} {rdir}')
        # no backslash allowed in f-strings
        print('\n'.join(failed), file=stderr)

    return failed
