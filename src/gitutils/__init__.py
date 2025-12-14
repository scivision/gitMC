"""
These Git utilities use pygit2 where possible for much more efficient operations
than using subprocesses even with asyncio.

Speed is emphasized throughout, with pipelining and concurrent `asyncio` routines throughout
for fastest operation on large numbers of repos.
"""

import logging

__version__ = "2.1.0"


def _log(verbose: bool):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
