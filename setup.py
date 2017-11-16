#!/usr/bin/env python
req=['nose','colorama']
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
      python_requires='>=3.6',
	  )
