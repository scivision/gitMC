"""
These Git utilities use nothing beyond pure Python and command-line Git.
Speed is emphasized throughout, with pipelining and concurrent `asyncio` routines throughout
for fastest operation on large numbers of repos.
"""

import logging

__version__ = "1.11.0"


def _log(verbose: bool):

    if verbose:
        logging.basicConfig(level=logging.DEBUG)
