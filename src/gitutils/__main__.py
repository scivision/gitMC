from argparse import ArgumentParser
import logging
from pathlib import Path
import webbrowser

from .branch import coro_branch
from .push import coro_modified
from .pull import coro_remote
from .runner import runner
from .git import MAGENTA, BLACK, listchanged
from .find import find_matching_file, find_dir_missing_file
from .email import gitemail

p = ArgumentParser()
p.add_argument("path", help="path to look under", nargs="?", default="~/code")
p.add_argument("-v", "--verbose", action="store_true")


def _log(verbose: bool):

    if verbose:
        logging.basicConfig(level=logging.DEBUG)


def git_branch():
    """
    report on git repos not on the expected branch e.g. 'master'
    """
    p.add_argument("mainbranch", nargs="?", default="master", help="name of your main branch")
    P = p.parse_args()

    _log(P.verbose)

    branches = runner(coro_branch, P.mainbranch, P.path)
    for b in branches:
        print(b[0], " => ", b[1])


def git_modified():
    P = p.parse_args()

    _log(P.verbose)

    changes = runner(coro_modified, P.path)

    c = MAGENTA if P.verbose else ""

    for d, v in changes:
        print(c + str(d))
        if P.verbose:
            print(BLACK + v)


def git_pull():
    P = p.parse_args()

    _log(P.verbose)

    remotes = runner(coro_remote, "pull", P.path)
    txt = "\n".join(map(str, remotes))
    if txt:
        print(txt)


def git_fetch():
    P = p.parse_args()

    _log(P.verbose)

    remotes = runner(coro_remote, "fetch", P.path)
    txt = "\n".join(map(str, remotes))
    if txt:
        print(txt)


def git_check():
    P = p.parse_args()

    _log(P.verbose)

    remotes = runner(coro_remote, ["fetch", "--dry-run"], P.path)
    print("\n".join(map(str, remotes)))


def find_match():
    p.add_argument("fn", help="filename to look for")
    P = p.parse_args()

    _log(P.verbose)

    for f in find_matching_file(P.fn, P.path):
        print(f)


def ActOnChanged():
    p.add_argument("path", help="root path to search under", nargs="?", default=".")
    p.add_argument("-p", "--preview", help="web browser preview of localhost", action="store_true")
    p.add_argument("--port", help="port of localhost web server (Jekyll: 4000, Hugo: 1313)", type=int, default=1313)
    P = p.parse_args()

    _log(P.verbose)

    path = Path(P.path).expanduser().resolve()
    flist = listchanged(path)
    # %%
    if P.preview:
        prefix = "http://localhost:{}/".format(P.port)

        if path.name == "_posts":  # Jekyll with leading date in filename
            cut = 11
        else:
            cut = 0
        flist = (prefix + fn.split("/")[-1][cut:].split(".")[0] for fn in flist)

        for f in flist:
            webbrowser.open_new_tab(f)
    else:
        for f in flist:
            print(path / f)


def find_missing():
    p.add_argument("fn", help="filename to look for")
    p.add_argument("-c", "--copy", help="filepath to copy in if missing")
    P = p.parse_args()

    _log(P.verbose)

    filedest = Path(P.copy).expanduser() if P.copy else None

    for f in find_dir_missing_file(P.path, P.fn, filedest):
        print(f)


def git_email():
    p.add_argument("-e", "--exclude", help="user to ignore (keep)")
    P = p.parse_args()

    _log(P.verbose)

    for d, emails in gitemail(P.path, P.exclude):
        print(MAGENTA + d.stem + BLACK)
        for email in emails:
            print(*email)
