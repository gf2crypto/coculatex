#!/usr/bin/env python
"""Setup tools for CoCuLaTeX."""

from os.path import (join,
                     dirname)
from setuptools import (setup,
                        find_packages)
import coculatex

README_FILE = 'README.md'


setup(name=coculatex.__name__,
      version=coculatex.__version__,
      description=coculatex.__description__,
      author=coculatex.__author__,
      author_email=coculatex.__email__,
      url='',
      packages=find_packages(),
      long_description=open(join(dirname(__file__), README_FILE)).read(),
      install_requires=[
          'pyyaml>=3.13',
          'jinja2>=2.10'
      ],
      entry_points={
          'console_scripts': ['{script_name}={script_name}.main:main'.format(
              script_name=coculatex.__name__)]
      })
