#!/usr/bin/env python
from setuptools import setup

import pip
pip.main(['install','-r','requirements.txt'])


setup(name='pygitutils',
      description ='cross-platform git utilities for managing a large number of git repositories quickly',
      author = 'Michael Hirsch, Ph.D.',
      version = '1.0',
      url = 'https://github.com/scienceopen/pygitutils',
      classifiers=[
      'Development Status :: 5 - Production/Stable',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.6',
      ],
        packages=['pygitutils'],
	  )
