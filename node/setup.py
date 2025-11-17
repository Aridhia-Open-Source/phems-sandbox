from setuptools import find_packages, setup

setup(
    name="phems-node",
    packages=find_packages(exclude=["app/tests"]),
)
