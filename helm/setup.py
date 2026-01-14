from setuptools import find_packages, setup

setup(
    name="phems-helm",
    packages=find_packages(exclude=["app/tests"]),
)
