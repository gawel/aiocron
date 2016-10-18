# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup
from setuptools import find_packages

version = '0.6'

install_requires = ['croniter']
test_requires = ['coverage']

py_ver = sys.version_info[:2]
if py_ver < (3, 0):
    install_requires.extend([
        'trollius',
        'futures',
    ])
    test_requires.extend(['mock'])
elif py_ver < (3, 3):
    install_requires.append('trollius')
    test_requires.append('mock')
elif py_ver < (3, 4):
    install_requires.append('asyncio')


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='aiocron',
    version=version,
    description="Crontabs for asyncio",
    long_description=read('README.rst'),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='crontab cron asyncio',
    author='Gael Pasgrimaud',
    author_email='gael@gawel.org',
    url='https://github.com/gawel/aiocron/',
    license='MIT',
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'test': test_requires,
    },
)
