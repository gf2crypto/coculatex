#!/usr/bin/env python
"""
    Setup tools for LaTeXTM
"""

from setuptools import setup, find_packages
from os.path import join, dirname
import latextm


setup(name='latextm',
      version=latextm.__version__,
      description='LaTeX themes maker',
      author='Ivan Chizhov',
      author_email='ichizhov@gmail.com',
      url='',
      packages=find_packages(),
      long_description=open(join(dirname(__file__), 'README.txt')).read(),
      install_requires=[
          'pyyaml>=3.13',
          'colorama>=0.4',
          'jinja2>=2.10'
      ],
      entry_points={
          'console_scripts': ['latextm=latextm.latextm:main']
      })
