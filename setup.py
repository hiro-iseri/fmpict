# coding: utf-8

"""FMPict, combinatorial testing tool using FreeMind and PICT
Site: https://github.com/hiro-iseri/fmpict/
License: MIT
"""

from setuptools import setup, find_packages

try:
    with open('README.md') as fr:
        long_description = fr.read()
except IOError:
    long_description = ""


setup(
    name='fmpict',
    version='0.0.1',
    description='Combinatorial testing tool using FreeMind and PICT',
    author='Hiroki Iseri',
    author_email='iseri.hiroki@gmail.com',
    long_description=long_description,
    license="MIT",
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
    ],
    packages=['fmpict'],
    entry_points={  # Optional
        'console_scripts': [
            'fmpict = fmpict:main',
        ],
    }
)
