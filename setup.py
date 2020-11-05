# coding: utf-8

import os
import re

import setuptools


def ascii_bytes_from(path, *paths):
    """
    Return the ASCII characters in the file specified by *path* and *paths*.
    The file path is determined by concatenating *path* and any members of
    *paths* with a directory separator in between.
    """
    file_path = os.path.join(path, *paths)
    with open(file_path) as f:
        ascii_bytes = f.read()
    return ascii_bytes


# read required text from files
thisdir = os.path.dirname(__file__)
init_py = ascii_bytes_from(thisdir, "src", "gdcapiwrapper", "__init__.py")
readme = ascii_bytes_from(thisdir, "README.md")
# This allows users to check installed version with:
# `python -c 'from gdcapiwrapper import __version__; print(__version__)'`
version = re.search('__version__ = "([^"]+)"', init_py).group(1)

install_requires = ["requests[security]", "responses", "tqdm"]

test_requires = ["pytest", "pytest-xdist", "coverage", "pytest-cov", "coveralls"]

setuptools.setup(
    name="gdc-api-wrapper",
    version=version,
    maintainer="Histolab Developers",
    maintainer_email="ernesto.arbitrio@gmail.com",
    author="E. Arbitrio",
    description="A simple Python wrapper for the GDC Application Programming Interface",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/histolab/gdc-api-wrapper",
    download_url="https://github.com/histolab/gdc-api-wrapper",
    install_requires=install_requires,
    tests_require=test_requires,
    extras_require={"testing": test_requires},
    packages=setuptools.find_packages("src", exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
    ],
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={},
    test_suite="pytest",
    zip_safe=True,
    python_requires=">=3.6",
)
