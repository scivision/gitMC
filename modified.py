#!/usr/bin/env python
"""
detects uncommitted work/files in all git repos under a directory
"""
import os
import sys
import asyncio
from pathlib import Path
from argparse import ArgumentParser
from gitutils.push import git_modified
from gitutils.git import MAGENTA, BLACK


async def find_modified(path: Path, verbose: bool):
    c = MAGENTA if verbose else ''

    async for d, v in git_modified(path):
        print(c + str(d))
        if verbose:
            print(BLACK + v)


def main():
    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    p.add_argument('-v', '--verbose', action='store_true')
    P = p.parse_args()

    if os.name == 'nt' and (3, 7) <= sys.version_info < (3, 8):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    if sys.version_info >= (3, 7):
        asyncio.run(find_modified(P.codepath, P.verbose))
    else:
        if os.name == 'nt':
            loop = asyncio.ProactorEventLoop()
        else:
            loop = asyncio.new_event_loop()
            asyncio.get_child_watcher().attach_loop(loop)
        loop.run_until_complete(find_modified(P.codepath, P.verbose))
        loop.close()


if __name__ == '__main__':
    main()
