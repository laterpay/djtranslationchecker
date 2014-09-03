# -*- coding: UTF-8 -*-
from setuptools import find_packages, setup

import codecs
import os

#import time
#_version = "0.9.dev%s" % int(time.time())
_version = "0.9.0"
_packages = find_packages('.', exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

if os.path.exists('README.rst'):
    _long_description = codecs.open('README.rst', 'r', 'utf-8').read()
else:
    _long_description = ""

setup(
    name='djtranslationchecker',
    version=_version,

    description="Check your Django translation files",
    long_description=_long_description,
    author="LaterPay GmbH",
    author_email="support@laterpay.net",
    url="https://github.com/laterpay/djtranslationchecker",
    license='MIT',
    keywords="Django translation check gettext",

    #test_suite="tests",

    packages=_packages,

    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
)
