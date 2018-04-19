#!/usr/bin/env python
from pathlib import Path
import subprocess,os
import unittest
from pygitutils import fetchpull

rdir = Path(__file__).parents[1]

cmd = 'python ' if os.name == 'nt' else ''
    
class Selftest(unittest.TestCase):

    def test_gitpushpullfetch(self):
        fetchpull('pull',rdir.parent)
        fetchpull('fetch',rdir.parent)

    def test_gitbranch(self):
        subprocess.check_call((cmd+'gitbranch.py ..').split(), cwd=rdir)

    def test_actonchanged(self):
        subprocess.check_call((cmd+'ActOnChanged.py .').split(), cwd=rdir)

    def test_email(self):
        subprocess.check_call((cmd+'gitemail.py').split(), cwd=rdir)

if __name__ == '__main__':
    unittest.main()
