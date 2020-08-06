#!/usr/bin/env python
from setuptools import setup
import glob

scripts = glob.glob("scripts/*")

setup(name='acispy_cmd',
      packages=['acispy_cmd'],
      use_scm_version=True,
      setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
      description='Python-based command-line tools for ACIS Ops',
      author='John ZuHone',
      author_email='john.zuhone@cfa.harvard.edu',
      url='http://github.com/acisops/acispy_cmd',
      install_requires=["numpy>=1.12.1","requests","astropy"],
      scripts=scripts,
      classifiers=[
          'Intended Audience :: Science/Research',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3'
      ],
      )
