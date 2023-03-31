import argparse
from pathlib import Path
import webbrowser

from . import _log
from .git import list_changed
from .find import find_matching_file, find_dir_missing_file


p = argparse.ArgumentParser()
p.add_argument("path", help="path to look under", nargs="?", default="~/code")
p.add_argument("-v", "--verbose", action="store_true")


def find_match():
    p.add_argument("fn", help="filename to look for")
    P = p.parse_args()

    _log(P.verbose)

    for f in find_matching_file(P.fn, P.path):
        print(f)


def ActOnChanged():
    # needs to have its own argparser
    p = argparse.ArgumentParser()
    p.add_argument("path", help="root path to search under", nargs="?", default=".")
    p.add_argument("-p", "--preview", help="web browser preview of localhost", action="store_true")
    p.add_argument(
        "--port",
        help="port of localhost web server (Jekyll: 4000, Hugo: 1313)",
        type=int,
        default=1313,
    )
    p.add_argument("-v", "--verbose", action="store_true")
    P = p.parse_args()

    _log(P.verbose)

    path = Path(P.path).expanduser().resolve()
    flist = list_changed(path)
    # %%
    if P.preview:
        prefix = f"http://localhost:{P.port}/"

        cut = 11 if path.name == "_posts" else 0
        # Jekyll with leading date in filename

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
