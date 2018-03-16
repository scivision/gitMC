#!/usr/bin/env python
from pathlib import Path
import subprocess

rdir = Path(__file__).parents[1]

def test_gitpush():
    subprocess.check_call('gtps.py ..'.split(), cwd=rdir)

def test_gitbranch():
    subprocess.check_call('gitbranch.py ..'.split(), cwd=rdir)

def test_actonchanged():
    subprocess.check_call('ActOnChanged.py .'.split(), cwd=rdir)
