#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = []

test_requirements = [
    "pytest>=3",
]

setup(
    author="Tom Vo",
    author_email="tomvothecoder@gmail.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="A Python package for bumping dependencies in conda env `yml` files to the latest versions",
    entry_points={
        "console_scripts": [
            "bumpconda=bumpconda.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="bumpconda",
    name="bumpconda",
    packages=find_packages(include=["bumpconda", "bumpconda.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/tomvothecoder/bumpconda",
    version="0.1.0",
    zip_safe=False,
)
