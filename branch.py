#!/usr/bin/env python
"""
report on git repos not on the expected branch e.g. 'master'
"""
from argparse import ArgumentParser
from gitutils import findbranch
from pathlib import Path
import asyncio
import os
import sys


async def find_branch(branch: str, path: Path):
    path = Path(path).expanduser()

    async for b in findbranch(branch, path):
        print(b[0], ' => ', b[1])


def main():
    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    p.add_argument('mainbranch', nargs='?',
                   default='master', help='name of your main branch')
    P = p.parse_args()

    if os.name == 'nt' and (3, 7) <= sys.version_info < (3, 8):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    if sys.version_info >= (3, 7):
        asyncio.run(find_branch(P.mainbranch, P.codepath))
    else:
        if os.name == 'nt':
            loop = asyncio.ProactorEventLoop()
        else:
            loop = asyncio.new_event_loop()
            asyncio.get_child_watcher().attach_loop(loop)
        loop.run_until_complete(find_branch(P.mainbranch, P.codepath))
        loop.close()


if __name__ == '__main__':
    main()
