#!/usr/bin/env python
"""
for a root directory, assumes all subdirectories are Git repos
and "git pull" each of them.
"""
import os
import asyncio
from pathlib import Path
from gitutils.pull import fetchpull
from argparse import ArgumentParser
from gitutils.git import MAGENTA, BLACK


async def find_remote(mode: str, path: Path, verbose: bool = False):

    async for d, v in fetchpull('pull', path, verbose):
        print(MAGENTA + str(d))
        print(BLACK + v)


def main():
    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    p.add_argument('-v', '--verbose', action='store_true')
    P = p.parse_args()

    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    asyncio.run(find_remote('pull', P.codepath, P.verbose))


if __name__ == '__main__':
    main()
