#! /usr/bin/env python
import io
from setuptools import setup, find_packages



def get_long_description():
    with io.open("README.rst", encoding="utf-8") as readme_file:
        readme = readme_file.read()
    # add GitHub badge in PyPi
    return readme.replace(
        "|codecov.io| |Circle CI| |PyPi downloads| |requires.io| |PyPi version| |PyPi pythons|",  #  noqa
        "|codecov.io| |Circle CI| |PyPi downloads| |requires.io| |PyPi version| |PyPi pythons| |GitHub|",
    )  #  noqa


setup(
    name="MMOGameValidator",
    long_description=get_long_description(),
    author="Qasem hajizadeh",
    author_email="gasemhacker@gmail.com",
    description="MMo Game database",
    license="BSD",
    version="0.0.1",
    url="https://github.com/Qasem-h/mmo-game-validator",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=["requests>=2.7.0"],
    tests_require=["mock", "pytest-cov", "pytest"],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Environment :: Web Environment",
        "Topic :: Software Development :: Internationalization",
    ],
)
