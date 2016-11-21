#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('requirements.txt', 'r') as r:
    requires = r.read().split()

with open('version.txt', 'r') as v:
    version = v.read().strip()

setup(
    name='python-overwatch',
    packages=['overwatch'],
    description=('A Python wrapper for playoverwatch.com'),
    version=version,
    author='Alexander J. Botello',
    author_email='alexander.botello@g.austincc.edu',
    url='https://github.com/alexbotello/python-overwatch',
    install_requires=requires,
    license='MIT-Zero'
)
