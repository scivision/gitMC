#!/usr/bin/env python
from setuptools import setup
from pathlib import Path

setup(python_requires='>=3.6')
      scripts = [s.name for s in Path(__file__).parent.glob('*.{sh,py}') if not s.name == 'setup.py']
	  )
