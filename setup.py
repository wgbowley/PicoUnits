"""
Filename: setup.py
Author: William Bowley
Version: 0.2
Date: 2025-12-27

Description:
    Install script for picounits — adds console script 'picounits'
"""

from setuptools import setup, find_packages

setup(
    name='picounits',
    version='0.1.0',
    description=(
        'Explicit Units and Dimensional Analysis for Scientific Python'
    ),
    author='William Bowley',
    author_email='wgrantbowley@gmail.com',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"picounits": ["py.typed", "**/*.pyi"]},
    include_package_data=True,
    install_requires=[
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
    ],
    python_requires=">=3.8",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "picounits = picounits.configuration.cli:main",
        ],
    },
)
