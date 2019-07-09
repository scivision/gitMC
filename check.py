#!/usr/bin/env python
"""
for a root directory, assumes all subdirectories are Git repos
and "git fetch --dry-run" each
"""
import sys
import os
import logging
import asyncio
from argparse import ArgumentParser

from gitutils.pull import find_remote

MODE = ['fetch', '--dry-run']


def main():
    p = ArgumentParser()
    p.add_argument('codepath', help='path to code root', nargs='?', default='~/code')
    p.add_argument('-v', '--verbose', action='store_true')
    P = p.parse_args()

    if P.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if os.name == 'nt' and (3, 7) <= sys.version_info < (3, 8):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    if sys.version_info >= (3, 7):
        asyncio.run(find_remote(MODE, P.codepath))
    else:
        if os.name == 'nt':
            loop = asyncio.ProactorEventLoop()
        else:
            loop = asyncio.new_event_loop()
            asyncio.get_child_watcher().attach_loop(loop)
        loop.run_until_complete(find_remote(MODE, P.codepath))
        loop.close()


if __name__ == '__main__':
    main()
