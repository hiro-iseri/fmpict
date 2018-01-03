# coding: utf-8

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setup(name='fmpict',
      version='0.0.1',
      description='Python setuptools fmpict',
      author='Hiroki Iseri',
      author_email='iseri.hiroki[a]gmail.com',
      url='https://github.com/hiro-iseri/fmpict',
      packages=find_packages(),
      licence=license,
      entry_points="""
      [console_scripts]
      greet = fmpict.fmpict:main
      """,)