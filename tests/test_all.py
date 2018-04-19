#!/usr/bin/env python
from pathlib import Path
import subprocess,os

rdir = Path(__file__).parents[1]

cmd = 'python ' if os.name == 'nt' else ''
    

def test_gitpushpullfetch():
    for s in ('gtps.py','gtpl.py','gtft.py'):
        subprocess.check_call((cmd+s+' ..').split(), cwd=rdir)

def test_gitbranch():
    subprocess.check_call((cmd+'gitbranch.py ..').split(), cwd=rdir)

def test_actonchanged():
    subprocess.check_call((cmd+'ActOnChanged.py .').split(), cwd=rdir)

def test_email():
    subprocess.check_call((cmd+'gitemail.py').split(), cwd=rdir)
