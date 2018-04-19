#!/usr/bin/env python
install_requires=['colorama']
tests_require=['pytest','nose','coveralls']
# %%
from setuptools import setup, find_packages

setup(name='pygitutils',
      packages=find_packages(),
      description ='cross-platform git utilities for managing a large number of git repositories quickly',
      long_description=open('README.rst').read(),
      author = 'Michael Hirsch, Ph.D.',
      version = '1.0.4',
      url = 'https://github.com/scivision/pygitutils',
      classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      ],
      install_requires=install_requires,
      python_requires='>=3.6',
      tests_require=tests_require,
      extras_require={'tests':tests_require,
                      'github':['pandas','numpy','tabulate','github']},
      scripts=['ActOnChanged.py','find_missing_file.py','gitbranch.py',
               'gitemail.py','git_filemode_windows.py','gtft.py',
               'gtpl.py','gtps.py','ListAllGithubRepos.py',
               ]
	  )
