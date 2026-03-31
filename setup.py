"""
Filename: setup.py
Author: William Bowley

Description: Local development / editable install for PicoUnits
"""

from setuptools import setup, find_packages

setup(
    name="PicoUnits",
    version="1.0.4",
    description="Explicit Units and Dimensional Analysis for Scientific Python",
    author="William Bowley",
    author_email="wgrantbowley@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"picounits": ["py.typed", "**/*.pyi"]},
    include_package_data=True,
    install_requires=["numpy"],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "picounits = picounits.configuration.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
    ],
)