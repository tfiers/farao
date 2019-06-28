from setuptools import setup, find_packages

setup(
    name="farao",
    version="0.1",
    author="Tomas Fiers",
    author_email="tomas.fiers@gmail.com",
    url="https://github.com/tfiers/farao",
    packages=find_packages(),
    install_requires=("typeguard", "gitpython"),
)
