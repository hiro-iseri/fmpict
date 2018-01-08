# coding: utf-8

"""FMPict, combinatorial testing tool using FreeMind and PICT

See: https://github.com/hiro-iseri/fmpict/
"""


from setuptools import setup, find_packages

with open('README.md') as f:
   long_description  = f.read()

with open('LICENSE.txt') as f:
   license = f.read()

setup(name='fmpict',
     version='0.0.1',
     description='Combinatorial testing tool using FreeMind and PICT',
     author='Hiroki Iseri',
     author_email='iseri.hiroki@example.jp',
     long_description=long_description,
     url='https://github.com/hiro-iseri/fmpict',
     classifiers=[
         'Development Status :: 3 - Alpha',
         'Intended Audience :: Developers',
         'Topic :: Software Development :: Testing',
         'License :: OSI Approved :: MIT License',
         'Programming Language :: Python :: 2.7',
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.4',
         'Programming Language :: Python :: 3.5',
         'Programming Language :: Python :: 3.6',
         'Programming Language :: Python :: 3.7',
     packages=find_packages(),
     entry_points={  # Optional
         'console_scripts': [
             'fmpict = fmpict:main',
         ],
     },
)