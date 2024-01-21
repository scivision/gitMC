#!/usr/bin/env python3
"""
find all running Git processes

On Windows only, Git with cwd= or -C option whether plain subprocess
or asyncio.create_subprocess_shell() will leave a zombie process running.
Python 3.9...3.11 at least.
"""

import argparse
import psutil
from pprint import pprint

p = argparse.ArgumentParser(description="find all running Git processes")
p.add_argument("-kill", action="store_true", help="kill all Git processes")
p.add_argument("-v", "--verbose", action="store_true", help="verbose output")
a = p.parse_args()

name = "git"

gp = [proc for proc in psutil.process_iter() if proc.name().startswith(name)]

if a.verbose:
    pprint(gp)

print(f"found {len(gp)} Git processes")

if a.kill:
    for proc in gp:
        proc.kill()
