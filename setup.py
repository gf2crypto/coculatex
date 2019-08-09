#!/usr/bin/env python
"""
    Setup tools for LaTeXTM
"""

from os.path import (join,
                     dirname)
from setuptools import (setup,
                        find_packages)
import coculatex


setup(name=coculatex.__name__,
      version=coculatex.__version__,
      description='The cookie cutters for the LaTeX',
      author='Ivan Chizhov',
      author_email='ivchizhov@gmail.com',
      url='',
      packages=find_packages(),
      long_description=open(join(dirname(__file__), 'README.md')).read(),
      install_requires=[
          'pyyaml>=3.13',
          'jinja2>=2.10'
      ],
      entry_points={
          'console_scripts': ['{script_name}={script_name}.main:main'.format(
              script_name=coculatex.__name__)]
      })
