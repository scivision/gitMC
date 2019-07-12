"""
These Git utilities use nothing beyond pure Python and command-line Git.
Speed is emphasized throughout, with pipelining and concurrent `asyncio` routines throughout
for fastest operation on large numbers of repos.
"""

from .runner import runner  # noqa: F401
