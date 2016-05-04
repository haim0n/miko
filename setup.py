#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pygithub', 'eventlet',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='miko',
    version='0.1.0',
    description="Get a list of OpenStack project's library requirements",
    long_description=readme + '\n\n' + history,
    author="Arie Bregman, Haim Daniel",
    author_email='abregman@redhat.com',
    url='https://github.com/bregman-arie/miko',
    packages=[
        'miko',
    ],
    package_dir={'miko':
                 'miko'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='miko',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'miko = miko.__main__:main'
        ]
    }
)
