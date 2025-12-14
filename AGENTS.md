This Python library uses the "git" command line tool via Python asyncio to run hundreds of Git operations concurrently.

Assumptions:

* a recent version of Git is installed and accessible from the command line.
* a recent version of Python is installed.
* We're interested in showing off the capabilities of Python's asyncio library, even if a relatively new version of Python is required
* we need to work on all popular operating systems: Windows, Mac, Linux
* PyGit2 is used for certain operations as it was significantly faster than a lot of Git CLI invocations in testing.
* Asyncio.Semaphore is used to limit the number of concurrent Git commands to avoid overwhelming system resources (ulimit)
