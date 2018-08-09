from pathlib import Path
from typing import List
import shutil
from .git import findbranch, gitemail, fetchpull, gitpushall, listchanged, detectchange  # noqa: F401


def find_dir_missing_file(fn: str, path: Path, copyfile: Path=None) -> List[Path]:
    path = Path(path).expanduser()

    dlist = [x for x in path.iterdir() if x.is_dir()]

    missing = []
    for d in dlist:
        if not (d / fn).is_file():
            if isinstance(copyfile, Path):
                shutil.copy(copyfile, d)
                print('copied', copyfile, 'to', d)
            else:
                missing.append(d)

    return missing
