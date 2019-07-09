import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name="mwrvr",
    version="0.0.1",
    description="A package to parse MWR videos",
    long_description=long_description,
    packages=setuptools.find_packages(),
    python_requires=">=3.7.0",
    install_requires=install_requires,
)
