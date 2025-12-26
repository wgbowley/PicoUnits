"""
Filename: setup.py
Author: William Bowley
Version: 0.1
Date: 2025-12-14

Description:
    Install script for PicoUnits v0.1 framework
"""

from setuptools import setup, find_packages

setup(
    name='picounits',
    version='1.5.0',
    description=(
        'SI Based Unit System With Minimal Overhead And Maximal Speed'
    ),
    author='William Bowley',
    author_email='wgrantbowley@gmail.com',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
    ],
    python_requires='>=3.8',
    include_package_data=True,
)
