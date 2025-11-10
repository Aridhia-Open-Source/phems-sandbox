from setuptools import find_packages, setup

setup(
    name="phems-codeloc",
    packages=find_packages(exclude=["app/tests"]),
)
