from setuptools import find_packages, setup

setup(
    name="phems-sandbox",
    packages=find_packages(exclude=["app/tests"]),
)
