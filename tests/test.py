#!/usr/bin/env python
from pathlib import Path
import subprocess

rdir = Path(__file__).parents[1]

print(type(rdir))
subprocess.check_call('./gtps.py ..'.split(), cwd=rdir)
