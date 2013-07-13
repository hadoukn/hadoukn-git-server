# hadoukngit/setup.py
import os
from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

entry_points = """
    [console_scripts]
    hadoukngit = hadoukngit:main
"""

setup(name='hadoukngit',
      version='0.1',
      description='hadoukn-git-server',
      long_description=README,
      packages=find_packages(),
      test_suite='hadoukngit.tests',
      entry_points=entry_points)
