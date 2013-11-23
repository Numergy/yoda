#!/usr/bin/env python
from setuptools import setup


setup(
    name="yoda",
    version="0.1",
    description="",
    license="",
    scripts=["scripts/yoda"],
    packages=["yoda"],
    install_requires=[
        u"PyYaml"
    ],
    tests_require=[
        u"mock",
        u"nose",
        u"pep8"
    ]
)
