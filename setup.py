#!/usr/bin/env python
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='pygitutils',
	  install_requires=required,
        packages=['pygitutils'],
	  )
