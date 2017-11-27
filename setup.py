#!/usr/bin/env python
install_requires=['colorama']
tests_require=['nose','coveralls']
# %%
from setuptools import setup, find_packages

setup(name='pygitutils',
      packages=find_packages(),
      description ='cross-platform git utilities for managing a large number of git repositories quickly',
      author = 'Michael Hirsch, Ph.D.',
      version = '1.0.1',
      url = 'https://github.com/scivision/pygitutils',
      classifiers=[
      'Development Status :: 5 - Production/Stable',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      ],
      install_requires=install_requires,
      python_requires='>=3.6',
      tests_require=tests_require,
      extras_require={'tests':tests_require},
	  )
