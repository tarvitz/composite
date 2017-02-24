#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import os
import sys

from composite.version import get_release

py_version = sys.version_info
version = get_release()
readme = os.path.join(os.path.dirname(__file__), 'README.rst')

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Natural Language :: English',
    'Topic :: Utilities',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6'
]

install_requires = [
    'six',
    'lxml',
]


if isinstance(py_version, tuple):
    if py_version < (2, 7):
        install_requires.append('importlib')


setup(
    name='python-composite',
    author='Nickolas Fox <tarvitz@blacklibrary.ru>',
    version=version,
    author_email='tarvitz@blacklibrary.ru',
    download_url='https://github.com/tarvitz/composite/archive/master.zip',
    description='Declarative work with nested documents '
                '(JSON, XML, etc)',
    long_description=open(readme).read(),
    license='MIT license',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=install_requires,
    packages=find_packages(exclude=['tests', 'docs', 'documents']),
    test_suite='tests',
    include_package_data=True,
    zip_safe=False)
