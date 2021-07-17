from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="casp",
    version="0.1",
    description="Music file viewer and player",
    packages=find_packages(),
    entry_points={"console_scripts": ["casp = casp.main:run"]},
    include_package_data=True,
    python_requires=">=3.9",
    long_description=long_description,
)
