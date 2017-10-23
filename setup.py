#!/usr/bin/env python
req=['nose','colorama']
import pip
try:
    import conda.cli
    conda.cli.main('install', *req)
except Exception as e:
    pip.main(['install'] + req)
# %%
from setuptools import setup


setup(name='pygitutils',
      packages=['pygitutils'],
      description ='cross-platform git utilities for managing a large number of git repositories quickly',
      author = 'Michael Hirsch, Ph.D.',
      version = '1.0',
      url = 'https://github.com/scivision/pygitutils',
      classifiers=[
      'Development Status :: 5 - Production/Stable',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      ],
      install_requires=req,
	  )
