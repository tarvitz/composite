#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
import os
import sys

py_version = sys.version_info
version = ".".join([
    str(i) for i in __import__('composite.version').__VERSION__
])
readme = os.path.join(os.path.dirname(__file__), 'README.rst')

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Natural Language :: English',
    'Topic :: Utilities'
]

install_requires = [
    'six',
    'lxml',
]

extra_requires = {
    'with_simplejson': ['simplejson>=3.6.0',]
}

if isinstance(py_version, tuple):
    if py_version < (2, 7):
        install_requires.append('importlib')


setup(
    name='composite',
    author='Nickolas Fox <tarvitz@blacklibrary.ru>',
    version=version,
    author_email='tarvitz@blacklibrary.ru',
    download_url='https://github.com/tarvitz/composite/archive/master.zip',
    description='Declarative work with nested documents '
                '(JSON, XML, YAML, etc)',
    long_description=open(readme).read(),
    license='MIT license',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=install_requires,
    extra_requires=extra_requires,
    packages=find_packages(exclude=['tests', 'docs', 'documents']),
    test_suite='tests',
    include_package_data=True,
    zip_safe=False)
