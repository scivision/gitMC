import os
import sys
import asyncio


def runner(fun, *args):
    """
    Generic asyncio.run() equivalent for Python >= 3.5
    """
    if sys.version_info >= (3, 7):
        if os.name == "nt" and sys.version_info < (3, 8):
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        return asyncio.run(fun(*args))

    if os.name == "nt":
        loop = asyncio.ProactorEventLoop()
    else:
        loop = asyncio.new_event_loop()
        asyncio.get_child_watcher().attach_loop(loop)
    result = loop.run_until_complete(fun(*args))
    loop.close()

    return result
