from pathlib import Path
from sys import stderr
import colorama
import subprocess
from random import randrange
from time import sleep
from typing import List, Tuple
import shutil


def listchanged(path: Path) -> List[str]:
    """very quick check"""
    ret = subprocess.check_output(['git', 'ls-files', '--modified'],
                                  universal_newlines=True,
                                  cwd=path)

    ret = ret.split('\n')

    return ret


def detectchange(d: Path, verbose: bool=False) -> Path:
    """in depth check"""
    c1 = ['git', 'status', '--porcelain']  # uncommitted or changed files
    dpath = None
    try:
        # %% detect uncommitted changes
        ret = subprocess.check_output(c1, cwd=d, universal_newlines=True)
        dpath = _print_change(ret, d, verbose)
        if dpath is not None:
            return dpath

# %% detect committed, but not pushed
        c0 = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']  # get branch name
        branch = subprocess.check_output(c0, cwd=d, universal_newlines=True)[:-1]

        c2 = ['git', 'diff', '--stat', f'origin/{branch}..']
        ret = subprocess.check_output(c2, cwd=d, universal_newlines=True)
        dpath = _print_change(ret, d, verbose)
    except subprocess.CalledProcessError as e:
        print('Error in', d, e.output, file=stderr)

    return dpath


def _print_change(ret: str, d: Path, verbose: bool=False) -> Path:
    dpath = None  # in case error
    if ret:
        dpath = d
        if verbose:
            print(colorama.Back.MAGENTA + str(d))
            print(colorama.Back.BLACK + ret)

    return dpath


# %%
def gitemail(path: Path, user: str, exclude: list=None) -> List[str]:
    if (path / '.nogit').is_file():
        return

    cmd = ['git', 'log', '--pretty="%ce"']

    ret = subprocess.check_output(cmd, cwd=str(path), universal_newlines=True)
    ret = ret.replace('"', '')
    ret = filter(None, ret.split('\n'))  # remove blanks
    emails = set(ret)
    if exclude:
        emails = emails.difference(set(exclude))
# %%
    emails = list(emails)
    if not (len(emails) == 1 and not user != emails[0].split('@')[0]):
        if str(path) != '.':
            print(colorama.Back.MAGENTA + str(path))

        print(colorama.Back.BLACK + '\n'.join(list(emails)))

    return emails


def fetchpull(mode: str, rdir: Path) -> List[str]:

    rdir = Path(rdir).expanduser()

    dlist = [x for x in rdir.iterdir() if x.is_dir()]

    print('git', mode, len(dlist), 'paths under', rdir)
    failed = []
    for d in dlist:
        if (d / '.nogit').is_file():  # user requesting this directory not to be synced
            continue

        print(' -->', d.name, end="", flush=True)
        try:
            # don't use timeout as it doesn't work right when waiting for user input (password)
            subprocess.check_output(['git', mode], cwd=str(d), universal_newlines=True)
            print(end="\r")
        except (subprocess.CalledProcessError, FileNotFoundError):
            failed.append(d.name)

        sleep(randrange(10) * .1 + 1)  # don't hammer the remote server, delay of 1-2 seconds

    print()
    if failed:
        print('git', mode, 'ERROR under', rdir, file=stderr)
        # no backslash allowed in f-stringss
        print('\n'.join(failed), file=stderr)

    return failed


def gitpushall(rdir: Path, verbose: bool=False) -> List[Path]:
    rdir = Path(rdir).expanduser()
    dlist = [x for x in rdir.iterdir() if x.is_dir()]

    dir_topush = []
    for d in dlist:
        if (d / '.nogit').is_file():  # user requesting this directory not to be synced
            continue

        dpath = detectchange(d, verbose)
        if dpath:
            dir_topush.append(dpath)

    return dir_topush

# replaced by git status --porcelain
# ['git','ls-files','-o','-d','--exclude-standard']): # check for uncommitted files
# ['git','--no-pager','diff','HEAD'], # check for uncommitted work
# DOES NOT WORK ['git','log','--branches','--not','--remotes'],     # check for uncommitted branches


def find_dir_missing_file(fn: str, path: Path, copyfile: Path=None) -> List[str]:
    path = Path(path).expanduser()

    dlist = [x for x in path.iterdir() if x.is_dir()]

    missing = []
    for d in dlist:
        if not (d / fn).is_file():
            if copyfile:
                shutil.copy(copyfile, d)
                print('copied', copyfile, 'to', d)
            else:
                missing.append(d)

    return missing


def findbranch(ok: str, rdir: Path) -> List[Tuple[Path, str]]:
    """find all branches in tree not matching ok"""

    rdir = Path(rdir).expanduser()

    cmd = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']

    dlist = [x for x in rdir.iterdir() if x.is_dir()]

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
