from setuptools import setup, find_packages

setup(
    name="fileflow",
    version="0.1",
    author="Tomas Fiers",
    author_email="tomas.fiers@gmail.com",
    url="https://github.com/tfiers/fileflow",
    packages=find_packages(),
    install_requires=(
        "typeguard ~=2.2.2",
        "gitpython ~=2.1.11",
        "decopatch ~=1.4.5",
    ),
)
