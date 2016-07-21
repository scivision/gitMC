#!/usr/bin/env python
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='pygitutils',
	  description='Python Git Utilities generally useful',
	  author='Michael Hirsch',
	  url='https://github.com/scienceopen/pygitutils',
	  install_requires=required,
        packages=['pygitutils'],
	  )
