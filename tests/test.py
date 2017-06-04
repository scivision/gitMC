#!/usr/bin/env python
from pygitutils import Path
import subprocess

rdir = Path(__file__).parents[1]


subprocess.check_call('./gtps.py ..'.split(),cwd=rdir)
