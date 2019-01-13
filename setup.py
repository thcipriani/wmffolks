#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='WMFFolks',
    version='0.0.1',
    packages=find_packages(),
    scripts=[
        'bin/historic-wmf-folks',
        'bin/historic-wmf-folks-git-repo',
        'bin/wmf-folks',
        'bin/wmf-folks-nightly',
        'bin/wmf-folks-web',
    ],

    install_requires=[
        'beautifulsoup4',
        'bottle',
        'python-dateutil',
        'requests',
    ],

    author='Tyler Cipriani',
    author_email='tcipriani@wikimedia.org',
    description='Find all the wmf folk',
    license='GNU GPLv3',
    keywords='Wikimedia',
    url='https://github.com/thcipriani/wmffolks',
)
