from setuptools import find_packages, setup

setup(
    name="phems-code",
    packages=find_packages(exclude=["app/tests"]),
)
