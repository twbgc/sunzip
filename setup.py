#!/usr/bin/env python3
# -*- coding:utf-8 -*-


with open("README.md", "r") as fh:
        long_description = fh.read()


from setuptools import setup, find_packages

setup(
    name="sunzip",
    version="0.0.3",
    keywords=("secure unzip","zipbomb"),
    description="Provide secure unzip against zip bomb.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT Licence",
    url="https://github.com/twbgc/sunzip",
    author="JunWeiSong,KunYuChen",
    author_email="sungboss2004@gmail.com",
    packages=find_packages(),
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
            "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['sunzip-cli=sunzip.cli:main'],
    }
)
